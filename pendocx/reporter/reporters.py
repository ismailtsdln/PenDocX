from abc import ABC, abstractmethod
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from ..models.models import Mission
from ..core.errors import ReporterError
from ..core.logger import logger

class BaseReporter(ABC):
    """Abstract base class for all reporters."""
    
    @abstractmethod
    def generate(self, mission: Mission, output_path: Path) -> Path:
        """Generates a report from mission data."""
        pass

class MarkdownReporter(BaseReporter):
    """Generates a Markdown report."""
    
    def generate(self, mission: Mission, output_path: Path) -> Path:
        try:
            template_str = """# Penetration Test Report: {{ mission.project_name }}

**Client:** {{ mission.client_name }}
**Author:** {{ mission.author }}
**Date:** {{ mission.start_date.strftime('%Y-%m-%d') }}

## Summary of Findings
{% for test in mission.test_cases %}
- [{{ test.severity }}] {{ test.title }}
{% endfor %}

## Findings Detail
{% for test in mission.test_cases %}
### {{ loop.index }}. {{ test.title }}
**Severity:** {{ test.severity }}

#### Description
{{ test.description }}

#### Impact
{{ test.impact }}

#### Remediation
{{ test.remediation }}
{% endfor %}
"""
            from jinja2 import Template
            template = Template(template_str)
            content = template.render(mission=mission)
            
            output_file = output_path / f"{mission.project_name}_report.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"Markdown report generated at [blue]{output_file}[/blue]")
            return output_file
        except Exception as e:
            raise ReporterError(f"Failed to generate Markdown report: {e}")

class HTMLReporter(BaseReporter):
    """Generates a premium HTML report."""
    
    def generate(self, mission: Mission, output_path: Path) -> Path:
        try:
            template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ mission.project_name }} - Security Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
            --primary: #38bdf8;
            --accent: #818cf8;
            --critical: #ef4444;
            --high: #f97316;
            --medium: #f59e0b;
            --low: #10b981;
            --info: #0ea5e9;
        }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; margin: 0; padding: 40px; }
        .container { max-width: 1000px; margin: 0 auto; }
        header { border-bottom: 2px solid var(--primary); padding-bottom: 20px; margin-bottom: 40px; }
        h1 { font-size: 2.5rem; margin: 0; color: var(--primary); }
        .meta { display: flex; gap: 40px; margin-top: 10px; color: #94a3b8; }
        .finding { background: var(--card-bg); border-radius: 12px; padding: 30px; margin-bottom: 30px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); border-left: 6px solid #ccc; }
        .finding.severity-Critical { border-left-color: var(--critical); }
        .finding.severity-High { border-left-color: var(--high); }
        .finding.severity-Medium { border-left-color: var(--medium); }
        .finding.severity-Low { border-left-color: var(--low); }
        .finding.severity-Informational { border-left-color: var(--info); }
        .badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin-bottom: 10px; }
        .badge-Critical { background: var(--critical); color: #fff; }
        .badge-High { background: var(--high); color: #fff; }
        .badge-Medium { background: var(--medium); color: #fff; }
        .badge-Low { background: var(--low); color: #fff; }
        .badge-Informational { background: var(--info); color: #fff; }
        .cvss { background: #334155; padding: 10px 15px; border-radius: 8px; font-family: monospace; font-size: 0.9rem; display: inline-block; margin-top: 10px; }
        .compliance { margin-top: 15px; font-size: 0.9rem; color: var(--accent); }
        .compliance span { background: #4338ca; color: white; padding: 2px 8px; border-radius: 4px; margin-right: 5px; }
        h3 { font-size: 1.5rem; margin-top: 0; }
        .section-title { font-weight: 600; color: var(--primary); margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ mission.project_name }}</h1>
            <div class="meta">
                <span><strong>Client:</strong> {{ mission.client_name }}</span>
                <span><strong>Author:</strong> {{ mission.author }}</span>
                <span><strong>Date:</strong> {{ mission.start_date.strftime('%Y-%m-%d') }}</span>
            </div>
        </header>

        {% for test in mission.test_cases %}
        <div class="finding severity-{{ test.severity }}">
            <span class="badge badge-{{ test.severity }}">{{ test.severity }}</span>
            <h3>{{ test.title }}</h3>
            
            {% if test.cvss_score %}
            <div class="cvss">CVSS Base Score: {{ test.cvss_score }} | Vector: {{ test.cvss_vector }}</div>
            {% endif %}

            {% if test.compliance_mapping %}
            <div class="compliance">
                {% for map in test.compliance_mapping %}
                <span>{{ map }}</span>
                {% endfor %}
            </div>
            {% endif %}

            <div class="section-title">Description</div>
            <p>{{ test.description }}</p>

            <div class="section-title">Impact</div>
            <p>{{ test.impact }}</p>

            <div class="section-title">Remediation</div>
            <p>{{ test.remediation }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""
            from jinja2 import Template
            template = Template(template_str)
            content = template.render(mission=mission)
            
            output_file = output_path / f"{mission.project_name}_report.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"HTML report generated at [blue]{output_file}[/blue]")
            return output_file
        except Exception as e:
            raise ReporterError(f"Failed to generate HTML report: {e}")
