# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:51:52 2020

@author: group5
version: 1.0
"""

from subprocess import Popen, PIPE
import csv

def Author_occurrence(repo):
    #Get data from git.
    cmd = 'git log --no-merges --pretty=format:"%h, %an"'
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    txt = data.decode('latin').encode('utf8').decode('utf8').split("\n")  
    
    #Put data into dictionary.
    dir0 = {}
    for i in txt:
        dir0.update({i[0:12]:(i[14:],1)})
    
    #Put author occurrences in dictionary.
    dir_count = {}
    for i in txt:
        if i[14:] in dir_count:
            dir_count[i[14:]]+=1 #If there is a corresponding key in the dictionary, value + 1
        else:
            dir_count[i[14:]]=1 #Create a new one if it is not in the dictionary, let count be 1
    
    #Update the value of count in dir0
    for author,count in dir_count.items():
        for sha,author_count0 in dir0.items():
            if author_count0[0] == author:
                dir0[sha] = (author, count) 
                
    #The storage format is:commit, author, total_commit_count_of_that_author
    csv_file = open('author_occurrence.csv','w',newline='',encoding='utf8')
    writer = csv.writer(csv_file)
    for sha,author_count in dir0.items():
        writer.writerow([sha,author_count[0],author_count[1]])
    csv_file.close()  

Author_occurrence("D:\Source\linux")