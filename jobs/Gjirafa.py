from datetime import datetime
import re

from bs4 import BeautifulSoup
import requests
from Helpers import Helpers


class Gjirafa:

    url = "https://gjirafa.com/Top/Pune"
    helpers = Helpers()
    date_format = "%d/%m/%Y"

    def __init__(self):
        self.parsedData = []

    def get_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')

        allJobs = soup.find('ul', class_="listView")
        jobs = allJobs.find_all('li')

        for job in jobs:

            title = None
            deadline = None
            category = None
            url = None
            image = None
            titleEl = job.find('h3', id="titulli")

            if titleEl is not None:
                title = titleEl.text.strip()

            deadlineEl = job.findAll('div', class_="half mrrjp_ct")
            if len(deadlineEl) != 0 and deadlineEl is not None:
                deadlineEl = deadlineEl[1]
                deadline = self.get_deadline(deadlineEl)

            categoryEl = job.findAll('div', class_="half mrrjp_ct")
            if len(deadlineEl) != 0 and deadlineEl is not None:
                category = self.get_category(categoryEl[0])

            url = job.find('a')
            if url is not None:
                url = url.get('href').strip()

            image_el = job.find('div', class_='mp_img')
            if image_el is not None:
                image = self.getImage(image_el)

            if image == '/Images/promovoIco.png':
                image = None

            if title is not None:

                url_exists = self.helpers.check_if_url_exists("job", title, deadline)

                if url_exists is not True:

                    self.parsedData.append({
                        "name": title,
                        "url": url,
                        "image_path": image,
                        "deadline": deadline,
                        "provider": "Gjirafa",
                        'country': "Kosovo",
                        'categories': [category]
                    })

        return self.parsedData

    def get_deadline(self, deadline_el):
        deadline_pattern = r"Data e Skadimit:</em>\s*([\d/]+)"
        deadline_match = re.search(deadline_pattern, str(deadline_el))

        if deadline_match:
            deadline = deadline_match.group(1)
            deadline_date = datetime.strptime(deadline, "%d/%m/%Y").date()
            return str(deadline_date)

        return None

    def get_category(self, category_el):
        category_pattern = r"Kategoria:</em>\s*([\w\s]+)"
        category_match = re.search(category_pattern, str(category_el))

        if category_match:
            category = category_match.group(1)
        else:
            category = None

        return category

    def getImage(self, element):
        style_attribute = element['style']
        start_index = style_attribute.index("url('") + len("url('")
        end_index = style_attribute.index("')")
        return style_attribute[start_index:end_index]
