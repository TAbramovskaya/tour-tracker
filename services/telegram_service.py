import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from logger import get_logger

ENV_FILE = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

logger = get_logger(__name__)


def send_notification(event):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    message = message_compose(event)
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "disable_notification": True
    }

    try:
        response = requests.post(url, json=payload, timeout=5)

        response.raise_for_status()
        result = response.json()
        if result.get("ok"):
            logger.info("Notification sent")
        else:
            logger.error(
                "Notification failed. Error code %s", result.get("error_code"))

    except (requests.HTTPError, requests.RequestException, ValueError) as e:
        logger.error("Notification failed: %s", str(e))


def message_compose(event):
    return f"""
<b>New Event</b>

<b>Artist:</b> {event.artist}
<b>Date:</b> {event.date}
<b>Title:</b> {event.title}
<b>Location:</b> {event.location}

<a href="{event.url}">Event link</a>
"""
