from od_app.od_utils.api_utils.api_utils import get_json
from typing import List

URL = "https://data.cityofnewyork.us/resource/vjbm-hsyr.json"


def get_park_trails() -> List[dict]:
    park_trails = list()
    resp_json = get_json(URL, 200)
    for trail in resp_json:

        # only get entries with a park name, otherwise how to people know where the trail is?
        if "park_name" in trail:
            new_trail = dict(
                park_name=trail["park_name"],

                # all info besides park_name can be none
                trail_name=trail["trail_name"] if "trail_name" in trail else None,
                surface=trail["surface"] if "surface" in trail else None,
                topogragy=trail["gen_topog"] if "gen_topog" in trail else None,
                difficulty=trail["difficulty"] if "difficulty" in trail else None
            )
            park_trails.append(new_trail)

    return park_trails