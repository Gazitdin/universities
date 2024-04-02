#! /bin/python3
"""this module contains a function for getting a list of links to the pages of
federal districts on the website of the GIVC."""

import requests
from bs4 import BeautifulSoup
import re


def get_regions ( link, prefix):
    """Function for getting links to pages with universities links
    on the target site.
    """
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find("table", attrs={"id": "tregion"})
    row_list = table.find_all("a")
    region_list = []

    for item in row_list:
        region_temp = {"link"       : prefix + item["href"],
                       "region_name": item.text}
        region_list.append(region_temp)

    region_list_to_db = []

    for item in region_list:
        region_temp = item
        region_string = re.search('федеральный округ',
                                  region_temp['region_name'])
        if region_string:
            region_list_to_db.append(item)

    return region_list_to_db
