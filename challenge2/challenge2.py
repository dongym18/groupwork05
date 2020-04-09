#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Challenge 2: get the difference between PATCHLEVEL and draw it from 2 to 30 bins"""

__license__ = "GPL V2"
__author__ = "Group 05"

# References
# subplot: https://www.cnblogs.com/xiaoboge/p/9683056.html
# plt.hist: https://www.jianshu.com/p/273e28cafe85
# read_csv: https://blog.csdn.net/weixin_39175124/article/details/79434022


import pandas as pd
import matplotlib.pyplot as plt

# read a csv
data_file = r"data_v4.4.csv"
df = pd.read_csv(data_file, comment="#", header=0, index_col="lv")
# add a difference as a column
df.insert(1,'diff',df['hour'] - df['hour'].shift(1).fillna(value=0))
# get diff column
data = df['diff'].values
# mean and variance
data_list = df['diff'].values.tolist()
l = len(data_list)
mean = sum(data_list)/l
diff_square = [(i-mean)**2 for i in data_list]
v = sum(diff_square)/l
print("Mean is {0}, and Variance is {1}".format(mean,v))
# draw subplots which range from 2 to 30 bins
for i in range(1,31):
    plt.subplot(5,6,i)
    plt.hist(data, bins=i+1, density=True, facecolor="blue", edgecolor="black", alpha=0.6)
    plt.xlabel('{} bins'.format(i))
plt.show()
