from typing import NamedTuple
import datetime

SYSTEM_AUTHOR = "System"


class Event(NamedTuple):
    artist: str
    date: str
    title: str
    location: str
    url: str


def get_event(artist: str, date: str, title: str, location: str, url: str) -> Event:
    return Event(
        artist = artist,
        date = date,
        title = title,
        location = location,
        url = url
    )


def get_heartbeat_event():
    return Event(
        artist=SYSTEM_AUTHOR,
        date=datetime.datetime.now().strftime("%Y-%m-%d"),
        title="Heartbeat",
        location="Home",
        url="https://www.google.com",
    )


def get_system_event(title, location, artist=SYSTEM_AUTHOR, url="system"):
    return Event(
        artist=artist,
        date=datetime.datetime.now().strftime("%Y-%m-%d"),
        title=title,
        location=location,
        url="https://" + url,
    )