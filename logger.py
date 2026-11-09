import logging
from pathlib import Path

LOG_PATH = Path(__file__).parent / "logs"
LOG_PATH.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH / "tour_tracker.log", encoding="utf-8"),
    ]
)


def get_logger(name):
    return logging.getLogger(name)