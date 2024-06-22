import requests
def getpage(page:int,schoolId:int,provinceId:int,year:int):
    params = {
        "local_province_id": provinceId,
        "page": page,
        "school_id": schoolId,
        "size": "10",
        "uri": "apidata/api/gk/score/special",
        "year": year
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
    }

    response = requests.get("https://api.zjzw.cn/web/api/", params=params, headers=headers)
    if ("访问太过频繁，请稍后再试" in response.text) == False:
        data = ((response.json()).get("data")).get("item", "none")
    return data