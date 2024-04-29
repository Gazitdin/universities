#! /bin/python3
"""script for preparing input data for parsing GIVC"""
import json

input_list_2023 = {"year": 2022,
                   "link": 'https://monitoring.miccedu.ru/?m=vpo',
                   "region_prefix": 'https://monitoring.miccedu.ru/',
                   "university_prefix": 'https://monitoring.miccedu.ru/iam/2023/_vpo/'}
input_list_2022 = {"year": 2021,
                   "link": 'https://monitoring.miccedu.ru/?m=vpo&year=2022',
                   "region_prefix": 'https://monitoring.miccedu.ru/',
                   "university_prefix": 'https://monitoring.miccedu.ru/iam/2022/_vpo/'}
input_list_2021 = {"year": 2020,
                   "link": 'https://monitoring.miccedu.ru/?m=vpo&year=2021',
                   "region_prefix": 'https://monitoring.miccedu.ru/',
                   "university_prefix": 'https://monitoring.miccedu.ru/iam/2021/_vpo/'}
input_list_2020 = {"year": 2019,
                   "link": 'https://monitoring.miccedu.ru/?m=vpo&year=2020',
                   "region_prefix": 'https://monitoring.miccedu.ru/',
                   "university_prefix": 'https://monitoring.miccedu.ru/iam/2020/_vpo/'}
input_list_2019 = {"year": 2018,
                   "link": 'https://monitoring.miccedu.ru/?m=vpo&year=2019',
                   "region_prefix": 'https://monitoring.miccedu.ru/',
                   "university_prefix": 'https://monitoring.miccedu.ru/iam/2019/_vpo/'}
input_list_2018 = {"year": 2017,
                   "link": 'https://monitoring.miccedu.ru/?m=vpo&year=2018',
                   "region_prefix": 'https://monitoring.miccedu.ru/',
                   "university_prefix": 'https://monitoring.miccedu.ru/iam/2018/_vpo/'}
input_list_2017 = {"year": 2016,
                   "link": 'https://monitoring.miccedu.ru/?m=vpo&year=2017',
                   "region_prefix": 'https://monitoring.miccedu.ru/',
                   "university_prefix": 'https://monitoring.miccedu.ru/iam/2017/_vpo/'}

monitorings_list = []
inputs_list = [input_list_2023, input_list_2022, input_list_2021,
               input_list_2020, input_list_2019, input_list_2018,
               input_list_2017]
names_list = ["monitoring_2023", "monitoring_2022", "monitoring_2021",
              "monitoring_2020", "monitoring_2019", "monitoring_2018",
              "monitoring_2017"]

for name in names_list:
    position = names_list.index(name)
    input_to_list = inputs_list[position]
    row_to_list = {"monitoring": name,
                   "input_data": input_to_list}
    monitorings_list.append(row_to_list)

with open('parsing_input.json', 'w', encoding="utf-8") as file:
    json.dump(monitorings_list, file)
