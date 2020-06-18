# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:04:55 2020

@author: Zhang Yuhao
__StudentID__ = 320180940581
__Group__ = 5

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_2 = pd.read_csv('dataset2.csv',index_col=0) #Read csv dataset

#View outliers of fixes_percent
fig,ax = plt.subplots() 
fig.set_size_inches(12,10) #Set the canvas size, the same below
sns.boxplot(data=df_2['fixes_percent'],color='#aaacbf') 
plt.title('Box plot of fixes_percent')

#View the frequency distribution of lines
fig,ax = plt.subplots() 
fig.set_size_inches(12,10) 
sns.distplot(df_2['lines'], bins=100, kde=False) 
plt.title('Histogram of frequency distribution of lines (bins=100)')

#View the frequency distribution of total_shas
fig,ax = plt.subplots() 
fig.set_size_inches(12,10) 
sns.distplot(df_2['total_shas'], bins=10, kde=False)
plt.title('Histogram of total_shas frequency distribution (bins=10)')

#View the proportion of authors
bins = [0, 5, 10, 50, 100, 200]
df_cuts2 = pd.cut(df_2['authors'], bins).value_counts().reset_index().rename(columns={'index':'group','authors':'Frequency'}) #Make frequency distribution table of authors
fig,ax = plt.subplots() 
fig.set_size_inches(12,10) 
plt.pie(x =df_cuts2['Frequency'],
        labels=df_cuts2['group'],
        autopct='%.1f%%', #Keep a decimal
        colors=['#6c80d1','#a795f1','#51aae9','#7dcc90','#bfe39e','#e4db8c','#f4ba7f']
       ) 
plt.title('Pie chart for authors (bins=5)')
plt.show()

#View the relationship between lines and fixes_percent
fig,ax = plt.subplots() 
fig.set_size_inches(12,10) 
sns.scatterplot(df_2['lines'],df_2['fixes_percent'],color='#6c80d1')
plt.title('Scatter plot of lines and fixes_percent')

#View the relationship between authors and fixes_percent
fig,ax = plt.subplots() 
fig.set_size_inches(12,10) 
sns.scatterplot(df_2['authors'],df_2['fixes_percent'],color='#7dcc90')
plt.title('Scatter plot of authors and fixes_percent')

#View the relationship between total_shas and fixes_percent
fig,ax = plt.subplots() 
fig.set_size_inches(12,10) 
sns.scatterplot(df_2['total_shas'],df_2['fixes_percent'],color='#e4db8c')
plt.title('Scatter plot of total_shas and fixes_percent')

#View the correlation coefficient of the data set
corr = df_2.corr()
fig,ax = plt.subplots() 
fig.set_size_inches(12,10) 
sns.heatmap(corr, cmap='BuPu', vmax=1.0,square=True, annot=True)
plt.title('Heat map of the dataset')