import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import scipy.stats
import random
csv_data=pd.read_csv("data_v4.4.csv")
csv_data1=pd.read_csv('data_v4.9 (1).csv')
csv_data2=pd.read_csv("data_v4.14.csv")
csv_data3=pd.read_csv("data_v4.19.csv")
df=pd.DataFrame(csv_data)
df1=pd.DataFrame(csv_data1)
df2=pd.DataFrame(csv_data2)
df3=pd.DataFrame(csv_data3)
df.columns=['lv','hours','bugs']
df1.columns=['lv','hours','bugs']
df2.columns=['lv','hours','bugs']
df3.columns=['lv','hours','bugs']

hours0=df['hours'].sample(n=100).reset_index(drop=True)
hours1=df1['hours'].sample(n=100).reset_index(drop=True)
hours2=df2['hours'].sample(n=100).reset_index(drop=True)
hours3=df3['hours'].sample(n=100).reset_index(drop=True)

print(hours0)
print(hours1)
print(hours2)
print(hours3)
def JS_divergence(p,q):
    M=(p+q)/2
    return 0.5*scipy.stats.entropy(p, M)+0.5*scipy.stats.entropy(q, M)
#print(JS_divergence(hours0,hours1))
print(JS_divergence(hours0,hours1))
print(JS_divergence(hours0,hours2))
print(JS_divergence(hours0,hours3))
print(JS_divergence(hours1,hours2))
print(JS_divergence(hours1,hours3))
print(JS_divergence(hours2,hours3))
#if the value is closed to 0,the correlation is stronger
# the result shows that four groups of data about time has strong correlation.

