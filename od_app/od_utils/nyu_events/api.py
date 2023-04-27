from od_app.od_utils.api_utils.api_utils import get_json
import datetime
from typing import List
import json

URL = "http://events.nyu.edu/live/json/events/"


def utc_to_est(utc_time: str, date_format: str):
    import pytz
    est = pytz.timezone('US/Eastern')
    eastern_time = datetime.datetime.strptime(utc_time, date_format).replace(tzinfo=est)
    return eastern_time.strftime(date_format)


def _parse_nyu_events() -> List[dict]:
    nyu_events = get_json(URL, 200)

    events = list()
    dupes = list()
    for event in nyu_events:

        # dont retrieve non MYC campus events
        # Example: events.shanghai.nyu.edu
        if "events.nyu.edu" in event["url"] and event["id"] not in dupes:
            new_event = dict(
                id=event["id"],
                title=event["title"],
                url=event["url"],
                date_time=utc_to_est(event["date_utc"], "%Y-%m-%d %H:%M:%S"),
                img_url=event["thumbnail"],
                location=event.get("location"),  # .get() returns None if key DNE
                description=event.get("description")
            )
            events.append(new_event)
            dupes.append(new_event["id"])

    return events


def _load_to_nyu_events_table():
    from od_app.od_utils import db_utils
    from od_app.od_utils.db_utils import NYUEvents
    from od_app import app

    db_utils.run_raw_sql("TRUNCATE TABLE public.nyu_events")  # delete all from table before loading
    payload = _parse_nyu_events()

    for p in payload:
        record = NYUEvents(**p)
        with app.app_context():
            db_utils.add(data=record, commit=True)
