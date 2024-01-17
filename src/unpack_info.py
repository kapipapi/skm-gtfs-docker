import zipfile
import pandas as pd
import os


def unzip_file(file_path, destination_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(destination_path)

def create_merged_file(dir_path, merged_file):
    stop_times_file = os.path.join(dir_path, "stop_times.txt")
    trips_file = os.path.join(dir_path, "trips.txt")
    routes_file = os.path.join(dir_path, "routes.txt")
    services_file = os.path.join(dir_path, "calendar_dates.txt")

    stop_times_df = pd.read_csv(stop_times_file)
    trips_df = pd.read_csv(trips_file)
    routes_df = pd.read_csv(routes_file)
    services_df = pd.read_csv(services_file)

    merged_df = pd.merge(stop_times_df, trips_df, on='trip_id')
    merged_df = pd.merge(merged_df, routes_df, on='route_id')
    merged_df = pd.merge(merged_df, services_df, on='service_id')

    merged_df.to_csv(merged_file, index=False)