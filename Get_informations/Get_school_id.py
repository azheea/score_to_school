import json
def get_school_ids():
    all_school_id = {}
    with open("schoolid.json", "r", encoding="utf-8") as f:
        all_school_ids = (json.loads(f.read())).get("data").get("school")        
    for school_info in all_school_ids:  # 遍历学校信息列表
        school_id = school_info["school_id"]  # 获取学校ID
        school_name = school_info["name"]  # 获取学校名称
        all_school_id[school_name] = school_id  # 将学校名称和对应的ID添加到字典中
    return all_school_id  # 返回学校名称和对应的ID字典