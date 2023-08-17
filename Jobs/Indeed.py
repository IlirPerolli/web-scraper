from datetime import timedelta, datetime
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup
import requests
from zenrows import ZenRowsClient

from Helpers import Helpers


class Indeed:
    url = "https://www.indeed.com/jobs?q=doctor&l=Remote&vjk=cbf747028cec6cfa"
    helpers = Helpers()

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        client = ZenRowsClient("569a9c9a52d37d3c46ddfaed9a53edb66ecd3592")

        params = {
            "js_render": "true",
            "premium_proxy": "true"
        }

        html = client.get(self.url, params=params).text

        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('div', class_="slider_item")

        for job in jobs:
            salaryEl = job.find('div', class_="salary-snippet-container") or job.find('div',
                                                                                      class_="estimated-salary-container")

            title = job.find('h2', class_="jobTitle").text.strip()
            salary = None

            if salaryEl:
                salary = salaryEl.text.strip()

            partUrl = job.find('h2', class_="jobTitle").find('a').get('href')
            parsed_url = urlparse(partUrl)
            query_params = parse_qs(parsed_url.query)
            jk_attribute = query_params.get('jk', [None])[0]

            if not jk_attribute:
                continue

            url = f"https://www.indeed.com/m/viewjob?jk={jk_attribute}"

            url_exists = self.helpers.check_if_url_exists("job", title)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": self.helpers.add_one_month_deadline(),
                    "category": "Computer Science",
                    "price": salary,
                    "provider": "Indeed",
                    "country": "Remote",
                })

        return self.parsedData
