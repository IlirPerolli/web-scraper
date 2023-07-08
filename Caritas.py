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

            raw_text = self.get_raw_text(url)

            # openai_model = OpenAiModel("deadline", raw_text)
            # deadline = openai_model.getResponse()

            self.parsedData.append({
                "name": title,
                "url": url,
                "image_path": None,
                "deadline": None,
                "company": "Caritas"
            })

        return self.parsedData

    def get_raw_text(self, url):
        response = requests.get(url)
        job_content = BeautifulSoup(response.text, 'html.parser')
        text = job_content.get_text().strip()
        return text