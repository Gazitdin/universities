#! /bin/python3
"""this module contains a function for getting a list of links to the pages of
federal districts on the website of the GIVC. The function input is provided
with a link to the monitoring home page and the beginning of the link to the
region
"""

import re
import time
import requests
from bs4 import BeautifulSoup


def get_regions (link='https://monitoring.miccedu.ru/?m=vpo',
                 prefix='https://monitoring.miccedu.ru/'):
    """Function for getting links to pages with universities links
    on the target site. Link is a link to the monitoring web page for
    a specific year. Prefix - the initial part of the link to the region's
    web page.
    """
    page = requests.get(link, timeout=10)
    request_status = page.status_code
    current_time = time.strftime("%d.%m.%Y %H:%M:%S")
    request_log = {"link": link,
                   "time": current_time,
                   "request_status": request_status}
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find("table", attrs={"id": "tregion"})
    row_list = table.find_all("a")
    region_list = []

    for item in row_list:
        region_temp = {"link": prefix + item["href"],
                       "region_name": item.text}
        region_list.append(region_temp)

    region_list_to_db = []

    for item in region_list:
        region_temp = item
        region_string = re.search('федеральный округ',
                                  region_temp['region_name'])
        if region_string:
            region_list_to_db.append(item)

    result = {"request_log": request_log,
              "regions_list": region_list_to_db}
    return result
