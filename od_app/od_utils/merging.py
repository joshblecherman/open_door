from od_app.od_utils.ticketmaster.api import ticketmaster_api_to_activities_table
from od_app.od_utils.nyu_events.api import nyu_events_api_to_activities_table
from od_app.od_utils.park_trails.api import park_trails_api_to_spots_table
from timeloop import Timeloop
import datetime


def activities_merge():
    tl = Timeloop()

    @tl.job(interval=datetime.timedelta(days=1))
    def schedule():
        print("running ticketmaster load...")
        ticketmaster_api_to_activities_table()

        print("running nyu_events load...")
        nyu_events_api_to_activities_table()

    tl.start()


def spots_merge():
    tl = Timeloop()

    @tl.job(interval=datetime.timedelta(days=7))
    def schedule():
        print("running park_trails load...")
        park_trails_api_to_spots_table()

    tl.start()