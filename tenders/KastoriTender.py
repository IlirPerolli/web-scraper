import requests
from datetime import datetime
from Helpers import Helpers
from OpenAi import OpenAiModel


class KastoriTender:
    url = "https://octopus-app-sngkk.ondigitalocean.app/v1/jobs?page=1&limit=32&typeOfJob=grante"
    date_format = "%Y-%m-%d"
    helpers = Helpers()

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        data = self.fetch_data_from_api(self.url)

        if data is None:
            return None

        data = data['data']
        for item in data:

            title = item['title']
            # description = item['description']
            url = f"https://www.kastori.net/shpalljet/{item['_id']}"
            image = item['company']['images']['md']['url']
            deadline = self.formatDate(item['expirationDate'])
            provider = "Kastori"
            categories = item.get('categories', [])
            category = categories[0]['title'] if categories and isinstance(categories, list) and categories else None
            city = item.get('city', None)

            url_exists = self.helpers.check_if_url_exists("tender", title, deadline)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": image,
                    "deadline": deadline,
                    "provider": provider,
                    "city": city,
                    "categories": [category],
                    'country': "Kosovo",
                })

        return self.parsedData

    def fetch_data_from_api(self, api_url):
        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Error: Unable to fetch data from API. Status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def formatDate(self, date):
        datetime_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Convert datetime object to the desired format
        return datetime_obj.strftime(self.date_format)