#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: hjc
@contact:***@**.com
@version: 1.0.0
@license: Apache Licence
@file: sampling.py
@time: 2020/6/13 16:31
"""


import os
import random


filePath = 'C:/Users/40485/Documents/linux-stable'  # 运行时应改为linux-stable在自己电脑里的的绝对路径
m = len(filePath) + 1
samples = []
for root, dirs, files in os.walk(filePath):
    # root是指当前目录路径(文件夹的绝对路径)
    # dirs是指当前路径下所有的子目录(文件夹里的文件夹)
    # files是指当前路径下所有的非目录子文件(文件夹里所有的文件)
    for file in files:
        if os.path.splitext(file)[1] == '.c':       # 只抓取c文件
            sample = os.path.join(root[m:], file)  #
            sample = sample.replace('\\', '/')      # 全部转化为/
            samples.append(sample)
# print(samples)

# 随机抽取n个样本
n = 8000
random_samples = random.sample(samples, n)

with open('samples.txt', 'w') as fs:
    for i in range(n):
        line = str(random_samples[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        line = line.replace("'", '').replace(',', '') + '\n'     # 去除单引号，逗号，每行末尾追加换行符
        fs.write(line)
print("The samples are saved as samples.txt")
