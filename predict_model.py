import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import f
csv_data = pd.read_csv('predict_.csv')
df=pd.DataFrame(csv_data)
df.columns=['x1','x2','x3','x4','x5','x6','x7','y1','yl','yi']
x1=df['x1']
x2=df['x2']
x3=df['x3']
x4=df['x4']
x5=df['x5']
x6=df['x6']
x7=df['x7']
y1=df['y1']
yi=df['yi']
mean_y=y1.mean()
ESS= np.sum((y1-yi) **2)
RSS= np.sum((yi-mean_y)**2)
TSS= np.sum((y1-mean_y)**2)
print(ESS)
print(RSS)
print(TSS)
p=7
#多少个自变量维度，有七个x，p=7
n=len(x1)
#多少组数值，csv文件的长度
F = (RSS / p) / (ESS / (n-p-1))
F_throry = f.ppf(q=0.95,dfn=p,dfd=n-p-1)
print(F)
print(F_throry)
#统计量远大于值，拒绝原假设
#F统计量值远远大于F分布的理论值，所以拒绝原假设，认为多元线性回归模型是显著的，所以回归模型的偏回归系数不全为0。




