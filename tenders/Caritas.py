from common.helpers import *


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

            url_exists = check_if_url_exists("job", title)

            if url_exists is not True:
                raw_text = get_raw_text(url)

                # openai_model = OpenAiModel("deadline", raw_text)
                # deadline = openai_model.getResponse()

                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": None,
                    "provider": "Caritas",
                    'country': "Kosovo"
                })

        return self.parsedData
