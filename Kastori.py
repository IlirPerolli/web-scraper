from bs4 import BeautifulSoup
import requests
from datetime import datetime

class Kastori:
    url = "https://kastori.net/jobs/?job_type%5B%5D=Tendera&p=5"
    date_format = "%d/%m/%Y"

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

            date_object = str(datetime.strptime(date, self.date_format).date())

            self.parsedData.append({
                "name": title,
                "url": url,
                "image_path": image,
                "deadline": date_object
            })

        return self.parsedData