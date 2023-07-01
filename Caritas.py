from bs4 import BeautifulSoup
import requests

class Caritas:
    url = "https://www.caritaskosova.org/sq/shpallje"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        jobs = soup.find_all('a', class_="document")
        for job in jobs:
            title = job.text.strip()
            url = job.get('href').strip()

            self.parsedData.append({
                "name": title,
                "url": url,
                "image_path": None,
                "deadline": None
            })

        return self.parsedData