from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from download_zip import download
from dotenv import load_dotenv
import os

from unpack_info import create_merged_file, unzip_file
from read_info import get_stops, read_next_arrival

load_dotenv()

URL = os.getenv("URL")
FILENAME = os.getenv("FILENAME")
DIRNAME = os.getenv("DIRNAME")
MERGED_FILENAME = os.getenv("MERGED_FILENAME")


def download_recent_data():
    print(f"Downloading recent data from {URL} to {FILENAME}")
    is_new_zip = download(URL, FILENAME)
    is_dir_exists = os.path.exists(DIRNAME)
    is_merged_file_exists = os.path.exists(os.path.join(DIRNAME, MERGED_FILENAME))

    if is_new_zip or not is_dir_exists or not is_merged_file_exists:

        if is_dir_exists and is_new_zip:
            os.remove(DIRNAME)

        if is_merged_file_exists and is_new_zip:
            os.remove(os.path.join(DIRNAME, MERGED_FILENAME))

        unzip_file(FILENAME, DIRNAME)
        create_merged_file(DIRNAME, MERGED_FILENAME)


download_recent_data()

sched = BackgroundScheduler(daemon=True)
sched.add_job(download_recent_data, 'interval', hours=24)
sched.start()


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return get_stops(DIRNAME).to_json(orient='records', force_ascii=False)

@app.route('/stop/<id>/<n>', methods=['GET'])
def get_data(id, n):
    n = int(n)
    if not (0 < n <= 50):
        return "Number of next arrival should be between 1 and 50", 404

    if (id in get_stops(DIRNAME)["stop_id"].astype(str).tolist()):
        return read_next_arrival(id, n).to_json(orient='records', force_ascii=False)
    else:
        return "Stop not found", 404

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0')
