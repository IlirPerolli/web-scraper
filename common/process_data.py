import requests
from common.api import *

logs = []


def process_data(type, source):
    with requests.Session() as session:
        data = source.get_data()
        for obj in data:
            try:
                url = job_url if type == 'job' else tender_url
                response = session.post(url, json=obj)

                if response.status_code not in [201, 400]:
                    logs.append((obj, response.json()))
                print("Response:", response.json(), obj)
            except requests.exceptions.RequestException as e:
                print("An error occurred:", e, obj)
