#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract sha, author,time_str from one file.
   The file is got from git blame linux-stable/kernel/sched/core.c > coreb.csv"""


import pandas as pd
import csv


file = 'coreb.csv'
with open(file, 'r') as fp:
    reader = csv.reader(fp)
    rows = [[r[0][:13], r[0][35:62].rstrip(), r[0][62:75]] for r in reader]
df = pd.DataFrame(rows)
df.columns = ['sha', 'author', 'time_str']
df.to_csv('regular_coreb.csv', sep=',', header=True, index=True)
print(df)