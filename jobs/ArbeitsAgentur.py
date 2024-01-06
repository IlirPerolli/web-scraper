import requests
from datetime import datetime
from Helpers import Helpers


class ArbeitsAgentur:
    date_format = "%Y-%m-%d"
    helpers = Helpers()

    def __init__(self):
        self.parsedData = []
        self.popularJobs = ['Informatik', 'IT-Systemanalyse, -Anwendungsberatung und -Vertrieb',
                            'Softwareentwicklung und Programmierung', 'Einkauf und Vertrieb',
                            'Steuerberatung', 'Unternehmensorganisation und -strategie',
                            'IT-Netzwerktechnik, -Administration, -Organisation', 'Werbung und Marketing',
                            'Personalwesen und -dienstleistung','Versicherungs- und Finanzdienstleistungen',
                            'Elektrotechnik','Rechtsberatung, -sprechung und -ordnung']

    def get_data(self):

        self.get_jobs_based_on_type(is_remote=True)
        self.get_jobs_based_on_type(is_remote=False)

        return self.parsedData

    def get_jobs(self, jobs, category, is_remote):
        for item in jobs:

            title = item.get('titel', None)

            if not title:
                continue

            url = f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{item['refnr']}"
            provider = "ArbeitsAgentur"

            arbeitsort = item.get('arbeitsort', {})
            city = arbeitsort.get('ort', None)

            url_exists = self.helpers.check_if_url_exists(type="job", name=title, deadline=None, url=url)

            if url_exists is not True:
                self.parsedData.append({
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": None,
                    "provider": provider,
                    "categories": [category],
                    "city": city,
                    'country': "Germany",
                    "is_remote": is_remote,
                })

    def get_jobs_based_on_type(self, is_remote):
        for category in self.popularJobs:

            if is_remote:
                url = f"https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs?berufsfeld={category}&page=1&size=25&arbeitszeit=ho"
            else:
                url = f"https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs?berufsfeld={category}&page=1&size=25&arbeitszeit=vz"

            data = self.fetch_data_from_api(url)

            if data is None:
                continue

            jobs = data.get('stellenangebote', None)
            if not jobs:
                continue

            self.get_jobs(jobs, category, is_remote)

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
