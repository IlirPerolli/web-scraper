from bs4 import BeautifulSoup
import requests
from datetime import datetime
from Helpers import Helpers
from OpenAi import OpenAiModel


class Kastori:
    url = "https://kastori.net/jobs/?job_type%5B%5D=Pun%C3%AB&p=1&s=0"
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

            part_title = title.split("/")[0]
            url_exists = self.helpers.check_if_url_exists(part_title)

            if url_exists is not True:
                # raw_text = self.helpers.get_raw_text(url)
                # if raw_text:
                #     openai_model = OpenAiModel("deadline", raw_text)
                #     response = openai_model.get_response()
                # else:
                #     response = None
                response = None
                try:
                    date_object = str(datetime.strptime(response, self.date_format).date())
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
