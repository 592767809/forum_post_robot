
import os
import time
import json


calendar_dict = []
file_path = os.path.dirname(__file__)
for file_name in os.listdir(file_path):
    if file_name.endswith('.json'):
        calendar_dict.append(json.load(open(os.path.join(file_path, file_name), 'r', encoding='utf-8')))
calendar_dict = [each for each in calendar_dict if time.strftime("%Y-%m-%d", time.localtime()) in each['追剧日历'].keys()]


if __name__ == '__main__':
    print(calendar_dict)