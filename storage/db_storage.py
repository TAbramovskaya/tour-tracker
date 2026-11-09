import sqlite3
from pathlib import Path
from logger import get_logger

STORAGE_DIR = Path(__file__).parent
FILENAME = "events.db"

logger = get_logger(__name__)


def get_connection():
    try:
        conn = sqlite3.connect(STORAGE_DIR / FILENAME)
        logger.debug("Database connection established")

        return conn

    except sqlite3.OperationalError:
        logger.exception("Failed to connect to database")
        raise


def create_table():
    try:
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    artist TEXT NOT NULL,
                    date TEXT NOT NULL,
                    title TEXT NOT NULL,
                    location TEXT NOT NULL,
                    url TEXT NOT NULL,
                    UNIQUE (artist, date, title, location)
                )
            """)
        logger.info("Events table is ready")

    except sqlite3.OperationalError:
        logger.info("Failed to ensure events table exists")
        raise


def insert_events(events):
    try:
        with get_connection() as conn:
            cursor = conn.executemany("""
                INSERT OR IGNORE INTO events (artist, date, title, location, url)
                VALUES (?, ?, ?, ?, ?)
            """,
            [
                (e.artist, e.date, e.title, e.location, e.url)
                for e in events
            ]
            )

            inserted = cursor.rowcount
            ignored = len(events) - inserted

            logger.info("Inserted %d events, ignored %d", inserted, ignored)

            return cursor.rowcount

    except sqlite3.OperationalError:
        logger.exception("Failed to insert events")
        raise


def query_recorded_events():
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM events")

        return cursor.fetchall()


def get_new_events(events):
    existing_events = set(e[1:5] for e in query_recorded_events())

    new_events = []
    for event in events:
        event_data = (
            event.artist,
            event.date,
            event.title,
            event.location
        )

        if event_data not in existing_events:
            new_events.append(event)

    return new_events


def update_events(events):
    new_events = get_new_events(events)

    if not new_events:
        return []

    insert_events(new_events)

    return new_events
