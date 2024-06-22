import requests
import json
import sys
import openpyxl
import time
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor  # 导入ThreadPoolExecutor
import os
import GetScore
# author 啊这.
# buy me a coffie https://v我50.啊这.site

# --------------------------------------
province_id = 52  # 填写对应地区的id 贵州的为52 不清楚请填写省份全名(会浪费一点时间遍历)
want = "生物"  # 请填写所选专业
year = 2022  # 此处填写所需获取的年份
is_hugescratch = True  # 是否模糊搜索 即包含专业关键词就收入
is_college_only = True  # 仅保留大学
# --------------------------------------


path = os.getcwd()
province_id = str(province_id)
if not province_id.isdigit() or province_id == "None":
    if province_id == "None":
        province_id = input("请输入省份名称:")
    print("检测到您未获取您省份的id,正在为你获取")
    back = requests.get("https://static-data.gaokao.cn/www/2.0/config/81004.json")
    all_province = json.loads(back.text)

    for key, value in all_province['data'].items():
        if value['provinceName'] == province_id:
            id = key
            break

    if province_id:
        print(f"{province_id}的ID为:{id}")
        province_id = id
    else:
        print("找不到该省份的ID")
        sys.exit()

is_id_there = False  # 是否已经获取了id 如有可关闭 可节省时间 但也可能影响获取结果 目前尚未完成
if year == None:
    year = input("请输入要获取的年份:")
if not is_id_there:
    print("开始获取学校id")
    all_school_id = {}
    back = requests.get("https://static-data.gaokao.cn/www/2.0/info/linkage.json")
    all_school_ids = ((json.loads(back.text)).get("data")).get("school")
    for i in range(len(all_school_ids)):
        school_id = all_school_ids[i]["school_id"]
        school_name = all_school_ids[i]["name"]
        if ("职业" in school_name or "技术" in school_name or "专科" in school_name) and is_college_only:
            continue
        all_school_id[school_name] = school_id

if want == None:
    want = input("请输入您想选择的专业:")
workbook = openpyxl.load_workbook(f'{path}\\schools.xlsx')
worksheet = workbook['Sheet1']
line = 0
print("开始获取学校对应专业最低分,首次获取较慢,请耐心等待")
start_time = time.time()
total_lines = worksheet.max_row - 1
lock = threading.Lock()
errors = []
def fetch_score(line):
    school_name = worksheet.cell(row=line + 1, column=4).value
    school_id = all_school_id.get(school_name, None)
    if school_id is not None:
        try:
            worksheet.cell(row=line + 1, column=3).value = school_id
            all_score = GetScore.getScore(schoolId=school_id,provinceId=province_id,year=year)

            result = {}
            for item in all_score["item"]:
                    if not is_hugescratch:
                        if item['spname'] == want:
                            result['spname'] = item['spname']
                            result['min'] = item['min']
                            result['min_section'] = item['min_section']
                            break
                    else:
                        if want in item['spname']:
                            result['spname'] = item['spname']
                            result['min'] = item['min']
                            result['min_section'] = item['min_section']
                            break


            if result.get("min") is not None and result.get("min_section") is not None:
                with lock:
                    worksheet.cell(row=line + 1, column=9).value = result.get("min")
                    worksheet.cell(row=line + 1, column=10).value = result.get("min_section")
                    worksheet.cell(row=line + 1, column=11).value = result.get("spname")
        except Exception as e:
            # print(e)
            errors.append(f"{school_name},{e}")
            pass

with tqdm(total=total_lines, ncols=80, dynamic_ncols=True) as pbar:
    with ThreadPoolExecutor(max_workers=5) as executor:  # 限制最大线程数量为5
        for _ in range(total_lines):
            line += 1
            executor.submit(fetch_score, line)

    workbook.save(f"{path}\{year}_{want}_学校分数排行.xlsx")
    end_time = time.time()
    pbar.update(total_lines)
    pbar.close()
    print(f"\n工作完成,结果已经输出在{path}\{year}_{want}_学校分数排行.xlsx")
    print(f"本次用时: {end_time - start_time}秒")
    if errors:
        print(f"{','.join(errors)}  获取失败")
