from config.sources import SOURCES
from parsers.loader import get_parser
from models.event import get_system_event
from logger import get_logger

logger = get_logger(__name__)


def fetch_events():
    events = []

    logger.info("Parsing sources for events")
    for source in SOURCES:
        try:
            parser = get_parser(source)
            source_events = parser(source)
            events.extend(source_events)

        except Exception as e:
            logger.exception("Failed to fetch events from the source %s", source["url_base"])

            return [
                get_system_event(
                    title=f'Failed to fetch events: {source["artist"]}',
                    location="fetch_events",
                    url=source["url_base"]
                )
            ]

    logger.info("Found %d events", len(events))
    return events
