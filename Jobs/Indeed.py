import re
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup
import requests
from zenrows import ZenRowsClient

from Helpers import Helpers


class Indeed:
    url = "https://www.indeed.com/jobs?q=doctor&l=Remote&vjk=cbf747028cec6cfa"
    helpers = Helpers()

    def __init__(self):
        self.parsedData = []
        self.popularJobs = ['Software Developer', 'Customer service representative', 'Virtual assistant',
                            'FlexJobs Corporation',
                            'Data science', 'Sales Representative', 'Tutor', 'Designer', 'Financial Analyst',
                            'Data entry', 'Information Security Analyst', 'Database Administrator', 'Financial Manager',
                            'Statistician']

    def get_data(self):
        client = ZenRowsClient("bb0f5c805023b6b10e61d1f8fa99e6c7ba88da50")

        params = {
            "js_render": "true",
            "premium_proxy": "true"
        }

        for category in self.popularJobs:
            html = client.get(f"https://www.indeed.com/jobs?q={category}&l=Remote&vjk=cbf747028cec6cfa",
                              params=params).text

            soup = BeautifulSoup(html, 'html.parser')

            jobs = soup.find_all('div', class_="slider_item")

            self.get_jobs(jobs, category)

        return self.parsedData

    def get_jobs(self, jobs, category):

        for job in jobs:
            salaryEl = job.find('div', class_="salary-snippet-container") or job.find('div',
                                                                                      class_="estimated-salary-container")

            title = job.find('h2', class_="jobTitle").text.strip()

            locationEl = job.find('div', class_="companyLocation").text.strip()

            city, country = self.get_location(locationEl)

            salary = None

            if salaryEl:
                salary = salaryEl.text.strip()

            partUrl = job.find('h2', class_="jobTitle").find('a').get('href')
            parsed_url = urlparse(partUrl)
            query_params = parse_qs(parsed_url.query)
            jk_attribute = query_params.get('jk', [None])[0]

            if not jk_attribute:
                continue

            url = f"https://www.indeed.com/m/viewjob?jk={jk_attribute}"

            url_exists = self.helpers.check_if_url_exists("job", title)

            if url_exists is not True:

                data_entry = {
                    "name": title,
                    "url": url,
                    "image_path": None,
                    "deadline": self.helpers.add_one_month_deadline(),
                    "categories": [category],
                    "price": salary,
                    'country': 'United States',
                    "is_remote": True,
                    "provider": "Indeed",
                }

                if city:
                    data_entry["city"] = city

                self.parsedData.append(data_entry)

    def get_location(self, location):
        pattern = r"Remote in ([a-zA-Z\s]+, [A-Z]{2} \d{5})"

        match = re.search(pattern, location)
        if match:
            location = match.group(1)

            url = f"http://api.geonames.org/searchJSON?q={location}&maxRows=10&username=ilir"

            response = requests.get(url)
            data = response.json()

            if data.get('geonames'):
                first_result = data['geonames'][0]
                city = first_result['name']
                country = first_result['countryName']

                return city, country

        return None, None
