import click
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

from ..core.logger import logger
from ..core.config import ProjectSettings, get_default_author
from ..core.errors import CLIError
from ..models.models import Mission, TestCase, Artifact, Severity
from ..models.storage import StorageManager
from ..core.cvss_utils import calculate_cvss_score, get_severity_from_score
from ..core.templates_data import OWASP_TOP_10_2021, SANS_TOP_25
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

console = Console()

BANNER = r"""
[bold cyan]
  _____            _____             __   __
 |  __ \          |  __ \            \ \ / /
 | |__) |___ _ __ | |  | | ___   ___  \ V / 
 |  ___// _ \ '_ \| |  | |/ _ \ / __|  > <  
 | |   |  __/ | | | |__| | (_) | (__  / . \ 
 |_|    \___|_| |_|_____/ \___/ \___|/_/ \_\
[/bold cyan]
[dim]  Pentest Documentation eXtended - v0.1.0[/dim]
"""

@click.group()
def cli() -> None:
    """PenDocX - Pentest Documentation eXtended"""
    console.print(BANNER)

@cli.command()
@click.option("--name", prompt="[bold blue]?[/bold blue] Project Name", help="Name of the pentest project.")
@click.option("--client", prompt="[bold blue]?[/bold blue] Client Name", help="Name of the client.")
@click.option("--author", default=get_default_author(), prompt="[bold blue]?[/bold blue] Author", help="Author of the report.")
def init(name: str, client: str, author: str) -> None:
    """Initialize a new pentest project workspace."""
    base_path = Path.cwd()
    settings = ProjectSettings(
        project_name=name,
        client_name=client,
        author=author,
        base_path=base_path
    )
    
    settings.ensure_dirs()
    
    mission = Mission(
        project_name=name,
        client_name=client,
        author=author
    )
    
    storage = StorageManager(settings.data_dir)
    storage.save_mission(mission)
    
    # Save project settings to a config file
    config_file = base_path / "pendocx_config.json"
    with open(config_file, "w") as f:
        f.write(settings.model_dump_json(indent=4))
        
    console.print(Panel(
        f"[green]Project '{name}' initialized successfully![/green]\n"
        f"Data directory: {settings.data_dir}\n"
        f"Reports directory: {settings.output_dir}\n"
        f"Config file: {config_file}",
        title="PenDocX Init"
    ))

@cli.command()
@click.option("--title", prompt="Finding Title", help="Title of the finding.")
@click.option("--severity", type=click.Choice([s.value for s in Severity]), default="Informational", prompt="Severity")
def add_test(title: str, severity: str) -> None:
    """Add a test case or finding to the mission."""
    config_file = Path.cwd() / "pendocx_config.json"
    if not config_file.exists():
        raise CLIError("Project not initialized. Run 'pendocx init' first.")
    
    with open(config_file, "r") as f:
        settings = ProjectSettings.model_validate_json(f.read())
        
    storage = StorageManager(settings.data_dir)
    mission = storage.load_mission()
    
    if not mission:
        raise CLIError("Mission data not found.")
        
    description = Prompt.ask("Description")
    impact = Prompt.ask("Impact")
    remediation = Prompt.ask("Remediation")
    
    cvss_vector = None
    cvss_score = None
    if Confirm.ask("Do you want to add a CVSS vector?", default=False):
        cvss_vector = Prompt.ask("CVSS Vector (e.g. AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)")
        cvss_score, cvss_vector = calculate_cvss_score(cvss_vector)
        if cvss_score:
            severity = get_severity_from_score(cvss_score)
            console.print(f"[bold green]Calculated CVSS Score: {cvss_score} ({severity})[/bold green]")
        else:
            console.print("[bold red]Invalid CVSS vector provided. Skipping scoring.[/bold red]")

    mapping = []
    if Confirm.ask("Do you want to add compliance mapping?", default=False):
        compliance_type = click.prompt("Mapping Type", type=click.Choice(["OWASP", "SANS", "Both"]))
        if compliance_type in ["OWASP", "Both"]:
            choices = list(OWASP_TOP_10_2021.keys())
            selected = Prompt.ask("Select OWASP Mapping", choices=choices)
            mapping.append(selected)
        if compliance_type in ["SANS", "Both"]:
            choices = list(SANS_TOP_25.keys())
            selected = Prompt.ask("Select SANS Mapping", choices=choices)
            mapping.append(selected)

    test_case = TestCase(
        title=title,
        description=description,
        impact=impact,
        remediation=remediation,
        severity=Severity(severity),
        cvss_vector=cvss_vector,
        cvss_score=cvss_score,
        compliance_mapping=mapping
    )
    
    mission.add_test_case(test_case)
    storage.save_mission(mission)
    
    table = Table(title="Finding Recorded", show_header=False, box=None)
    table.add_row("[bold cyan]Title:[/bold cyan]", title)
    table.add_row("[bold cyan]Severity:[/bold cyan]", f"[bold]{severity}[/bold]")
    if cvss_score:
        table.add_row("[bold cyan]CVSS Score:[/bold cyan]", str(cvss_score))
    if mapping:
        table.add_row("[bold cyan]Compliance:[/bold cyan]", ", ".join(mapping))
    table.add_row("[bold cyan]Mission:[/bold cyan]", mission.project_name)
    
    console.print(Panel(table, border_style="green"))

