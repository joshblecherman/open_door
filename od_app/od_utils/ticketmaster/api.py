import datetime
import time
from typing import *


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


def _get_response_pages(url: str) -> Iterator[dict]:
    """
    :param response_json: events response json
    :return: iterator for pages in request
    """
    from od_app.od_utils.api_utils.api_utils import get_json

    curr_resp_json = get_json(url, 200)
    yield curr_resp_json
    while "next" in curr_resp_json["_links"]:
        next_url = URL + curr_resp_json["_links"]["next"]["href"] + f"&apikey={API_KEY}"
        curr_resp_json = get_json(next_url, 200)
        yield curr_resp_json


def _parse_ticketmaster_events(url: str) -> List[dict]:
    """
    :param response_json: response json for NYC_EVENTS_URL
    :return: a list of dictionaries for each event
    """

    events = list()
    for page in _get_response_pages(url):
        page_events = page["_embedded"]["events"]
        for event in page_events:
            new_event = dict(
                name=event["name"],
                id=event["id"],
                url=event["url"],
                date=datetime.datetime.strptime(event["dates"]["start"]["localDate"], "%Y-%m-%d"),
                time=time.strptime(event["dates"]["start"]["localTime"], "%H:%M:%S"),
                img_url=event["images"][0]["url"]  # get the url of the first image
            )
            events.append(new_event)

    return events


def _get_ticketmaster_events() -> List[dict]:
    url = _get_ticketmaster_events_url()
    return _parse_ticketmaster_events(url)


def _ticketmaster_api_to_ticketmaster_table():
    from od_app.od_utils import db_utils
    from od_app.od_utils.db_utils import Ticketmaster
    from od_app import app

    db_utils.run_raw_sql("TRUNCATE TABLE Ticketmaster")  # delete all from table before loading
    payload = _get_ticketmaster_events()

    for p in payload:
        record = Ticketmaster(**p)
        with app.app_context():
            db_utils.add(data=record, commit=True, overwrite=True)


def _ticketmaster_table_to_activities_table():
    from od_app.od_utils import db_utils
    db_utils.run_raw_sql(
        """
        WITH activities_conversion (
            activities_id, title, place, description, datetime, fee, url, img, reservation_needed, rsvp_list
        ) as 
        SELECT (
            uuid(id), name,  NULL,  NULL, date + time, NULL, url, NULL, True, NULL 
        ) FROM Ticketmaster 
        INSERT * INTO Activities FROM activities_conversion  
        """
    )


def ticketmaster_api_to_activities_table():
    _ticketmaster_api_to_ticketmaster_table()
    _ticketmaster_table_to_activities_table()

