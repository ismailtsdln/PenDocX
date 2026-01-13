import json
from pathlib import Path
from typing import Optional
from .models import Mission
from ..core.errors import ModelError
from ..core.logger import logger

class StorageManager:
    """Manages mission data persistence."""
    
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.mission_file = data_path / "mission.json"

    def save_mission(self, mission: Mission) -> None:
        """Saves mission data to a JSON file."""
        try:
            self.data_path.mkdir(parents=True, exist_ok=True)
            with open(self.mission_file, "w", encoding="utf-8") as f:
                f.write(mission.model_dump_json(indent=4))
            logger.info(f"Mission data saved to [blue]{self.mission_file}[/blue]")
        except Exception as e:
            raise ModelError(f"Failed to save mission data: {e}")

    def load_mission(self) -> Optional[Mission]:
        """Loads mission data from a JSON file."""
        if not self.mission_file.exists():
            return None
        
        try:
            with open(self.mission_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Mission.model_validate(data)
        except Exception as e:
            raise ModelError(f"Failed to load mission data: {e}")
