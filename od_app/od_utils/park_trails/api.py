from od_utils.api_utils import get_json
from typing import List
import hashlib
import uuid

URL = "https://data.cityofnewyork.us/resource/vjbm-hsyr.json"


def is_named_trail(trail: dict):
    """a named trail is in an identified park and has a name that is not 'Unnamed Official Trail'"""
    return "park_name" in trail \
        and "trail_name" in trail \
        and trail["trail_name"] != "Unnamed Official Trail"


def _parse_park_trails() -> List[dict]:
    park_trails = list()
    resp_json = get_json(URL, 200)
    for trail in resp_json:

        # only get entries with a park name and a trail name
        if is_named_trail(trail):
            new_trail = dict(
                park_name=trail["park_name"],
                trail_name=trail["trail_name"],

                # all info besides park_name and trail name can be none
                surface=trail.get("surface"),
                topography=trail.get("gen_topog"),
                difficulty=trail.get("difficulty"),

                trail_id=uuid.UUID(
                    hashlib.md5(
                        bytes(trail["park_name"] + trail["trail_name"], 'utf-8')
                    ).hexdigest()
                )
            )
            park_trails.append(new_trail)

    return park_trails


def _load_to_park_trails_table():
    from od_app.od_utils import db_utils
    from od_app.od_utils.db_utils import ParkTrails
    from od_app import app
    from sqlalchemy.exc import DBAPIError

    db_utils.run_raw_sql("TRUNCATE TABLE public.park_trails")  # delete all from table before loading
    payload = _parse_park_trails()

    for p in payload:
        record = ParkTrails(**p)
        with app.app_context():
            try:
                db_utils.add(data=record, commit=True)
            except DBAPIError:
                pass


def _park_trails_table_to_spots_table():
    from od_app.od_utils import db_utils
    from od_app.od_utils.db_utils import Spots
    from od_app import app, db

    # delete old park trails
    with app.app_context():
        db.session.query(Spots).filter(Spots.source == "park_trails").delete()
        db.session.commit()

    # load new park trails
    db_utils.run_raw_sql(
        """
        INSERT INTO public.spots
            (spot_id,
             name,
             place,
             description,
             source)
        SELECT p.trail_id,
               p.trail_name,
               p.park_name,
               CONCAT_WS('</p><p>', '<p>' || p.surface, p.topography, p.difficulty || '</p>'),
               'park_trails'
        FROM   public.park_trails p; 
        """)


def park_trails_api_to_spots_table():
    _load_to_park_trails_table()
    _park_trails_table_to_spots_table()


park_trails_api_to_spots_table()