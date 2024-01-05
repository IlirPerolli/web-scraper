import requests
from datetime import datetime
from Helpers import Helpers


class ArbeitsAgentur:
    date_format = "%Y-%m-%d"
    helpers = Helpers()

    def __init__(self):
        self.parsedData = []
        self.popularJobs = ['Software Developer', 'Customer service representative',
                            'Data science', 'Designer', 'Financial Analyst', 'Information Security Analyst',
                            'Database Administrator', 'Statistician', 'Krankenschwester', 'Doctor']

    def get_data(self):

        for category in self.popularJobs:
            url = f"https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs?was={category}&page=1&size=25"

            data = self.fetch_data_from_api(url)

            if data is None:
                continue

            jobs = data.get('stellenangebote', None)
            if not jobs:
                continue

            self.get_jobs(jobs, category)

        return self.parsedData

    def get_jobs(self, jobs, category):
        for item in jobs:
            title = item['titel']
            url = f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{item['refnr']}"
            deadline = self.helpers.add_one_month_deadline()
            provider = "ArbeitsAgentur"

            arbeitsort = item.get('arbeitsort', {})
            city = arbeitsort.get('ort', None)

            url_exists = self.helpers.check_if_url_exists("job", title, deadline)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": deadline,
                    "provider": provider,
                    "categories": [category],
                    "city": city,
                    'country': "Germany",
                })

    def fetch_data_from_api(self, api_url):
        try:
            response = requests.get(api_url, headers={'x-api-key': 'dcdeacbd-2b62-4261-a1fa-d7202b579848'})

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

        return datetime_obj.strftime(self.date_format)
