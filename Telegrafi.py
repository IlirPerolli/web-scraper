from datetime import timedelta, datetime

from bs4 import BeautifulSoup
import requests
from Helpers import Helpers


class Telegrafi:

    url = "https://jobs.telegrafi.com/"
    helpers = Helpers()
    date_format = "%d/%m/%Y"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('div', class_="job-info")

        for job in jobs:

            titleEl = job.find('div', class_="job-name").find('h3')

            deadlineEl = job.find('div', class_="job-schedule")

            category = job.find('span', class_="puna-position-title").text.strip()

            title = titleEl.text.strip()

            date = deadlineEl.text.strip()

            deadline = self.get_deadline(date)

            url = job.find('a').get('href').strip()

            image = job.find('img').get('src').strip()

            if image == '/assets/img/passBackLogo.svg':
                image = None

            part_title = title.split("/")[0]

            url_exists = self.helpers.check_if_url_exists("job", part_title)

            if url_exists is not True:

                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": deadline,
                    "provider": "Telegrafi",
                    'country': "Kosova",
                    'category': category
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
