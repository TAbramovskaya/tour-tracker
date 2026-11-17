import datetime
import sqlite3
from services.telegram_service import send_notification
from storage.db_storage import get_connection
from models.event import get_event, get_system_event
from logger import get_logger

logger = get_logger(__name__)


def heartbeat():
    try:
        with get_connection() as conn:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            conn.execute(
                "UPDATE events SET date = ? WHERE artist = ?",
                (today, 'Pi')
            )
            cursor = conn.execute(
                "SELECT * FROM events WHERE artist = ?",
                ('Pi', )
            )
            result = cursor.fetchone()

            if result is None:
                log_message = "Heartbeat event not found in database"
                logger.error(log_message)
                heartbeat_event = get_system_event(title=log_message, location="heartbeat")

            heartbeat_event = get_event(*result)

    except sqlite3.OperationalError:
        log_message = "Heartbeat database operation failed"
        logger.exception(log_message)
        heartbeat_event = get_system_event(title=log_message, location="heartbeat")

    send_notification(heartbeat_event, header="Heartbeat")


if __name__ == '__main__':
    logger.info("Starting heartbeat service")
    heartbeat()
