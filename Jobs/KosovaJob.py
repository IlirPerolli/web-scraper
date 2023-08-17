from datetime import timedelta, datetime

from bs4 import BeautifulSoup
import requests
from Helpers import Helpers
from zenrows import ZenRowsClient


class KosovaJob:
    url = "https://kosovajob.com/"
    helpers = Helpers()
    date_format = "%d/%m/%Y"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        client = ZenRowsClient("569a9c9a52d37d3c46ddfaed9a53edb66ecd3592")

        html = client.get(self.url).text

        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('div', class_="jobListCnts")

        for job in jobs:

            titleEl = job.find('div', class_="jobListTitle")

            cityEl = job.find('div', class_="jobListCity")

            deadlineEl = job.find('div', class_="jobListExpires")

            title = titleEl.text.strip()

            city = cityEl.text.strip()

            date = deadlineEl.text.strip()

            deadline = self.get_deadline(date)

            url = job.find('a').get('href').strip()

            image = job.find('div').attrs.get("data-background-image", None)

            url_exists = self.helpers.check_if_url_exists("job", title, deadline)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": deadline,
                    "provider": "Kosova Job",
                    'country': "Kosova",
                    'city': city
                })

        return self.parsedData

    def get_deadline(self, days):
        if days.lower() == "sot":
            date = datetime.now().strftime("%d/%m/%Y")
            return str(datetime.strptime(date, self.date_format).date())

        deadline_in_days = [int(x) for x in days.split() if x.isdigit()][0]

        current_date = datetime.now()
        future_date = current_date + timedelta(days=deadline_in_days)

        date = future_date.strftime("%d/%m/%Y")

        return str(datetime.strptime(date, self.date_format).date())
