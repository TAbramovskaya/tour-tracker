import json
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)


STORAGE_DIR = Path(__file__).parent
FILENAME = "upcoming_events.json"


def save_events(events):
    filepath = STORAGE_DIR / FILENAME

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(
                [event._asdict() for event in events],
                file,
                ensure_ascii=False,
                indent=4
            )
        logger.info("Saved %d events to %s", len(events), FILENAME)

    except (OSError, TypeError, ValueError):
        logger.exception("Failed to save events to %s", filepath)
        raise