#! /bin/python3
"""this module contains a function for getting a list of links to the pages of
federal districts on the website of the GIVC. The function input is provided
with a list of links to regions and the beginning of the link to the
university
"""

import re
import requests
from bs4 import BeautifulSoup


def get_universities(regions_list,
                     prefix = "https://monitoring.miccedu.ru/iam/2023/_vpo/"):
    """Function collecting links to universities"""
    universities_list = []
    for item in regions_list:
        link = item['link']
        page = requests.get(link, timeout=10)
        soup = BeautifulSoup(page.text, "lxml")
        table = soup.find("table", attrs={"class": "an"})
        rows = table.find_all("td", attrs={"class": "inst"})
        for row in rows:
            tmp = row.find("a")
            link_tmp = tmp["href"]
            university_id = re.search(r'id=\d+', link_tmp)
            university_id = re.sub('id=', '', university_id.group(0))
            university_name = tmp.text
            university_link = prefix + tmp["href"]
            university = {
                'university_id': university_id,
                'link': university_link,
                'university_name' : university_name
                }
            universities_list.append(university)
    return universities_list
