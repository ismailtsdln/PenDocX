import pytest
from pathlib import Path
from pendocx.models.models import Mission, TestCase, Severity
from pendocx.models.storage import StorageManager

def test_mission_creation():
    mission = Mission(
        project_name="Test Project",
        client_name="Test Client",
        author="Test Author"
    )
    assert mission.project_name == "Test Project"
    assert len(mission.test_cases) == 0

def test_add_test_case():
    mission = Mission(
        project_name="Test Project",
        client_name="Test Client",
        author="Test Author"
    )
    test_case = TestCase(
        title="SQL Injection",
        description="Found SQLi on login page",
        impact="Critical",
        remediation="Use parameterized queries",
        severity=Severity.CRITICAL
    )
    mission.add_test_case(test_case)
    assert len(mission.test_cases) == 1
    assert mission.test_cases[0].title == "SQL Injection"

def test_storage_save_load(tmp_path):
    storage = StorageManager(tmp_path)
    mission = Mission(
        project_name="Test Project",
        client_name="Test Client",
        author="Test Author"
    )
    storage.save_mission(mission)
    
    loaded_mission = storage.load_mission()
    assert loaded_mission is not None
    assert loaded_mission.project_name == "Test Project"
