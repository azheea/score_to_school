import os
import json
import sqlite3
import Get_informations.Getpage as Getpage

conn = sqlite3.connect('score.db')
cursor = conn.cursor()

def getScore(schoolId, provinceId, year):
    # 检查表是否存在，如果不存在则创建
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS score_data 
                    (schoolId INTEGER, 
                     provinceId INTEGER,
                     year INTEGER,
                     data TEXT,
                     PRIMARY KEY (schoolId, provinceId, year))''')
    
    # 先从数据库中查询
    cursor.execute('''SELECT data FROM score_data 
                     WHERE schoolId = ? AND provinceId = ? AND year = ?''', 
                     (schoolId, provinceId, year))
    result = cursor.fetchone()
    
    if result:
        # 如果在数据库中找到数据，直接返回
        return json.loads(result[0])
    
    # 从API获取数据
    page = 0
    data = []
    all_data = []
    while len(data) == 10 or page == 0:
        page += 1
        data = Getpage.getpage(page, schoolId, provinceId, year)
        all_data.extend(data)
    all_data = {"item": all_data}
    
    # 保存到数据库
    cursor.execute('''INSERT OR REPLACE INTO score_data 
                    (schoolId, provinceId, year, data) 
                    VALUES (?, ?, ?, ?)''',
                    (schoolId, provinceId, year, json.dumps(all_data)))
    conn.commit()
    
    return all_data