@cli.command()
def list_findings() -> None:
    """List all findings for the current mission."""
    config_file = Path.cwd() / "pendocx_config.json"
    if not config_file.exists():
        raise CLIError("Project not initialized. Run 'pendocx init' first.")
    
    with open(config_file, "r") as f:
        settings = ProjectSettings.model_validate_json(f.read())
        
    storage = StorageManager(settings.data_dir)
    mission = storage.load_mission()
    
    if not mission or not mission.test_cases:
        console.print("[yellow]No findings recorded yet.[/yellow]")
        return
        
    table = Table(title=f"Findings for {mission.project_name}")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Severity", style="bold")
    table.add_column("CVSS", justify="center")
    
    for i, test in enumerate(mission.test_cases, 1):
        color = "white"
        if test.severity == "Critical": color = "red"
        elif test.severity == "High": color = "orange1"
        elif test.severity == "Medium": color = "yellow"
        elif test.severity == "Low": color = "green"
        
        table.add_row(
            str(i),
            test.title,
            f"[{color}]{test.severity}[/]",
            str(test.cvss_score) if test.cvss_score else "-"
        )
        
    console.print(table)

@cli.command()
@click.option("--format", type=click.Choice(["word", "html", "md", "pdf"]), default="word", help="Report format.")
def generate_report(format: str) -> None:
    """Generate a penetration test report."""
    config_file = Path.cwd() / "pendocx_config.json"
    if not config_file.exists():
        raise CLIError("Project not initialized. Run 'pendocx init' first.")
    
    with open(config_file, "r") as f:
        settings = ProjectSettings.model_validate_json(f.read())
        
    storage = StorageManager(settings.data_dir)
    mission = storage.load_mission()
    
    if not mission:
        raise CLIError("Mission data not found.")
        
    if format == "word":
        from ..reporter.word_report import WordReporter
        reporter = WordReporter()
    elif format == "html":
        from ..reporter.reporters import HTMLReporter
        reporter = HTMLReporter()
    elif format == "pdf":
        from ..reporter.reporters import PDFReporter
        reporter = PDFReporter()
    else:
        from ..reporter.reporters import MarkdownReporter
        reporter = MarkdownReporter()
        
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Generating {format} report...", total=None)
        output_file = reporter.generate(mission, settings.output_dir)
        
    console.print(f"[green]✔[/green] Report generated successfully: [bold blue]{output_file}[/bold blue]")

@cli.command()
def export_json() -> None:
    """Export mission data to a standalone JSON file."""
    config_file = Path.cwd() / "pendocx_config.json"
    if not config_file.exists():
        raise CLIError("Project not initialized. Run 'pendocx init' first.")
    
    with open(config_file, "r") as f:
        settings = ProjectSettings.model_validate_json(f.read())
        
    storage = StorageManager(settings.data_dir)
    mission = storage.load_mission()
    
    if not mission:
        raise CLIError("Mission data not found.")
        
    export_file = Path.cwd() / f"{mission.project_name}_export.json"
    with open(export_file, "w") as f:
        f.write(mission.model_dump_json(indent=4))
        
    console.print(f"[green]Mission data exported to {export_file}[/green]")

if __name__ == "__main__":
    cli()
