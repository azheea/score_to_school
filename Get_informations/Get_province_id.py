import requests
import json
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