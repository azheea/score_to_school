import json
import process

# 主函数，负责读取配置并调用分数获取逻辑
with open("config.json", encoding="utf-8") as f:
        configs = json.load(f)  # 读取配置文件
        province_id = configs["province_id"]
        want = configs["want"]
        year = configs["year"]
        ethnic_minority = configs["ethnic_minority"]
        output = configs["output"]
        rank = configs["rank"]
    
if __name__ == "__main__":
    print("author 啊这.")
    print("仓库地址:\nhttps://github.com/azheea/score_to_school")
    process.process(province_id, want, year, ethnic_minority,output,rank,output)