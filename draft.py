import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

link = 'https://monitoring.miccedu.ru/?m=vpo'
prefix = 'https://monitoring.miccedu.ru/'

# Get regions list
page = requests.get(link)
result = page.status_code
soup = BeautifulSoup(page.text, 'lxml')
table = soup.find("table", attrs={"id": "tregion"})
row_list = table.find_all("a")
region_list = []
for item in row_list:
    region_temp = {"link"       : prefix + item["href"],
                   "region_name": item.text}
    region_list.append(region_temp)

# Get universities list
region = region_list[0]
link_temp = region["link"]
page_temp = requests.get(link_temp)
result_temp = page_temp.status_code
soup_temp = BeautifulSoup(page_temp.text, "lxml")
table_universities = soup_temp.find("table", attrs={"class": "an"})
row_list_temp = table_universities.find_all("td", attrs={"class": "inst"})

university_list = []
prefix_university = "https://monitoring.miccedu.ru/iam/2023/_vpo/"
for item in row_list_temp:
    temp = item.find("a")
    university_temp = {"id"  : item["id"],
                       "link": prefix_university + temp["href"],
                       "name": temp.text}
    university_list.append(university_temp)

