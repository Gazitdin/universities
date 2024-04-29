
import json
import sqlite3
import time
import random
from get_parameters import get_info, get_parameters



root_links = {"year":2023,
              "root_link":'https://monitoring.miccedu.ru/?m=vpo'}

link = root_links["root_link"]

region_list = get_regions(link)

with open('region_list.json', 'w') as file:
    json.dump(region_list, file)

universities = get_universities(region_list,
                                     'https://monitoring.miccedu.ru/iam/2023/_vpo/')

with open('universities_list.json', 'w') as file:
    json.dump(universities, file)


with open('universities_list.json', 'r') as file:
    universities = json.load(file)

year = 2023
test_list = universities[0:2]
test_log = []
test_to_file = []
for item in test_list:
    item_id = item["university_id"]
    try:
        university_info = get_info(item["link"])
        university_performance = get_parameters(item["link"])
        university = {"id": item["university_id"],
                      "name": item["university_name"],
                      "year": year,
                      "info": university_info,
                      "performance": university_performance}
        test_to_file.append(university)
        print(f"{item_id}: done")
    except:
        request_time = time.localtime()
        request_status = requests.get(item["link"]).status_code
        log = {"university_id": item["university_id"],
               "link": item["link"],
               "time": request_time,
               "status": request_status}
        test_log.append(log)
        print(f"{item[item_id]}: error")
    time.sleep(random.randint(5,15))

connection = sqlite3.Connection("draft.db")
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
connection.close

for item in test_to_file:
    temp_id = item["id"]
    temp_name = item["name"]
    temp_name = temp_name.replace('"', '')
    temp_year = item["year"]
    temp_info = item["info"]
    temp_region = temp_info["region"]
    temp_type = temp_info["type"]
    temp_affiliation = temp_info["affiliation"]
    connection = sqlite3.Connection("draft.db")
    cursor = connection.cursor()
    cursor.execute('''
                   INSERT INTO universities (givc_id, university_name,
                   region, type, affiliation) VALUES (?, ?, ?, ?, ?)''',
                   (temp_id, temp_name, temp_region, temp_type,
                    temp_affiliation)
                   )
    connection.commit()
    connection.close()
    temp_performance = item["performance"]

    for indicator in temp_performance:
        temp_indicator_number = indicator["indicator_number"]
        temp_indicator_name = indicator["indicator_name"]
        temp_uom = indicator["uom"]
        temp_indicator_value = indicator["indicator_value"]
        connection = sqlite3.Connection("draft.db")
        cursor = connection.cursor()
        cursor.execute('''
                       INSERT INTO performance (givc_id, data_year,
                       indicator_number, indicator_name, uom,
                       indicator_value) VALUES (?, ?, ?, ?, ?, ?)''',
                       (temp_id, temp_year, temp_indicator_number,
                        temp_indicator_name, temp_uom, temp_indicator_value)
                        )
        connection.commit()
        connection.close()

connection = sqlite3.connect('draft.db')
cursor = connection.cursor()
cursor.execute('SELECT * FROM universities')
universities = cursor.fetchall()

for university in universities:
    print(university)

cursor.execute('SELECT * FROM performance')
indicators = universities = cursor.fetchall()
for indicator in indicators:
    print(indicator)
