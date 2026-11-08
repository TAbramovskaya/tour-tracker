import json
from pathlib import Path


STORAGE_DIR = Path(__file__).parent
FILENAME = "events.json"

def save_events(events):
    filepath = STORAGE_DIR / FILENAME
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            [event._asdict() for event in events],
            file,
            ensure_ascii=False,
            indent=4
        )
