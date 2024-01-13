from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from download_zip import download
from dotenv import load_dotenv
import os

from service import get_stops, read_next_arrival

load_dotenv()

def download_recent_data():
    URL = os.getenv("URL")
    FILENAME = os.getenv("FILENAME")

    print(f"Downloading recent data from {URL} to {FILENAME}")
    download(URL, FILENAME)

download_recent_data()

sched = BackgroundScheduler(daemon=True)
sched.add_job(download_recent_data, 'interval', hours=24)
sched.start()


app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return get_stops().to_json(orient='records', force_ascii=False)

@app.route('/stop/<id>/<n>', methods=['GET'])
def get_data(id, n):
    n = int(n)
    if not (0 < n <= 50):
        return "Number of next arrival should be between 1 and 50", 404

    if (id in get_stops().stop_id.tolist()):
        return read_next_arrival(id, n).to_json(orient='records', force_ascii=False)
    else:
        return "Stop not found", 404

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0')
