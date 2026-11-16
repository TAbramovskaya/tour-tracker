from services.event_service import fetch_events
from services.telegram_service import send_notification
from storage.json_storage import save_events
from storage.db_storage import update_events, find_new_events
from models.event import SYSTEM_AUTHOR
from logger import get_logger

logger = get_logger(__name__)


def main():
    upcoming_events = fetch_events()
    save_events(upcoming_events)

    new_events = find_new_events(upcoming_events)

    events_to_update = []

    if new_events:
        logger.info("Sending new event notifications")
        count = len(new_events)

        for i, event in enumerate(new_events, start=1):
            logger.info("Sending %d of %d", i, count)

            header = "New Event" if event.artist != SYSTEM_AUTHOR else "Parser Failure Warning"
            sent_status = send_notification(event, header=header)

            if sent_status:
                if event.artist != SYSTEM_AUTHOR:
                    events_to_update.append(event)

    system_event = update_events(events_to_update)  # returns () on success, otherwise a system event.

    if system_event:
        send_notification(system_event, header="Update Warning")


if __name__ == '__main__':
    logger.info("Event update process started")
    main()
