import datetime
import sqlite3
from services.telegram_service import send_notification
from storage.db_storage import get_connection
from models.event import get_event
from logger import get_logger

logger = get_logger(__name__)


def heartbeat():
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT * FROM events WHERE artist = 'Pi'")
            result = cursor.fetchone()

    except sqlite3.OperationalError:
        logger.exception("Failed to query recorded events")
        result = ("Some", "thing", "went", "wrong", ".")

    heartbeat_event = get_event(*result)

    send_notification(heartbeat_event)


if __name__ == '__main__':
    heartbeat()
