import requests
import json
import sys
import openpyxl
import time
from tqdm import tqdm
import threading
from concurrent.futures import ThreadPoolExecutor
import os
import GetScore

# author 啊这.
# buy me a coffie https://v我50.啊这.site

# --------------------------------------
province_id = 52  # 填写对应地区的id 贵州的为52 不清楚请填写省份全名(会浪费一点时间遍历)
want = "生物科学"  # 请填写所选专业
year = 2024  # 此处填写所需获取的年份
is_hugescratch = True  # 是否模糊搜索 即包含专业关键词就收入
is_college_only = True  # 仅保留大学
thread_num = 2  # 线程数量限制 防止过快导致出问题
# --------------------------------------

path = os.getcwd()  # 获取当前工作目录的路径
province_id = str(province_id)  # 将province_id转换为字符串类型

def get_province_id(province_id):
    if not province_id.isdigit() or province_id == "None":  # 如果province_id不是数字或为字符串"None"
        if province_id == "None":  # 如果province_id为字符串"None"
            province_id = input("请输入省份名称:")  # 提示用户输入省份名称
        print("检测到您未获取您省份的id,正在为你获取")
        back = requests.get("https://static-data.gaokao.cn/www/2.0/config/81004.json")  # 发送GET请求获取省份信息
        all_province = json.loads(back.text)  # 将返回的JSON数据解析为字典

        for key, value in all_province['data'].items():  # 遍历省份信息字典
            if value['provinceName'] == province_id:  # 如果省份名称与输入的省份名称相同
                id = key  # 获取省份ID
                break

        if province_id:  # 如果输入的省份名称不为空
            print(f"{province_id}的ID为:{id}")  # 打印省份名称和对应的ID
            province_id = id  # 将province_id更新为对应的ID
        else:
            print("找不到该省份的ID")  # 打印找不到省份ID的提示信息
            sys.exit()  # 退出程序
    return province_id  # 返回province_id

province_id = get_province_id(province_id)  # 获取省份ID

def get_school_ids():
    all_school_id = {}
    with open("schoolid.json", "r", encoding="utf-8") as f:
        all_school_ids = (json.loads(f.read())).get("data").get("school")        
    for school_info in all_school_ids:  # 遍历学校信息列表
        school_id = school_info["school_id"]  # 获取学校ID
        school_name = school_info["name"]  # 获取学校名称
        if ("职业" in school_name or "技术" in school_name or "专科" in school_name) and is_college_only:  # 如果学校名称包含关键词且is_college_only为True
            continue  # 跳过当前循环，继续下一次循环
        all_school_id[school_name] = school_id  # 将学校名称和对应的ID添加到字典中
    return all_school_id  # 返回学校名称和对应的ID字典

all_school_id = get_school_ids()  # 获取学校名称和对应的ID字典

def fetch_score(line, worksheet, all_school_id, province_id, year, want, is_hugescratch):
    school_name = worksheet.cell(row=line + 1, column=4).value  # 获取工作表中指定单元格的值，即学校名称
    school_id = all_school_id.get(school_name)  # 根据学校名称从学校名称和对应的ID字典中获取学校ID
    if school_id:  # 如果学校ID存在
        try:
            worksheet.cell(row=line + 1, column=3).value = school_id  # 将学校ID写入工作表中的指定单元格
            all_score = GetScore.getScore(schoolId=school_id, provinceId=province_id, year=year)  # 调用GetScore模块的getScore函数获取分数信息

            result = {}  # 创建空字典，用于存储结果
            for item in all_score["item"]:  # 遍历分数信息列表
                if (not is_hugescratch and item['spname'] == want) or (is_hugescratch and want in item['spname']):  # 如果不是模糊搜索且专业名称与所选专业相同，或者是模糊搜索且所选专业包含在专业名称中
                    result['spname'] = item['spname']  # 存储专业名称
                    result['min'] = item['min']  # 存储最低分
                    result['min_section'] = item['min_section']  # 存储最低分段
                    break  # 跳出循环 

            if result.get("min") is not None and result.get("min_section") is not None:  # 如果最低分和最低分段存在
                with lock:  # 获取锁
                    worksheet.cell(row=line + 1, column=9).value = result.get("min")  # 将最低分写入工作表中的指定单元格
                    worksheet.cell(row=line + 1, column=10).value = result.get("min_section")  # 将最低分段写入工作表中的指定单元格
                    worksheet.cell(row=line + 1, column=11).value = result.get("spname")  # 将专业名称写入工作表中的指定单元格
                    # print(result)
        except Exception as e:  # 捕获异常并将异常信息存储到变量e中
            error = str(e)  # 将异常信息转换为字符串类型
            errors.append(f"{school_name},{error}")  # 将学校名称和异常信息添加到错误列表中
            

workbook = openpyxl.load_workbook(f'{path}\schools.xlsx')  # 加载Excel文件
worksheet = workbook['Sheet1']  # 获取工作表
total_lines = worksheet.max_row - 1  # 获取工作表中的总行数
lock = threading.Lock()  # 创建锁对象
errors = []  # 创建空列表，用于存储错误信息

with tqdm(total=total_lines, ncols=80, dynamic_ncols=True) as pbar:  # 使用tqdm创建进度条
    with ThreadPoolExecutor(max_workers=thread_num) as executor:  # 创建线程池
        for line in range(total_lines):  # 遍历总行数
            executor.submit(fetch_score, line, worksheet, all_school_id, province_id, year, want, is_hugescratch)  # 提交任务给线程池

    workbook.save(f"{path}\{year}_{want}_学校分数排行.xlsx")  # 保存Excel文件
    print(f"\n工作完成,结果已经输出在{path}\{year}_{want}_学校分数排行.xlsx")  # 打印完成信息及结果文件路径