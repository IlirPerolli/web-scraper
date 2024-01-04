from datetime import datetime, timedelta

import requests
import json
from bs4 import BeautifulSoup


class Helpers:
    tender_exists_url = "https://punapune.com/api/tenders/"
    job_exists_url = "https://punapune.com/api/jobs/"

    def check_if_url_exists(self, type, name, deadline=None):
        try:
            params = {
                'name': name,
            }

            if deadline is not None:
                params['deadline'] = deadline

            if type == 'job':
                response = requests.get(self.job_exists_url, params=params)
            else:
                response = requests.get(self.tender_exists_url, params=params)

            if response.status_code != 200:
                return False

            response = response.json()
            return response['data'] is not None

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return False

    def get_raw_text(self, url):
        if not self.is_webpage(url):
            return False

        response = requests.get(url)
        job_content = BeautifulSoup(response.text, 'html.parser')
        text = job_content.get_text().replace("\n", "").strip()

        return text

    def is_webpage(self, url):
        response = requests.head(url)
        content_type = response.headers.get("content-type")
        if content_type is None:
            return False
        return content_type.startswith("text/html")

    def add_one_month_deadline(self):
        current_date = datetime.now()

        one_month_from_now = current_date + timedelta(days=30)

        date_format = "%Y-%m-%d"

        return one_month_from_now.strftime(date_format)

