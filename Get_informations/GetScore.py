import os
import json
import Get_informations.Getpage as Getpage

def getScore(schoolId, provinceId, year):
    #检查并创建本地目录
    directory = f"./schools/{provinceId}/{year}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    #从本地获取学校信息
    file_path = f"{directory}/{schoolId}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            return json.load(file)

    #实话实说，这里的逻辑我也真看不懂了。。。 等gpt解释吧
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