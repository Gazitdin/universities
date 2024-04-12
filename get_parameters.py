#! /bin/python3
"""this module contains a function for getting a list of parameters of
univerisy from the pages of university on the website of the GIVC.
"""

import re
import requests
from bs4 import BeautifulSoup

TEST_LINK = 'https://monitoring.miccedu.ru/iam/2023/_vpo/inst.php?id=2183'
page = requests.get(TEST_LINK)
soup = BeautifulSoup(page.text, 'lxml')

info = soup.find("table", attrs={"id":"info"})
region = info.find_all("a")[0].text

type_check = info.find_all("td", attrs={"colspan": "2"})

type = 'Головная организация' if not type_check else 'Филиал'

info_content = info.find_all("tr")
for item in info_content:
    temp = item.find_all("td")
    if temp[0].text == 'Ведомственная принадлежность':
      affiliation = temp[1].text

indicator_tables = soup.find_all("table", attrs={"class":"napde"})
table_1 = indicator_tables[1]

print(table_1)