import requests
import time
def getpage(page:int,schoolId:int,provinceId:int,year:int):
    params = {
        "local_province_id": provinceId,
        "page": page,
        "school_id": schoolId,
        "size": "10",
        "uri": "apidata/api/gk/score/special",
        "year": year,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)"
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }
    # time.sleep(0.3)
    response = requests.get("https://api.zjzw.cn/web/api/", params=params, headers=headers)

    if ("请求过多，请稍后再试" in response.text) == False:
        data = ((response.json()).get("data")).get("item", "none")
    return data