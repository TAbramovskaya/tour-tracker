from services.event_service import fetch_events
from storage.json_storage import save_events
from storage.db_storage import create_table, insert_events
from models.event import get_heartbeat_event

from logger import get_logger

logger = get_logger(__name__)


def initial_load():
    events = fetch_events()

    save_events(events)

    events.append(get_heartbeat_event())

    create_table()
    insert_events(events)


if __name__ == "__main__":
    initial_load()
