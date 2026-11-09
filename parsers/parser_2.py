from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.event import Event


def parse(source):
    artist = source["artist"]
    url_base = source["url_base"]
    url = urljoin(url_base, source["url_suffix"])

    response = requests.get(
        url,
        impersonate="chrome",
        timeout=30
    )

    soup = BeautifulSoup(response.content, 'html.parser')
    event_elements = soup.select("article.event-upcoming")

    events = []

    for event in event_elements:
        date_element = event.select_one("time")
        title_element = event.select_one("a.underline-hover")
        location_element = event.select_one("div.post-location")

        date = date_element.get("datetime")
        title = title_element.get_text(strip=True)
        location = location_element.get_text(strip=True)
        url = title_element.get("href")

        event_data = Event(
            artist=artist,
            date=date,
            title=title,
            location=location,
            url=url,
        )

        events.append(event_data)

    return events
