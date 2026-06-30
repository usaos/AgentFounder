import logging
import sys
import os
from pathlib import Path
def create_logger(name: str):
    logger = logging.getLogger(name)
    level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)
    logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    log_dir = Path("./data/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    try:
        fh_info = logging.FileHandler(log_dir / "agent.log")
        fh_info.setFormatter(fmt)
        fh_info.setLevel(logging.INFO)
        logger.addHandler(fh_info)
        fh_err = logging.FileHandler(log_dir / "error.log")
        fh_err.setFormatter(fmt)
        fh_err.setLevel(logging.ERROR)
        logger.addHandler(fh_err)
    except Exception: pass
    return logger
logger = create_logger("AgentFounder")
