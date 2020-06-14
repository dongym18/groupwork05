import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
csv_data=pd.read_csv("data_v4.4.csv")
csv_data1=pd.read_csv('data_v4.2.csv')
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
hours=df['hours']
hours1=df1['hours']
hours2=df2['hours']
hours3=df3['hours']
print(len(df))
print(len(df1))
print(len(df2))
print(len(df3))
def JS_divergence(p,q):
    M=(p+q)/2
    return 0.5*scipy.stats.entropy(p, M)+0.5*scipy.stats.entropy(q, M)
print(JS_divergence(hours,hours1))
#print(JS_divergence(hours1,hours2))
#print(JS_divergence(hours2,hours3))


