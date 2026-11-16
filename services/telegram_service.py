import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from html import escape
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
            return True
        else:
            logger.error(
                "Notification failed. Error code: %s. Description: %s\nMessage:\n%s",
                result.get("error_code"),
                result.get("description"),
                message
            )
            return False

    except (requests.RequestException, ValueError) as e:
        logger.error("Notification failed: %s\nMessage:\n%s", str(e), message)
        return False


def message_compose(event):
    return f"""
<b>New Event</b>

<b>Artist:</b> {escape(str(event.artist))}
<b>Date:</b> {escape(str(event.date))}
<b>Title:</b> {escape(str(event.title))}
<b>Location:</b> {escape(str(event.location))}

<a href="{escape(str(event.url))}">Event link</a>
"""
