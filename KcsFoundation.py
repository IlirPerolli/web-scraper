from bs4 import BeautifulSoup
import requests
from datetime import date
from Helpers import Helpers

class KcsFoundation:
    url = "https://www.kcsfoundation.org/grantet/thirrjet-e-hapura/"
    helpers = Helpers()

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')
        jobs = soup.find('ul', class_="card-list")

        all_items = jobs.find_all('li', class_ = "col-xs-12")
        for item in all_items:
            title = item.text.strip()
            url = item.find('a').get('href').strip()
            image = item.find('img').get('src').strip()

            part_title = title.split("/")[0]
            url_exists = self.helpers.check_if_url_exists("tender", part_title)

            if url_exists is not True:

                raw_text = self.helpers.get_raw_text(url)

                # openai_model = OpenAiModel("deadline", raw_text)
                # deadline = openai_model.getResponse()

                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": None,
                    "company": "Kcs"
                })

        return self.parsedData
