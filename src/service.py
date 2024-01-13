import gtfs_kit as gk
from datetime import datetime
import os

def read_feed(filename) -> gk.Feed:
    return gk.read_feed(filename, dist_units='km')


def read_next_arrival(stop_id: str, n=10):
    FILENAME = os.getenv("FILENAME")

    feed = read_feed(FILENAME)

    def convert_datetime(rows):
        date = rows.date
        time = rows.arrival_time

        h, m, s = rows.arrival_time.split(":")
        if h == "24":
            h = "00"
            time = f"{h}:{m}:{s}"

        return datetime.strptime(f"{date} {time}", "%Y%m%d %H:%M:%S")

    now = datetime.now()
    next_arrivals = gk.stops.build_stop_timetable(feed, stop_id, [now.strftime("%Y%m%d")]).copy()
    next_arrivals["arrival_datetime"] = next_arrivals[["arrival_time", "date"]].apply(convert_datetime, axis=1)
    next_arrivals = next_arrivals[["trip_headsign", "arrival_datetime"]]
    next_arrivals = next_arrivals[next_arrivals['arrival_datetime'] > now]
    next_arrivals = next_arrivals.sort_values("arrival_datetime")
    return next_arrivals.head(n)


def get_stops():
    FILENAME = os.getenv("FILENAME")

    feed = read_feed(FILENAME)
    
    return feed.stops
