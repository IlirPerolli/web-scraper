from datetime import timedelta, datetime

from bs4 import BeautifulSoup
import requests
from Helpers import Helpers


class RemoteCo:
    url = "https://remote.co/remote-jobs/"
    helpers = Helpers()
    date_format = "%d/%m/%Y"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('div', class_="job-card")

        for job in jobs:

            title = job.find('a').text.strip()
            urlEl = job.find('a').get('href').strip()
            url = f'https://remote.co{urlEl}'
            categoriesEl = job.find('div', class_='card-body').find_all('p')[1].text.strip()
            try:
                categories = categoriesEl.split('|')[1].strip().split(',')
            except (IndexError, AttributeError):
                categories = None

            image = job.find('img', class_='card-img').get('data-lazy-src').strip()

            url_exists = self.helpers.check_if_url_exists("job", title)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": self.helpers.add_one_month_deadline(),
                    "provider": "Remote.co",
                    "categories": categories,
                    "is_remote": True
                })

        return self.parsedData
