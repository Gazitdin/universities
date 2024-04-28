
import json
from get_parameters import *
from get_regions import *
from get_universities import *

prefix = 'https://monitoring.miccedu.ru/'
prefix_university = "https://monitoring.miccedu.ru/iam/2023/_vpo/"

root_links = {"year":2023,
              "root_link":'https://monitoring.miccedu.ru/?m=vpo'}

link = root_links["root_link"]

region_list = get_regions(link)

with open('region_list.json', 'w') as file:
    json.dump(region_list, file)

with open('region_list.json') as file:
    file_content = file.read()
    region_list = json.loads(file_content)

print(region_list)