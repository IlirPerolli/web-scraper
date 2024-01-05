from datetime import timedelta, datetime

from bs4 import BeautifulSoup
import requests
from zenrows import ZenRowsClient

from Helpers import Helpers


class StepStone:
    url = "https://www.stepstone.de/jobs/vollzeit/"
    helpers = Helpers()
    date_format = "%d/%m/%Y"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        client = ZenRowsClient("036faa034fde5136fcb3f696a6ff094037ee522d")

        params = {
            "js_render": "true",
            "premium_proxy": "true"
        }
        html = client.get(self.url, params=params).text

        soup = BeautifulSoup(html, 'html.parser')
        print (soup)

        # jobs = soup.find_all('div', class_="job-card")
        #
        # for job in jobs:
        #
        #     title = job.find('a').text.strip()
        #     urlEl = job.find('a').get('href').strip()
        #     url = f'https://remote.co{urlEl}'
        #     categoriesEl = job.find('div', class_='card-body').find_all('p')[1].text.strip()
        #     try:
        #         categories = categoriesEl.split('|')[1].strip().split(',')
        #     except (IndexError, AttributeError):
        #         categories = None
        #
        #     image = job.find('img', class_='card-img').get('data-lazy-src').strip()
        #
        #     url_exists = self.helpers.check_if_url_exists("job", title)
        #
        #     if url_exists is not True:
        #         self.parsedData.append({
        #             "name": title,
        #             "url": url,
        #             "image_path": image,
        #             "deadline": self.helpers.add_one_month_deadline(),
        #             "provider": "Remote.co",
        #             "categories": categories,
        #             "is_remote": True
        #         })
        #
        # return self.parsedData