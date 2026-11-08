import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.event import Event


def parse(source):
    artist = source["artist"]
    url_base = source["url_base"]
    url = urljoin(url_base, source["url_suffix"])

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    event_elements = soup.select("article.eventlist-event--upcoming")

    events_list = []

    for event in event_elements:
        date_element = event.select_one("time.event-date")
        title_element = event.select_one("a.eventlist-title-link")
        location_element = event.select_one("li.eventlist-meta-address")
        map_element = event.select_one("a.eventlist-meta-address-maplink")

        date = date_element.get("datetime", "") if date_element else ""
        title = title_element.get_text(strip=True) if title_element else ""
        location = (
            location_element.get_text(strip=True).removesuffix("(map)").strip()
            if location_element else "")
        url = urljoin(url_base, title_element.get("href", "")) if location_element else ""

        if map_element:
            map_url = map_element.get("href", "")
            map_location = map_url.split("?q=", 1)[1] if "?q=" in map_url else ""

            if map_location:
                location = f"{location} ({map_location})"

        event_data = Event(
            artist=artist,
            date=date,
            title=title,
            location=location,
            url=url,
        )

        events_list.append(event_data)

    return events_list
