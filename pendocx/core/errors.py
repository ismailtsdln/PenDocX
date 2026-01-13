"""
Custom exception classes for PenDocX.
"""

class PenDocXError(Exception):
    """Base exception for PenDocX."""
    pass

class ConfigError(PenDocXError):
    """Raised when there is a configuration error."""
    pass

class ModelError(PenDocXError):
    """Raised when there is a data model error."""
    pass

class ReporterError(PenDocXError):
    """Raised when report generation fails."""
    pass

class CLIError(PenDocXError):
    """Raised when a CLI command fails."""
    pass
