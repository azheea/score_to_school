import os
import json
import Getpage

def getScore(schoolId, provinceId, year):
    directory = f"./schools/{year}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = f"{directory}/{schoolId}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            return json.load(file)

    page = 0
    data = []
    all_data = []
    while len(data) == 10 or page == 0:
        page += 1
        data = Getpage.getpage(page, schoolId, provinceId, year)
        all_data.extend(data)
    all_data = {"item": all_data}

    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False)
    return all_data