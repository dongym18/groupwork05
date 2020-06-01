# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 00:45:52 2020

@author: Group05
"""
#git diff --numstat HEAD~500..HEAD~499
#git log -p HEAD~500..HEAD~499

from subprocess import Popen, PIPE, DEVNULL
import csv

def GitDiff(HEAD_head, HEAD_end, repo, min_lines, max_lines, min_greater, min_equal):
    commund_list = []

    for i in range(HEAD_head, HEAD_end+1):
        #定义需要执行的git命令。
        head1 = str(i)
        head2 = str(i-1)
        gitdiff = "git diff --numstat HEAD~" + head1 + "..HEAD~" + head2
        gitdiff_list = Popen(gitdiff, cwd=repo, stdout=PIPE, stderr=DEVNULL, shell=True)
        #print(gitdiff)
        data, res = gitdiff_list.communicate()#获取记录，数据类型为“bytes"(字节字符串)。
        #print(data)
        txt1 = data.decode("utf-8").split("\n")
        #txt_ = re.split("\n|\t", txt)
        #print(txt1)
        add_remove = []
        for i in range(len(txt1)-1):
            txt2 = txt1[i].split("\t")
            #print(txt2)
            add_remove.append([int(txt2[0]), int(txt2[1])])
        #print(add_remove)
        
        greater = 0
        equal = 0
        
        if min_lines <= len(add_remove) <= max_lines:
            for i in add_remove:
                if i[0] > i[1]:
                    greater += 1
                elif i[0] == i[1]:
                    equal += 1
                else:
                    continue
        else:
            continue
        
        if greater >= min_greater and equal >= min_equal:
            commund_list.append(gitdiff)
        else:
            continue
        
    print(commund_list)
    #print(len(commund_list))

    with open('gitdiff.txt', 'w') as gd:
        for i in commund_list:
            gd.write(i+"\n")

GitDiff(401, 500, "E:\SourceTree Clone\linux-kernel\linux", 8, 20, 5, 3)#运行该函数并传入参数。