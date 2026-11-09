from services.event_service import fetch_events
from services.telegram_service import send_notification
from storage.json_storage import save_events
from storage.db_storage import update_events
from logger import get_logger

logger = get_logger(__name__)


def main():
    upcoming_events = fetch_events()
    save_events(upcoming_events)

    new_events = update_events(upcoming_events)

    if new_events:
        logger.info("Sending new event notifications")
        count = len(new_events)
        for i, event in enumerate(new_events, start=1):
            logger.info("Sending %d of %d", i, count)
            send_notification(event)


if __name__ == '__main__':
    logger.info("Event update process started")
    main()
