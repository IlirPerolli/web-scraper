import concurrent.futures
from common.process_data import *

from jobs.Gjirafa import Gjirafa
from jobs.Kastori import Kastori
from jobs.KosovaJob import KosovaJob
from jobs.Telegrafi import Telegrafi

sources = [
    {'type': 'job', 'source': Kastori()},
    {'type': 'job', 'source': Telegrafi()},
    {'type': 'job', 'source': Gjirafa()},
    {'type': 'job', 'source': KosovaJob()},
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

with open("logs/jobs_logs.txt", "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
