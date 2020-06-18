# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:04:55 2020

@author: Kang Yunhao
__StudentID__ =320180939851
__Group__ = 5

"""

import pandas as pd

df = pd.read_csv('dataset1.csv',index_col=0) #Read the csv dataset
print('Original dataset:\n',df)
df.info() #View basic information of dataset
#Found missing value in ‘last_fixes’ column
print('--------------------------------------------------------')
dup_c=(df.duplicated()).sum() #Find the number of duplicate values
print('The number of duplicated data: '+str(dup_c)) 
#No duplicate values found
print('--------------------------------------------------------')
isn_c=(df.isnull()).sum() #Find the number of missing values in each column
print('Number of NaN values per column:\n',isn_c)
#Confirm that there are missing values in the ‘last_fixes’ column
print('--------------------------------------------------------')
print('NaN value:\n',df[df.isnull().values]) #View missing values
#After analysis, it was found that the indicator could not be filled and could only be deleted.
#Data in the'fixes_percent' column of 0 can be discarded.
print('--------------------------------------------------------')
df_1 = df.dropna().reset_index(drop=True) #Delete missing values and reset index
print('datasets after deleting NaN values:\n',df_1)
df_1.info() #Review the data set information again
print('--------------------------------------------------------')
print('df_1 data features:\n',df_1.describe()) #View the data characteristics of the data set
#Found that there are several values greater than 100 in the ‘fixes_percen’ column
print('--------------------------------------------------------')
print('Fixes_percent > 100:\n',df_1[df_1['fixes_percent']>100]) #View outliers
print('--------------------------------------------------------')
df_2 = df_1[df_1['fixes_percent']<=100].reset_index(drop=True) #Retain data with the percentage not exceeding 100
print('Data set after cleaning:\n',df_2)
print('--------------------------------------------------------')
print('df_2 data features:\n',df_2.describe()) #Review the data characteristics again
print('--------------------------------------------------------')
print('Data clean has finished.')
df_2.to_csv('dataset2.csv',index=False,sep=',') #Store cleaning results as csv dataset