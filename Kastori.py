from bs4 import BeautifulSoup
import requests
from datetime import datetime
from Helpers import Helpers
from OpenAi import OpenAiModel


class Kastori:
    url = "https://kastori.net/jobs/?job_type%5B%5D=Tendera&p=5"
    date_format = "%d/%m/%Y"
    helpers = Helpers()

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('article', class_="listing-item__jobs")
        for job in jobs:
            title = job.find('div', class_='listing-item__title').text.strip()
            image = job.find('img', class_='profile__img-company').get('src').strip()
            url = job.find('div', class_='listing-item__title').find('a').get('href').strip()
            date = job.find('div', class_='listing-item__date').text.strip()

            url_exists = self.helpers.check_if_url_exists(title)

            if url_exists is not True:
                # raw_text = self.helpers.get_raw_text(url)
                #
                # openai_model = OpenAiModel("deadline", raw_text)
                # deadline = openai_model.getResponse()
                #
                try:
                    date_object = str(datetime.strptime(date, self.date_format).date())
                except:
                    date_object = None

                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": date_object,
                    "company": "Kastori"
                })

        return self.parsedData
