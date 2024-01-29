import requests
import json
import sys
import openpyxl

#author 啊这.
#buy me a coffie https://v我50.啊这.site

#--------------------------------------
province_id = 52#填写对应地区的id 贵州的为52 不清楚请填写省份全名(会浪费一点时间遍历)
want = "计算机"#请填写所选专业
year = 2022#此处填写所需获取的年份
is_hugescratch = True#是否模糊搜索 即包含专业关键词就收入
is_id_there =  False#是否已经获取了id 如有可关闭 可节省时间 但也可能影响获取结果 目前尚未完成
#--------------------------------------
province_id = str(province_id)
if province_id.isdigit() != True:
    print("检测到您未获取您省份的id,正在为你获取")
    back = requests.get("https://static-data.gaokao.cn/www/2.0/config/81004.json")
    all_province = json.loads(back.text)

    for key, value in all_province['data'].items():
        if value['provinceName'] == province_id:
            id = key
            break

    if province_id:
        print(f"{province_id}的ID为：{id}")
        province_id = id
    else:
        print("找不到该省份的ID")
        sys.exit()

if(is_id_there==False):
    print("开始获取学校id")
    all_school_id ={}
    back = requests.get("https://static-data.gaokao.cn/www/2.0/info/linkage.json")
    all_school_ids = ((json.loads(back.text)).get("data")).get("school")
    for i in range(len(all_school_ids)):
        school_id = all_school_ids[i]["school_id"]
        school_name = all_school_ids[i]["name"]
        if("职业" in school_name or "技术" in school_name or "专科" in school_name):
            continue
        all_school_id[school_name] = school_id


workbook = openpyxl.load_workbook('schools.xlsx')
worksheet = workbook['Sheet1']
line=0
print("开始获取学校对应专业最低分,该过程较慢,请耐心等待")
while True:
    line+=1
    school_name = worksheet.cell(row=line+1,column=3).value
    school_id = all_school_id.get(school_name,None)
    # print(school_name,school_id)
    if(school_id!=None):
        try:
            worksheet.cell(row=line+1,column=2).value = school_id
            back = requests.get(f"https://static-data.gaokao.cn/www/2.0/schoolspecialscore/{school_id}/2022/{province_id}.json")
            all_score = (json.loads(back.text)).get("data")

            result = {}
            for key, value in all_score.items():
                for item in value['item']:
                    if is_hugescratch != True:
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
            # print(result,school_name)
            if(result.get("min") != None and result.get("min_section") != None):
                worksheet.cell(row=line+1,column=8).value = result.get("min")
                worksheet.cell(row=line+1,column=9).value = result.get("min_section")
        except Exception as e:
            print(e)
    else:
        if(school_name != None):
            continue
        else:
            workbook.save(f"{year}_{want}_学校分数排行.xlsx")
            print(f"工作完成,结果已经输出在{year}_{want}_学校分数排行.xlsx")
            break
