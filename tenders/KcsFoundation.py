from common.helpers import *


class KcsFoundation:
    url = "https://www.kcsfoundation.org/grantet/thirrjet-e-hapura/"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')
        jobs = soup.find('ul', class_="card-list")

        all_items = jobs.find_all('li', class_="col-xs-12")
        for item in all_items:
            title = item.text.strip()
            url = item.find('a').get('href').strip()
            image = item.find('img').get('src').strip()

            url_exists = check_if_url_exists("tender", title)

            if url_exists is not True:
                raw_text = get_raw_text(url)

                # openai_model = OpenAiModel("deadline", raw_text)
                # deadline = openai_model.getResponse()

                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": None,
                    "provider": "Kcs",
                    'country': "Kosovo"
                })

        return self.parsedData
