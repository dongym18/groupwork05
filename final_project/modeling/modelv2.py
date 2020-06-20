# -*- coding: utf-8 -*-
__author__="Yuming Dong 320180939701"
__copyright__="Copyright2020,Group05 Final_Project"
__license__="GPL"
__version__="2.0"
__maintainer__="Yuming Dong 320180939701"
__email__="dongym18@lzu.edu.cn"


import pandas as pd
import numpy as np
from math import log
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import tree

#data_title.csv is for providing titles for each column
df_title = pd.read_csv("dataset_title.csv", header=None)
titles = df_title.iloc[0,:].values
print(titles)

#read csv as df for dataset and apply logarithm
df = pd.read_csv("dataset2.csv", header=None)
df[0] = df[0].apply(log)
df[1] = df[1].apply(log)
df[2] = df[2].apply(log)
df[3] = df[3].apply(log)
df[4] = df[4].apply(log)
df[5] = df[5].apply(log)
df[6] = df[6].apply(log)

#define x and y
x, y = df.iloc[:,:7].values, df.iloc[:,7].values

x = x.astype(np.float)
y = y.astype(np.float)
np.set_printoptions(threshold=np.inf)

#use seaborn to plot picture of each feature versus y value
for i in range(7):
    fig,ax = plt.subplots()
    fig.set_size_inches(12,10)
    img = sns.scatterplot(df[i],df[7])
    plt.title('The scatterplot of column '+titles[i])
    s = img.get_figure()
    s.savefig(titles[i]+'.png')

#get correlation matrix for heatmap
corr = df.corr()
print(df.corr())
fig,ax = plt.subplots()
fig.set_size_inches(12,10)
htpic = sns.heatmap(corr,cmap='BuPu',square=True,annot=True)
ht = htpic.get_figure()
ht.savefig('HeatMap.png')

#get train set and test set
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=1)

#normalize
min_max_scaler = preprocessing.MinMaxScaler()
x_train=min_max_scaler.fit_transform(x_train)
x_test=min_max_scaler.fit_transform(x_test)
y_train=min_max_scaler.fit_transform(y_train.reshape(-1,1))
y_test=min_max_scaler.fit_transform(y_test.reshape(-1,1))

#build model
from sklearn.linear_model import LinearRegression
lr=LinearRegression()
lr.fit(x_train,y_train)
lr_y_predict=lr.predict(x_test)

from sklearn.tree import DecisionTreeRegressor
dtr = DecisionTreeRegressor(criterion="mse",splitter='random',max_depth=21,random_state=27)
dtr.fit(x_train, y_train)
dtr_y_predict = dtr.predict(x_test)

#save the Decisiontree as dot file
with open("RegTree.dot", "w") as f:
    tree.export_graphviz(dtr, out_file = f)

#show the weight
y_importances = dtr.feature_importances_
x_importances = titles
y_pos = np.arange(len(x_importances))

from sklearn.metrics import r2_score
score_dtr = r2_score(y_test, dtr_y_predict)
print("r^2 of DecisionTree Regressor：",score_dtr)
print("Weight coeffecients of DecisionTree Regressor：",y_importances)
score_lr = r2_score(y_test, lr_y_predict)
print("r^2 of Multi-Linear Regression：",score_lr)
print("Weight coeffecients of Multi-Linear Regression:",lr.coef_)
print("Constant of Multi-Linear Regression:",lr.intercept_)


