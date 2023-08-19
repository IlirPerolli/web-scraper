from bs4 import BeautifulSoup
import requests
from Helpers import Helpers


class Osce:
    url = "https://procurement.osce.org/tenders?f%5B0%5D=source%3AOSCE%20Mission%20in%20Kosovo"
    helpers = Helpers()

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('article')

        for job in jobs:
            title = job.find('h4').find('a').text.strip()
            part_url = job.find('h4').find('a').get('href').strip()
            url = f"https://procurement.osce.org{part_url}"
            deadlineEl = job.find('time').get('datetime')
            deadline = deadlineEl.split('T')[0]

            url_exists = self.helpers.check_if_url_exists("tender", title)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": deadline,
                    "provider": "Osce",
                    'country': "Kosovo"
                })

        return self.parsedData
