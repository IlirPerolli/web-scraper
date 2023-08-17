import requests
import threading

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

clean_file = open("logs.txt", "w")
clean_file.close()


def process_data(type, data):
    for obj in data:
        try:
            if type == 'job':
                response = requests.post(job_url, json=obj)
            else:
                response = requests.post(tender_url, json=obj)

            if response.status_code != 201 and response.status_code != 400:
                file = open("logs.txt", "a")
                file.write(f"{obj} \n")
                file.close()

            print("Response:", response.json(), obj)
        except requests.exceptions.RequestException as e:

            print("An error occurred:", e, obj)


caritas = Caritas()
kcsFoundation = KcsFoundation()
kastori = Kastori()
kastoriTender = KastoriTender()
kosovaJob = KosovaJob()
telegrafi = Telegrafi()
gjirafa = Gjirafa()
osce = Osce()
world_bank = WorldBank()
undp = Undp()
cdf = Cdf()
indeed = Indeed()

data_caritas = caritas.get_data()
data_kcs = kcsFoundation.get_data()
data_kastori = kastori.get_data()
data_kastori_tender = kastoriTender.get_data()
data_kosova_job = kosovaJob.get_data()
data_telegrafi = telegrafi.get_data()
data_gjirafa = gjirafa.get_data()
data_osce = osce.get_data()
data_world_bank = world_bank.get_data()
data_undp = undp.get_data()
data_cdf = cdf.get_data()
data_indeed = indeed.get_data()

thread_caritas = threading.Thread(target=process_data, args=('tender', data_caritas,))
thread_kcs = threading.Thread(target=process_data, args=('tender', data_kcs,))
thread_kastori = threading.Thread(target=process_data, args=('job', data_kastori,))
thread_kastori_tender = threading.Thread(target=process_data, args=('tender', data_kastori_tender,))
thread_kosova_job = threading.Thread(target=process_data, args=('job', data_kosova_job,))
thread_telegrafi = threading.Thread(target=process_data, args=('job', data_telegrafi,))
thread_gjirafa = threading.Thread(target=process_data, args=('job', data_gjirafa,))
thread_osce = threading.Thread(target=process_data, args=('tender', data_osce,))
thread_world_bank = threading.Thread(target=process_data, args=('tender', data_world_bank,))
thread_undp = threading.Thread(target=process_data, args=('tender', data_undp,))
thread_cdf = threading.Thread(target=process_data, args=('tender', data_cdf,))
thread_indeed = threading.Thread(target=process_data, args=('job', data_indeed,))

thread_caritas.start()
thread_kcs.start()
thread_kastori.start()
thread_kastori_tender.start()
thread_kosova_job.start()
thread_telegrafi.start()
thread_gjirafa.start()
thread_osce.start()
thread_world_bank.start()
thread_undp.start()
thread_cdf.start()
thread_indeed.start()

thread_caritas.join()
thread_kcs.join()
thread_kastori.join()
thread_kastori_tender.join()
thread_kosova_job.join()
thread_telegrafi.join()
thread_gjirafa.join()
thread_osce.join()
thread_world_bank.join()
thread_undp.join()
thread_cdf.join()
thread_indeed.join()
