"""This script scrapes tech codes and names from USPTO site"""

from collections import namedtuple
import csv
import requests
from bs4 import BeautifulSoup

URL = 'http://www.uspto.gov/web/patents/classification/selectnumwithtitle.htm'
REQUEST = requests.get(URL)
SOUP = BeautifulSoup(REQUEST.text, "html.parser")

TECH_CODES = []
ClassRow = namedtuple('ClassRow', 'class_code class_name')

print('Scraping data')
for table_row in SOUP.find_all('tr'):
    class_code_tag = table_row.find('td', width='27')

    # not a class_code + name row. skip
    if class_code_tag is None:
        continue

    class_code = class_code_tag.string
    class_name = table_row.find('td', width='532').string
    TECH_CODES.append(ClassRow(class_code, class_name))

with open('./tech_code.csv', 'w', newline='') as out:
    print('Writing data to ' + out.name)
    CSV_FILE = csv.writer(out, delimiter=',')
    CSV_FILE.writerow(['Class Code', 'Class Name'])
    CSV_FILE.writerows(TECH_CODES)

