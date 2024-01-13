import requests
import sys
import os
from datetime import datetime, timedelta

def download(url, filename):
    if os.path.exists(filename):
        file_creation_time = datetime.fromtimestamp(os.path.getctime(filename))
        if datetime.now() - file_creation_time > timedelta(hours=24):
            print("File was created more than 24h ago, downloading new version")
            os.remove(filename)
        else:
            print("File was created less than 24h ago, using cached version")
            return

    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')

    f = open(filename, "wb")

    if total_length is None: # no content length header
        f.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
            sys.stdout.flush()