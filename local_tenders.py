import concurrent.futures
from common.process_data import *

from local_tender_scrapers.Caritas import Caritas
from local_tender_scrapers.Cdf import Cdf
from local_tender_scrapers.KcsFoundation import KcsFoundation
from local_tender_scrapers.KastoriTender import KastoriTender
from local_tender_scrapers.Osce import Osce
from local_tender_scrapers.Undp import Undp
from local_tender_scrapers.WorldBank import WorldBank

sources = [
    # {'type': 'tender', 'source': Caritas()},
    # {'type': 'tender', 'source': KcsFoundation()},
    # {'type': 'tender', 'source': KastoriTender()},
    # {'type': 'tender', 'source': Osce()},
    # {'type': 'tender', 'source': WorldBank()},
    # {'type': 'tender', 'source': Undp()},
    # {'type': 'tender', 'source': Cdf()},
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

with open("logs/tender_logs.txt", "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
