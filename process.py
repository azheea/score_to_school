import json
from concurrent.futures import ThreadPoolExecutor
import os
import Get_informations.GetScore as GetScore
import Get_informations.Get_province_id as Get_Province_Id
import Get_informations.Get_school_id as Get_School_Id

# 调用分数获取逻辑
def process(province_id, want, year, thread_num, ethnic_minority,output,rank):
    province_id = str(province_id)  # 确保省份ID为字符串
    is_hugescratch = True  # 是否启用模糊搜索
    path = os.getcwd()  # 获取当前工作目录
    province_id = Get_Province_Id.get_province_id(province_id)  # 获取标准化的省份ID
    all_school_id = Get_School_Id.get_school_ids()  # 获取学校名称与ID的映射
    results = []
    for school_name, school_id in all_school_id.items():
        if "学院" in school_name or "职业" in school_name:
            continue
        try:
            result = []
            all_score = GetScore.getScore(schoolId=school_id, provinceId=province_id, year=year)  # 获取分数数据
            majors = all_score.get("item", [])
            for major in majors:
                # 判断专业名称匹配、专项计划条件，以及排名差值是否在3000以内
                if (want in major["spname"] and 
                    ("专项"in major["spname"] or ethnic_minority == False) and 
                    abs(int(major["min_section"]) - rank) < 3000):
                    result.append({major["spname"]: {"min": major["min"], "min_section": major["min_section"]}})
        except Exception as e:
            print(f"Error processing {school_name}: {e}")
        if result == []:
            continue
        results.append({school_name: result})
    if output:
        # 保存结果到JSON文件
        output_file = f"{path}/{year}_{want}_学校分数排行.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        return f"已将结果保存到 {output_file} ..."
    else:
        return results