from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def configure_logging(log_dir: str | Path = ".jarvis/logs", level: str = "INFO") -> None:
    path = Path(log_dir); path.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(path / "jarvis.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger = logging.getLogger("jarvis"); logger.setLevel(level.upper())
    if not logger.handlers: logger.addHandler(handler)
