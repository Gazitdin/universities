#! /bin/python3
"""This module contains a functions for getting a list of parameters of
univerisy from the pages of university on the website of the GIVC.
"""

import requests
from bs4 import BeautifulSoup


def get_info(link):
    """Function to collect base information about unoversity"""
    page = requests.get(link, timeout=10)
    soup = BeautifulSoup(page.text, "lxml")
    info_table = soup.find("table", attrs={"id":"info"})
    region = info_table.find_all("a")[0].text
    type_check = info_table.find_all("td", attrs={"colspan": "2"})
    university_type = 'Головная организация' if not type_check else 'Филиал'
    affiliation_table = info_table.find_all("tr")
    for item in affiliation_table:
        temp = item.find_all("td")
        if temp[0].text == 'Ведомственная принадлежность':
            affiliation = temp[1].text
    university_info = {
       "region":region,
       "type":university_type,
       "affiliation":affiliation
       }
    return university_info


def get_parameters (link):
    """Function to collect parameters of universities performance from GIVC"""
    page = requests.get(link, timeout=10)
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
    addition_table = soup.find("table", attrs={"id":"analis_dop"})
    addition_table.thead.clear()
    rows_list = addition_table.find_all("tr")
    i = 0
    for row in rows_list:
        if len(row) != 1:
            cells = row.find_all("td")
            if len(cells) == 4:
                indicator_number = cells[0].text
                indicator_name = cells[1].text
                uom = cells[2].text
                indicator_value = cells[3].text
            else:
                i += 1
                indicator_number = "1.1." + str(i)
                indicator_name = cells[0].text
                uom = cells[1].text
                indicator_value = cells[2].text
                indicator_row = {"indicator_number": indicator_number,
                                 "indicator_name": indicator_name,
                                 "uom": uom,
                                 "indicator_value": indicator_value}
            content.append(indicator_row)
    return content
