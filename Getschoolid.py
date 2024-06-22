import requests
import json
def getschooliid(isCollegeonly):
    all_school_id = {}
    back = requests.get("https://static-data.gaokao.cn/www/2.0/info/linkage.json")
    all_school_ids = ((json.loads(back.text)).get("data")).get("school")
    for i in range(len(all_school_ids)):
        school_id = all_school_ids[i]["school_id"]
        school_name = all_school_ids[i]["name"]
        if ("职业" in school_name or "技术" in school_name or "专科" in school_name) and isCollegeonly:
            continue
        all_school_id[school_name] = school_id
    return all_school_id