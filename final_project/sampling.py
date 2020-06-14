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

# You should change the filepath to the absolute path of the linux-Stable on your own computer.
filePath = 'C:/Users/40485/Documents/linux-stable'
m = len(filePath) + 1
samples = []
for root, dirs, files in os.walk(filePath):
    # 'root' refers to the absolute path to the current directory.
    # 'dirs' refers to all subdirectories under the current path.
    # 'files' refers to all non-directory files in the current path.
    for file in files:
        if os.path.splitext(file)[1] == '.c':       # Only grab C files.
            sample = os.path.join(root[m:], file)
            sample = sample.replace('\\', '/')      # Change \\ to /
            samples.append(sample)
# print(samples)

#  Drawing n samples randomly.
n = 8000
random_samples = random.sample(samples, n)

with open('samples.txt', 'w') as fs:
    for i in range(n):
        line = str(random_samples[i]).replace('[', '').replace(']', '')
        line = line.replace("'", '').replace(',', '') + '\n'
        fs.write(line)
print("The samples are saved as samples.txt")
