# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 00:45:52 2020

@author: Group5
"""

from subprocess import Popen, PIPE
import csv

def gitFileDynamics(fileName, kernelRange, repo):
    #第一步：获取需要的记录。
    cmd = ["git", "-P", "log", "--stat","--oneline","--follow", kernelRange, fileName]#定义需要执行的git命令。
    p = Popen(cmd, cwd=repo, stdout=PIPE)#实例化带管道的Popen对象以便传输数据。
    data, res = p.communicate()#获取记录，数据类型为“bytes"(字节字符串)。
    txt = data.decode("utf-8").split("\n")  #将获取的字节字符串解码为文本字符串（str），并按照换行符（\n)分割元素创建列表。
    
    #第二步：写入csv文件。
    csv_file = open('record.csv','w',newline='')#创建csv文件。
    writer = csv.writer(csv_file)#实例化writer对象以便使用writerow方法写入数据。
    for i in range(int((len(txt)-1)/3)):  #遍历txt列表。
        s1 = txt[3*i].split(' ')#提取第一行数据。
        s2 = txt[3*i+1].split(' ')#提取第二行数据。
        s3 = txt[3*i+2].split(' ')#提取第三行数据。
        list_ = [i+1, s1[0], ' '.join(s1[1:]), s2[1], s3[4]]#将数据组合到一起并加上序号。
        print(list_)
        writer.writerow(list_)#写入csv文件。
    csv_file.close()#关闭csv文件。
    
gitFileDynamics("kernel/sched/core.c", "v3.4..v3.6", "D:\Source\linux")#运行该函数并传入参数。