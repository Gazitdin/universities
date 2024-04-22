#! /bin/python3
"""This module contains a functions for getting a list of parameters of
univerisy from the pages of university on the website of the GIVC.
"""

import re
import requests
from bs4 import BeautifulSoup


def get_info(link):
   """Function to collect base information about unoversity"""
   page = requests.get(link)
   soup = BeautifulSoup(page.text, "lxml")
   info_table = soup.find("table", attrs={"id":"info"})
   region = info_table.find_all("a")[0].text
   type_check = info_table.find_all("td", attrs={"colspan": "2"})
   type = 'Головная организация' if not type_check else 'Филиал'
   affiliation_table = info_table.find_all("tr")
   for item in affiliation_table:
      temp = item.find_all("td")
      if temp[0].text == 'Ведомственная принадлежность':
         affiliation = temp[1].text
   University_info = {
      "region":region,
      "type":type,
      "affiliation":affiliation
      }
   return University_info


def get_parameters (link):
   """Function to collect parameters of universities performance from GIVC"""
   page = requests.get(link)
   soup = BeautifulSoup(page.text, "lxml")
   indicator_tables = soup.find_all("table", attrs={"class":"napde"})
   content = []
   for item in indicator_tables:
      rows_list = item.find_all("tr", attrs={"class":"",})
      for row in rows_list:
         cells_list = row.find_all("td")
         indicator_number = cells_list[0].text
         indicator_name = cells_list[1].text
         uom = cells_list[2].text
         indicator_value = cells_list[3].text
         indicator_row = {"indicator_number": indicator_number,
                          "indicator_name": indicator_name,
                          "uom": uom,
                          "indicator_value": indicator_value}
         content.append(indicator_row)
   addition_table = soup.find_all("table", attrs={"id":"analis_dop"})
   
   return content

TEST_LINK = 'https://monitoring.miccedu.ru/iam/2023/_vpo/inst.php?id=2183'
print(get_parameters(TEST_LINK))

"""

indicator_tables = soup.find_all("table", attrs={"class":"napde"})
table_1 = indicator_tables[1]

table_1 = table_1.find_all("tr", attrs={"class":""})
row1 = table_1[0]
list = row1.find_all("td")
row_to_result=list[0].text
table_of_content = []
for item in list:
   content = item.text
   table_of_content.append(content)
print(table_of_content)





table_of_content = []
for item in 
"""