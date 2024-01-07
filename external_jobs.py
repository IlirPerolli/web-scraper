import concurrent.futures

from common.process_data import *

from external_job_scrapers.ArbeitsAgentur import ArbeitsAgentur

sources = [
    # {'type': 'job', 'source': RemoteCo()},
    # {'type': 'job', 'source': StepStone()},
    {'type': 'job', 'source': ArbeitsAgentur()},
    # {'type': 'job', 'source': Indeed()}
]

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_data, src['type'], src['source']) for src in sources]
    for future in concurrent.futures.as_completed(futures):
        future.result()

with open("logs/external_jobs_logs.txt", "w") as file:
    for log in logs:
        file.write(f"{log[0]} - Response: {log[1]}\n")
