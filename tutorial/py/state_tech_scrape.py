"""This script scrapes and collates state and territory data
from the USPTO PTMT data site"""

from collections import namedtuple
import csv
import requests
from bs4 import BeautifulSoup

# US state codes; add territory codes here if desired
REGION_CODES = {
    'Alabama' : 'AL',
    'Alaska' : 'AK',
    'Arizona' : 'AZ',
    'Arkansas' : 'AR',
    'California' : 'CA',
    'Colorado' : 'CO',
    'Connecticut' : 'CT',
    'Delaware' : 'DE',
    'District of Columbia' : 'DC',
    'Florida' : 'FL',
    'Georgia' : 'GA',
    'Hawaii' : 'HI',
    'Idaho' : 'ID',
    'Illinois' : 'IL',
    'Indiana' : 'IN',
    'Iowa' : 'IA',
    'Kansas' : 'KS',
    'Kentucky' : 'KY',
    'Louisiana' : 'LA',
    'Maine' : 'ME',
    'Maryland' : 'MD',
    'Massachusetts' : 'MA',
    'Michigan' : 'MI',
    'Minnesota' : 'MN',
    'Mississippi' : 'MS',
    'Missouri' : 'MO',
    'Montana' : 'MT',
    'Nebraska' : 'NE',
    'Nevada' : 'NV',
    'New Hampshire' : 'NH',
    'New Jersey' : 'NJ',
    'New Mexico' : 'NM',
    'New York' : 'NY',
    'North Carolina' : 'NC',
    'North Dakota' : 'ND',
    'Ohio' : 'OH',
    'Oklahoma' : 'OK',
    'Oregon' : 'OR',
    'Pennsylvania' : 'PA',
    'Rhode Island' : 'RI',
    'South Carolina' : 'SC',
    'South Dakota' : 'SD',
    'Tennessee' : 'TN',
    'Texas' : 'TX',
    'Utah' : 'UT',
    'Vermont' : 'VT',
    'Virginia' : 'VA',
    'Washington' : 'WA',
    'West Virginia' : 'WV',
    'Wisconsin' : 'WI',
    'Wyoming' : 'WY'
}

BASE_URL_PREFIX = 'http://www.uspto.gov/web/offices/ac/ido/oeip/taf/stcteca/'
BASE_URL_SUFFIX = 'stcl_gd.htm'

MASTER_LIST = []
StateRow = namedtuple('StateRow', 'state_name tech_code year value')

# for each state code, generate the target URL and pull the data
for state in sorted(REGION_CODES):
    print('Processing data for ' + state)
    path = BASE_URL_PREFIX + REGION_CODES[state].lower() + BASE_URL_SUFFIX
    r = requests.get(path)
    soup = BeautifulSoup(r.text, "html.parser")

    # skip first and last rows, which are headers and totals respectively
    for table_row in soup.find_all('tr')[1:-1]:
        tech_code = table_row.find('td', style=' text-align: left; ').string.strip()
        year = 1963
        # skip the last element, which is a total; we can aggregate the data ourselves
        for value in table_row.find_all('td', {'style': None})[:-1]:
            row = StateRow(state, tech_code, year, value.string.strip())
            MASTER_LIST.append(row)
            year = year + 1

# write out to csv
with open('./state_tech.csv', 'w', newline='') as out:
    print('Writing data to ' + out.name)
    CSV_FILE = csv.writer(out, delimiter=',')
    CSV_FILE.writerow(['Region', 'Tech Class Code', 'Year', 'Utility Patent Count'])
    CSV_FILE.writerows(MASTER_LIST)

