import requests
import json
from bs4 import BeautifulSoup

class Helpers:
    tender_exists_url = "http://e-tenderi.test/api/tenders/"

    def check_if_url_exists(self, name):
        try:
            response = requests.get(str(self.tender_exists_url + name))
            if response.status_code != 200:
                return False

            response = response.json()
            return response['data'] is not None

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return False

    def get_raw_text(self, url):
        response = requests.get(url)
        job_content = BeautifulSoup(response.text, 'html.parser')
        text = job_content.get_text().strip()
        return text
