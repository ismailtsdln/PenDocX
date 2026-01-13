from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class Severity(str, Enum):
    """Enumeration for finding severity."""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Informational"

class Artifact(BaseModel):
    """Model for a test artifact (screenshot, logs, etc.)."""
    name: str
    path: Path
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class TestCase(BaseModel):
    """Model for a single penetration test case or finding."""
    title: str
    description: str
    impact: str
    remediation: str
    severity: Severity = Severity.INFO
    cvss_vector: Optional[str] = None
    cvss_score: Optional[float] = None
    compliance_mapping: List[str] = Field(default_factory=list, description="OWASP/SANS mappings")
    steps_to_reproduce: List[str] = Field(default_factory=list)
    artifacts: List[Artifact] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Mission(BaseModel):
    """Model for a penetration test mission."""
    project_name: str
    client_name: str
    author: str
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    test_cases: List[TestCase] = Field(default_factory=list)
    
    def add_test_case(self, test_case: TestCase) -> None:
        """Adds a test case to the mission."""
        self.test_cases.append(test_case)
        self.end_date = datetime.now()
