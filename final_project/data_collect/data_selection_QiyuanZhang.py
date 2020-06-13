import pandas as pd
import csv
import time
file = 'coreb.csv'
with open(file, 'r') as fp:
    reader = csv.reader(fp)
    rows = [[r[0][:13], r[0][35:62].rstrip(), r[0][62:81]] for r in reader]
df = pd.DataFrame(rows)
df.columns = ['sha', 'author', 'time_str']
df.to_csv('regular_coreb.csv', sep=',', header=True, index=True)
print(df)
#作者数目计算
author=df['author']
emptylist=[]
for i in author:
    emptylist.append(i)
emptylist2=[]
for i in emptylist:
    if i not in emptylist2:
        emptylist2.append(i)
print("作者数目为",len(emptylist2))
#提交的commit数量计算
commit_number=df["sha"]
testlist=[]
for i in commit_number:
    testlist.append(i)
testlist2=[]
for i in commit_number:
    if i not in testlist2:
        testlist2.append(i)
print("提交的commit数量为",len(testlist2))
#平均提交的时间点
time_str=df['time_str']
a=0
l3=[]
for i in time_str:
    try:
        value=time.mktime(time.strptime(i,'%Y-%m-%d %H:%M:%S'))
        l3.append(value)
    except:
        pass
    a=a+1
    print(a)
print(len(l3))
print(l3)
average_date=sum(l3)/len(l3)
print("平均时间为",average_date)
l4=sorted(l3)
the_first_time=l4[0]
the_last_time=l4[-1]
print("最早时间为",the_first_time)
print("最晚时间为",the_last_time)










