import getpass
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_default_author() -> str:
    """Returns the current system username as a default author."""
    return getpass.getuser()

class ProjectSettings(BaseSettings):
    """Project-specific settings for PenDocX."""
    project_name: str = Field(..., description="The name of the penetration test mission.")
    client_name: str = Field(..., description="The name of the client.")
    version: str = "1.0.0"
    author: str = Field(default_factory=get_default_author, description="The author of the report.")
    
    # Paths
    base_path: Path = Field(default_factory=Path.cwd)
    output_dir: Path = Field(default=Path("reports"), description="Directory where reports are generated.")
    data_dir: Path = Field(default=Path("data"), description="Directory where mission data is stored.")
    artifact_dir: Path = Field(default=Path("artifacts"), description="Directory where artifacts are stored.")

    model_config = SettingsConfigDict(env_prefix="PENDOCX_")

    def ensure_dirs(self) -> None:
        """Ensures that required directories exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

def load_config(config_path: Optional[Path] = None) -> ProjectSettings:
    """Loads configuration from a JSON/YAML file or environment variables."""
    # Logic to load from file will be implemented when needed by the init command
    pass
