from od_app.od_utils.api_utils import get_json
import datetime
from typing import List

URL = "http://events.nyu.edu/live/json/events/"


def utc_to_est(utc_time: str, date_format: str):
    import pytz

    est = pytz.timezone("US/Eastern")
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
                description=event.get("description"),
            )
            events.append(new_event)
            dupes.append(new_event["id"])

    return events


def _load_to_nyu_events_table():
    from od_app.od_utils import db_utils
    from od_app.od_utils.db_utils import NYUEvents
    from od_app import app

    db_utils.run_raw_sql(
        "TRUNCATE TABLE public.nyu_events"
    )  # delete all from table before loading
    payload = _parse_nyu_events()

    for p in payload:
        record = NYUEvents(**p)
        with app.app_context():
            db_utils.add(data=record, commit=True)


def _nyu_events_table_to_activities_table():
    from od_app.od_utils import db_utils
    from od_app.od_utils.db_utils import Activities
    from od_app import app, db

    # delete old nyu events
    with app.app_context():
        db.session.query(Activities).filter(Activities.source == "nyu_events").delete()
        db.session.commit()

    # load new nyu events
    # insert new ones
    db_utils.run_raw_sql(
        """
        INSERT INTO public.activities
            (activity_id,
             title,
             place,
             description,
             datetime,
             fee,
             url,
             img_url,
             reservation_needed,
             source,
             rsvp_list)
        SELECT Md5(n.id::varchar(20)) :: uuid,
               n.title,
               n.location,
               n.description,
               n.date_time,
               NULL,
               n.url,
               n.img_url,
               TRUE,
               'nyu_events',
               NULL
        FROM   public.nyu_events n; 
        """
    )


def nyu_events_api_to_activities_table():
    _load_to_nyu_events_table()
    _nyu_events_table_to_activities_table()
