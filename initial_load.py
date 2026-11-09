from config.sources import SOURCES
from parsers.loader import get_parser
from storage.json_storage import save_events
from storage.db_storage import create_table, insert_events
from logger import get_logger

logger = get_logger(__name__)


def initial_load():
    all_events = []

    logger.info("Parsing sources for events")
    for source in SOURCES:
        parser = get_parser(source)
        events = parser(source)
        all_events.extend(events)

    logger.info("Found %d events", len(all_events))

    save_events(all_events)

    create_table()
    insert_events(all_events)


if __name__ == "__main__":
    initial_load()
