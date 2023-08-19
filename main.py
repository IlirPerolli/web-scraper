import requests
import concurrent.futures

# Assuming you have these imports at the top of your file
from Jobs.Indeed import Indeed
from Tenders.Caritas import Caritas
from Jobs.Gjirafa import Gjirafa
from Tenders.Cdf import Cdf
from Tenders.KcsFoundation import KcsFoundation
from Jobs.Kastori import Kastori
from Tenders.KastoriTender import KastoriTender
from Jobs.KosovaJob import KosovaJob
from Jobs.Telegrafi import Telegrafi
from Tenders.Osce import Osce
from Tenders.Undp import Undp
from Tenders.WorldBank import WorldBank

tender_url = "http://e-tenderi.test/api/tenders"
job_url = "http://e-tenderi.test/api/jobs"
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
    {'type': 'tender', 'source': Caritas()},
    {'type': 'tender', 'source': KcsFoundation()},
    {'type': 'job', 'source': Kastori()},
    {'type': 'tender', 'source': KastoriTender()},
    {'type': 'job', 'source': Telegrafi()},

    {'type': 'job', 'source': Gjirafa()},
    {'type': 'tender', 'source': Osce()},
    {'type': 'tender', 'source': WorldBank()},
    {'type': 'tender', 'source': Undp()},
    {'type': 'tender', 'source': Cdf()},
    {'type': 'job', 'source': KosovaJob()},
    {'type': 'job', 'source': Indeed()}
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

with open("logs.txt", "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
