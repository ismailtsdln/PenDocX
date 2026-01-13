from typing import Tuple, Optional
from cvss import CVSS3

def calculate_cvss_score(vector: str) -> Tuple[Optional[float], Optional[str]]:
    """ Calculates the CVSS base score from a vector string. """
    try:
        # Ensure the vector starts with CVSS:3.1/
        if not vector.startswith("CVSS:3.1/"):
            if vector.startswith("CVSS:3.0/"):
                pass
            else:
                vector = f"CVSS:3.1/{vector}"
        
        c = CVSS3(vector)
        return float(c.base_score), c.clean_vector()
    except Exception:
        return None, None

def get_severity_from_score(score: float) -> str:
    """ Returns a severity level based on the CVSS score. """
    if score == 0:
        return "Informational"
    elif 0.1 <= score <= 3.9:
        return "Low"
    elif 4.0 <= score <= 6.9:
        return "Medium"
    elif 7.0 <= score <= 8.9:
        return "High"
    elif 9.0 <= score <= 10.0:
        return "Critical"
    return "Informational"
