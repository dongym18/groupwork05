# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:51:52 2020

@author: group5
__version__ = 2.0
"""

from subprocess import Popen, PIPE
from collections import Counter
import csv

def Author_occurrence(repo):
    #Get data from git.
    cmd = 'git log --no-merges --pretty=format:"%h, %an"'
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    txt = data.decode('latin').encode('utf8').decode('utf8').split("\n")  
    
    #The storage format is:commit, author, total_commit_count_of_that_author
    csv_file = open('author_occurrence.csv','w',newline='',encoding='utf8')
    writer = csv.writer(csv_file)  
    author_count = Counter([data[14:] for data in txt])#Get the number of author occurrences through the Counter.
    for data in txt:
        writer.writerow([data[0:12],data[14:],author_count[data[14:]]])   
    csv_file.close()

Author_occurrence("D:\Source\linux")