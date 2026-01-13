import logging
import sys
from rich.logging import RichHandler

def setup_logger(name: str = "pendocx", level: int = logging.INFO) -> logging.Logger:
    """Sets up a logger with Rich handler."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )

    logger = logging.getLogger(name)
    return logger

logger = setup_logger()
