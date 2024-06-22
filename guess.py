import numpy as np
from scipy import stats

# 给定的数据
num = {2021: 593, 2022: 591, 2023: 612}#请注意 此处不限制填写的内容 但我仍然建议填写排名 格式年份:分数/排名
wantYear = 2024#填写希望预测的年份

# 提取自变量和因变量
years = np.array(list(num.keys()))
scores = np.array(list(num.values()))

# 计算相关系数
r = np.corrcoef(years, scores)[0, 1]

# 执行一元线性回归
slope, intercept, r_value, p_value, std_err = stats.linregress(years, scores)

# 输出结果
print("样本相关系数 r =", r)
print("一元线性方程：y =", slope, "x +", intercept)

# 预测数据
wantScore = slope * wantYear + intercept
print("预测", wantYear, "年的分数为：", wantScore)
