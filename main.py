import requests
import threading
from Caritas import Caritas
from KcsFoundation import KcsFoundation
from Kastori import Kastori
from KosovaJob import KosovaJob

url = "http://e-tenderi.test/api/tenders"

clean_file = open("logs.txt", "w")
clean_file.close()

def process_data(data):
    for obj in data:
        try:
            response = requests.post(url, json=obj)
            if response.status_code != 201 and response.status_code != 400:
                file = open("logs.txt", "a")
                file.write(f"{obj} \n")
                file.close()

            print("Response:", response.json())
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)

caritas = Caritas()
kcsFoundation = KcsFoundation()
kastori = Kastori()
kosovaJob = KosovaJob()

data_caritas = caritas.get_data()
data_kcs = kcsFoundation.get_data()
data_kastori = kastori.get_data()
data_kosova_job = kosovaJob.get_data()

thread_caritas = threading.Thread(target=process_data, args=(data_caritas,))
thread_kcs = threading.Thread(target=process_data, args=(data_kcs,))
thread_kastori = threading.Thread(target=process_data, args=(data_kastori,))
thread_kosova_job = threading.Thread(target=process_data, args=(data_kosova_job,))

thread_caritas.start()
thread_kcs.start()
thread_kastori.start()
thread_kosova_job.start()

thread_caritas.join()
thread_kcs.join()
thread_kastori.join()
thread_kosova_job.join()
