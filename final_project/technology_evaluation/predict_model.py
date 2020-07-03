#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Model Evaluation: F Test"""

__author__ = "ZhangQiyuan"
__copyright__ = "Copyright2020,Group05 Final_Project"
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = ["ZhangQiyuan", "YanHaoqiu"]

import numpy as np
import pandas as pd
from scipy.stats import f


def f_evaluation(samples, y_true, y_predict):
    """Model Evaluation: F Test
    1. Make decision rule: calculate critical values
    2. Test statistics: calculate f-test"""
    mean_y = y_true.mean()
    ESS = np.sum((y_true - y_predict) ** 2)
    RSS = np.sum((y_true - mean_y) ** 2)
    # TSS = np.sum((y_true - mean_y) ** 2)
    p = 7  # number of predictors
    n = samples  # number of samples
    f_test = (RSS / p) / (ESS / (n - p - 1))
    print(f"{y_predict.name}'s F-test: {f_test} ")
    # Two tailed test and calculate critical value
    F_throry_left = f.ppf(q=0.025, dfn=p, dfd=n - p - 1)
    F_throry_right = f.ppf(q=0.975, dfn=p, dfd=n - p - 1)
    print(f"{y_predict.name}'s left critical value: {F_throry_left} ")
    print(f"{y_predict.name}'s right critical value: {F_throry_right} ")


if __name__ == '__main__':
    csv_data = pd.read_csv('predict(1).csv')
    df = pd.DataFrame(csv_data)
    df.columns = ['lines', 'authors', 'shas','the_first_time','the_last_time',
                  'average_time','total_shas','true_y','linear_y','tree_y']
    x1 = df['lines']
    y1 = df['y1']
    yl = df['yl']
    yd = df['yd']
    samples = len(df['lines'])  # calculate the number of samples
    # Test of Linear Model
    f_evaluation(samples, df['true_y'], df['linear_y'])
    # Test of Decision Tree
    f_evaluation(samples, df['true_y'], df['tree_y'])
