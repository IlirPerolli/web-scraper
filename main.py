import requests
import concurrent.futures

from jobs.Indeed import Indeed
from jobs.RemoteCo import RemoteCo
from jobs.StepStone import StepStone
from tenders.Caritas import Caritas
from jobs.Gjirafa import Gjirafa
from tenders.Cdf import Cdf
from tenders.KcsFoundation import KcsFoundation
from jobs.Kastori import Kastori
from tenders.KastoriTender import KastoriTender
from jobs.KosovaJob import KosovaJob
from jobs.ArbeitsAgentur import ArbeitsAgentur
from jobs.Telegrafi import Telegrafi
from tenders.Osce import Osce
from tenders.Undp import Undp
from tenders.WorldBank import WorldBank

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


sources = [
    # {'type': 'job', 'source': RemoteCo()},
    # {'type': 'job', 'source': StepStone()},
    # {'type': 'tender', 'source': Caritas()},
    # {'type': 'tender', 'source': KcsFoundation()},
    {'type': 'job', 'source': Kastori()},
    # {'type': 'tender', 'source': KastoriTender()},
    {'type': 'job', 'source': Telegrafi()},

    {'type': 'job', 'source': Gjirafa()},
    # {'type': 'tender', 'source': Osce()},
    # {'type': 'tender', 'source': WorldBank()},
    # {'type': 'tender', 'source': Undp()},
    # {'type': 'tender', 'source': Cdf()},
    {'type': 'job', 'source': KosovaJob()},
    {'type': 'job', 'source': ArbeitsAgentur()},
    # {'type': 'job', 'source': Indeed()}
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

with open("logs.txt", "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
