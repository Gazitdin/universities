#! /bin/python3
"""this module contains a function for getting a list of links to the pages of
federal districts on the website of the GIVC. The function input is provided
with a list of links to regions and the beginning of the link to the
university
"""

import re
import time
import requests
from bs4 import BeautifulSoup


def get_universities(regions_list,
                     prefix = "https://monitoring.miccedu.ru/iam/2023/_vpo/"):
    """Function collecting links to universities"""
    universities_list = []
    request_logs_list = []

    for item in regions_list:
        link = item['link']
        page = requests.get(link, timeout=10)
        request_status = page.status_code
        current_time = time.strftime("%d.%m.%Y %H:%M:%S")
        request_log = {"link": link,
                       "time": current_time,
                       "request_status": request_status}
        request_logs_list.append(request_log)
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
    result = {"request_logs_list": request_logs_list,
              "universities_list": universities_list}
    return result
