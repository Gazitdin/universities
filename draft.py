import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

link = 'https://monitoring.miccedu.ru/?m=vpo'
prefix = 'https://monitoring.miccedu.ru/'

page = requests.get(link)
print(page.status_code)

soup = BeautifulSoup(page.text, 'lxml')

table = soup.find("table", attrs={"id": "tregion"})
row = table.find("a")
region = {"link": prefix + row["href"],
          "name": row.text}
print(region)