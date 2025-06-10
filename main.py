import json
import process

# 主函数，负责读取配置并调用分数获取逻辑
if __name__ == "__main__":
    with open("config.json", encoding="utf-8") as f:
        configs = json.load(f)  # 读取配置文件
        province_id = configs["province_id"]
        want = configs["want"]
        year = configs["year"]
        thread_num = configs["thread_num"]
        ethnic_minority = configs["ethnic_minority"]
        output = configs["output"]
        rank = configs["rank"]
    print("author 啊这.")
    print("仓库地址:\nhttps://github.com/azheea/score_to_school")

    process.process(province_id, want, year, thread_num, ethnic_minority,output,rank)