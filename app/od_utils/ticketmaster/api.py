import json
import datetime
from typing import *
from app.od_utils.api_utils.api_utils import get_json

API_SECRET = "J0zAFpB9xDbb9o4Y"  # not sure if it is needed for anything, but here just in case
API_KEY = "eKRil5sqCyPFlHFxHTB7ubR4avgMG1pI"

PAGE_SIZE = 50  # max number of results we get back per page, must be < 200

CITY = "New York City"
SORT = "date,asc"

URL = "https://app.ticketmaster.com"
API_URL = f"{URL}/discovery/v2"
EVENTS_URL = f"{API_URL}/events.json?"


def _get_ticketmaster_events_url() -> str:
    """
    :return: url for all relevant ticketmaster events in NYC after today's date
    """
    start_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{EVENTS_URL}city={CITY}&size={PAGE_SIZE}&apikey={API_KEY}&sort={SORT}&startDateTime={start_time}"


def _get_response_pages(response_json: dict) -> Iterator[dict]:
    """
    :param response_json: events response json
    :return: iterator for pages in request
    """
    curr_resp_json = response_json
    while "next" in curr_resp_json["_links"]:
        next_url = URL + curr_resp_json["_links"]["next"]["href"] + f"&apikey={API_KEY}"
        curr_resp_json = get_json(next_url, 200)
        yield curr_resp_json


def _parse_ticketmaster_events(response_json: dict) -> List[dict]:
    """
    :param response_json: response json for NYC_EVENTS_URL
    :return: a list of dictionaries for each event
    """

    events = list()
    for page in _get_response_pages(response_json):
        page_events = page["_embedded"]["events"]
        for event in page_events:
            new_event = dict(
                event_name=event["name"],
                id=event["id"],
                url=event["url"],
                start_date=event["dates"]["start"]["localDate"],
                start_time=event["dates"]["start"]["localTime"],
                # TODO: add end_date, end_time IF it exists
                # TODO: Maybe add genre, images
            )
            events.append(new_event)

    return events


def get_ticketmaster_events() -> List[dict]:
    url = _get_ticketmaster_events_url()
    r_json = get_json(url, 200)
    return _parse_ticketmaster_events(r_json)

