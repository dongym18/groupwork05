# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 19:24:12 2020

@author: user
"""

import pandas as pd
import numpy as np
from math import log
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

df_title = pd.read_csv("dataset_title.csv", header=None)
titles = df_title.iloc[0,:].values
print(titles)

df = pd.read_csv("dataset2.csv", header=None)
df[0] = df[0].apply(log)
df[1] = df[1].apply(log)
df[2] = df[2].apply(log)
df[3] = df[3].apply(log)
df[4] = df[4].apply(log)
df[5] = df[5].apply(log)
df[6] = df[6].apply(log)

x, y = df.iloc[:,:7].values, df.iloc[:,7].values

x = x.astype(np.float)
y = y.astype(np.float)
np.set_printoptions(threshold=np.inf)

'''
for i in range(7):
    plt.subplot(4,2,i+1)
    plt.subplots_adjust(wspace=0.1, hspace=0.9)
    plt.scatter(x[:,i],y,s = 20)
    plt.title(titles[i])  
    plt.show
'''

for i in range(7):
    fig,ax = plt.subplots()
    fig.set_size_inches(12,10)
    img = sns.scatterplot(df[i],df[7])
    plt.title('The scatterplot of column '+titles[i])
    s = img.get_figure()
    s.savefig(titles[i]+'.png')
    
corr = df.corr()
print(df.corr())
fig,ax = plt.subplots()
fig.set_size_inches(12,10)
htpic = sns.heatmap(corr,cmap='BuPu',square=True,annot=True)
ht = htpic.get_figure()
ht.savefig('HeatMap.png')

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)

'''
test_csv = open('predict.csv', 'w', newline='',encoding = 'utf8')
writer = csv.writer(test_csv)
for i in x_test:
    writer.writerow(i)
test_csv.close()
'''

'''
ty = pd.DataFrame(y_test)
ty.to_csv('predicty.csv')
'''

min_max_scaler = preprocessing.MinMaxScaler()
x_train=min_max_scaler.fit_transform(x_train)
x_test=min_max_scaler.fit_transform(x_test)
y_train=min_max_scaler.fit_transform(y_train.reshape(-1,1))
y_test=min_max_scaler.fit_transform(y_test.reshape(-1,1))

from sklearn.linear_model import LinearRegression
lr=LinearRegression()

lr.fit(x_train,y_train)

lr_y_predict=lr.predict(x_test)

'''
ty = pd.DataFrame(lr_y_predict)
ty.to_csv('predictlr.csv')
'''

from sklearn.tree import DecisionTreeRegressor
dtr = DecisionTreeRegressor(criterion="mse",splitter='random',max_depth=21,random_state=27)
dtr.fit(x_train, y_train)
dtr_y_predict = dtr.predict(x_test)

y_importances = dtr.feature_importances_
x_importances = titles
y_pos = np.arange(len(x_importances))

from sklearn.metrics import r2_score
score_dtr = r2_score(y_test, dtr_y_predict)
print("回归决策树的r^2值：",score_dtr)
print("回归决策树的各项权重：",y_importances)
score_lr = r2_score(y_test, lr_y_predict)
print("线性回归的r^2值：",score_lr)
print("多元线性回归的各项系数:",lr.coef_)#输出多元线性回归的各项系数
print("多元线性回归的常数项的值:",lr.intercept_)#输出多元线性回归的常数项的值


