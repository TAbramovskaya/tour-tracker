from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models.event import Event

NL_MONTHS = {
    "jan": "01",
    "feb": "02",
    "mrt": "03",
    "apr": "04",
    "mei": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "okt": "10",
    "nov": "11",
    "dec": "12"
}


def parse(source):
    artist = source["artist"]
    url_base = source["url_base"]
    source_url = urljoin(url_base, source["url_suffix"])

    response = requests.get(
        source_url,
        impersonate="chrome",
        timeout=30
    )

    soup = BeautifulSoup(response.content, 'html.parser')

    event_elements = soup.select("div.concert-cards-wrapper")

    event_urls = set()
    events = []

    for event_element in event_elements:
        event_url_element = event_element.select_one("a.card-inner")
        event_url_suffix = event_url_element.get("href")
        event_url = urljoin(url_base, event_url_suffix)
        event_urls.add(event_url)

    for event_url in event_urls:
        response = requests.get(
            event_url,
            impersonate="chrome",
            timeout=30
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        events_container = soup.select_one("div#speeldata")

        title_element = events_container.select_one("h3")
        title = title_element.get_text().replace("Alle speeldata van", "").strip()

        for date_element in events_container.select("div.speeldata-datum"):
            event_element = date_element.parent
            location_element = event_element.select_one("div.speeldata-locatie")

            location = " ".join([
                location_element.select_one("strong").get_text(strip=True),
                location_element.select_one("span").get_text(strip=True)
            ])

            date = date_element.select_one("strong").get_text(strip=True)  # current format 'vrijdag 04 dec 2026'
            day, month, year = date.split(" ")[1:]

            month_number = NL_MONTHS.get(month.lower(), "00")
            formatted_date = f"{year}-{month_number}-{day}"

            event_data = Event(
                artist=artist,
                date=formatted_date,
                title=title,
                location=location,
                url=event_url,
            )

            events.append(event_data)

    return events

