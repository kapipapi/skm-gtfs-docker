import os
import pandas as pd
from datetime import datetime, timedelta


def get_stops(dir_path):
    stops_file = os.path.join(dir_path, "stops.txt")
    return pd.read_csv(stops_file)


def read_next_arrival(stop_id: str, n=10):
    MERGED_FILENAME = os.getenv("MERGED_FILENAME")

    merged_df = pd.read_csv(MERGED_FILENAME)

    def convert_datetime(rows):
        date = rows.date
        time = rows.arrival_time

        h, m, s = rows.arrival_time.split(":")
        if h == "24":
            h = "00"
            time = f"{h}:{m}:{s}"

        return datetime.strptime(f"{date} {time}", "%Y%m%d %H:%M:%S")

    now = datetime.now()
    tomorow = now + timedelta(days=1)

    next_arrivals = merged_df[
            ( merged_df["stop_id"].astype(str) == stop_id )
            &
            ( merged_df["date"].astype(str).isin([now.strftime("%Y%m%d"), tomorow.strftime("%Y%m%d")]) )
    ].copy()

    next_arrivals["arrival_datetime"] = next_arrivals[["arrival_time", "date"]].apply(convert_datetime, axis=1)
    next_arrivals = next_arrivals[["trip_headsign", "arrival_datetime"]]
    next_arrivals = next_arrivals[next_arrivals['arrival_datetime'] > now]
    next_arrivals = next_arrivals.sort_values("arrival_datetime")
    return next_arrivals.head(n)
