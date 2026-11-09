from typing import NamedTuple
import datetime


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
        artist="Pi",
        date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        title="Heartbeat",
        location="Home",
        url="https://www.google.com",
    )
