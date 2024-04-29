#! /bin/python3
"""
Script for collecting data on the work of universities in Russia
"""

import json
import time
import sqlite3
import random
import requests
from get_regions import get_regions
from get_universities import get_universities
from get_parameters import get_parameters

connection = sqlite3.Connection("universities_performance.db")
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS universities (
university_id INTEGER PRIMARY KEY,
givc_id INTEGER NOT NULL,
university_name TEXT NOT NULL,
region TEXT NOT NULL,
type TEXT NOT NULL,
affiliation TEXT NOT NULL
)
''')
connection.commit()
cursor.execute('''
CREATE TABLE IF NOT EXISTS performance (
measurement_id INTEGER PRIMARY KEY,
givc_id INTEGER NOT NULL,
data_year INTEGER NOT NULL,
indicator_number TEXT NOT NULL,
indicator_name TEXT NOT NULL,
uom TEXT NOT NULL,
indicator_value TEXT NOT NULL,
FOREIGN KEY (givc_id) REFERENCES universities (givc_id)
)
''')
connection.commit()
connection.close()

with open('parsing_input.json', 'r', encoding="utf-8") as file:
    monitorings_list = json.load(file)

log = []

for monitoring in monitorings_list:
    print(f"{monitoring['monitoring']} in progress")

    input_data = monitoring["input_data"]
    year = input_data["year"]
    monitoring_link = input_data["link"]
    region_prefix = input_data["region_prefix"]
    university_prefix = input_data["university_prefix"]

    regions_list_file_name = ('regions_list_' + monitoring['monitoring'] +
                              '.json')
    temp_regions = get_regions(monitoring_link, region_prefix)
    with open(regions_list_file_name, 'w', encoding="utf-8") as file:
        json.dump(temp_regions["regions_list"], file)
    log.append(temp_regions["request_log"])

    universities_list_file_name = ('regions_list_' + monitoring['monitoring'] +
                                  '.json')
    temp_universities = get_universities(temp_regions["regions_list"],
                                         university_prefix)
    with open(universities_list_file_name, 'w', encoding="utf-8") as file:
        json.dump(temp_universities["universities_list"], file)
    temp_request_logs_list = temp_universities["request_logs_list"]
    for request_log in temp_request_logs_list:
        log.append(request_log)

    universities_list = temp_universities["universities_list"]
    for university in universities_list:
        university_id = university["university_id"]
        university_name = university["university_name"]
        university_name = university_name.replace('"', '')
        try:
            university_data = get_parameters(university["link"])
            log.append(university_data["request_log"])
            university_info = university_data["university_info"]
            university_performance = university_data["performance"]
            university_region = university_info["region"]
            university_type = university_info["type"]
            university_affiliation = university_info["affiliation"]
            connection = sqlite3.Connection("universities_performance.db")
            cursor = connection.cursor()
            cursor.execute('''
            INSERT INTO universities (givc_id, university_name,
            region, type, affiliation) VALUES (?, ?, ?, ?, ?)''',
            (university_id, university_name, university_region,
             university_type, university_affiliation))
            connection.commit()
            connection.close()
            for indicator in university_performance:
                indicator_number = indicator["indicator_number"]
                indicator_name = indicator["indicator_name"]
                uom = indicator["uom"]
                indicator_value = indicator["indicator_value"]
                connection = sqlite3.Connection("universities_performance.db")
                cursor = connection.cursor()
                cursor.execute('''
                INSERT INTO performance (givc_id, data_year, indicator_number,
                indicator_name, uom, indicator_value) VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (university_id, year, indicator_number, indicator_name, uom,
                 indicator_value))
                connection.commit()
                connection.close()
            print(f"{university_id}: done")
        except:
            current_time = time.strftime("%d.%m.%Y %H:%M:%S")
            page = requests.get(university["link"], timeout=10)
            request_status = page.status_code
            request_log = {"link": university["link"],
                           "time": current_time,
                           "parsing_status": 'ERROR',
                           "request_status": request_status}
            log.append(request_log)
            print(f"{university_id}: error")

        time.sleep(random.randint(5,15))
    print(f"{monitoring['monitoring']} finished")
    time.sleep(random.randint(5,15))

with open('log_file.json', 'w', encoding="utf-8") as file:
    json.dump(log, file)
