# -*- coding: utf-8 -*-
"""
Created on Fri May  8 17:24:31 2020

@author: Administrator
"""

from subprocess import Popen, PIPE
from collections import Counter
def gitFileDynamics(repo):
    #第一步：获取需要的记录。
    cmd = 'git log --no-merges --pretty=format:"%h, %an"'#git log --no-merges --pretty=format:"%h, %an"
    p = Popen(cmd, cwd=repo, stdout=PIPE)#实例化带管道的Popen对象以便传输数据。
    data, res = p.communicate()#获取记录，数据类型为“bytes"(字节字符串)。
    txt = data.decode('latin').encode('utf8').decode('utf8').split("\n")  #将获取的字节字符串解码为文本字符串（str），并按照换行符（\n)分割元素创建列表。
    print(txt)
    dir1 = {}
    lis=[]
    dir={}
    for i in txt:
        lis.append(i[14:])
    #print(lis)
    result={}
    for i in set(lis):
        result[i] = lis.count(i)
    print(result)
    #dir中的key：value为人名：出现次数
    #for i in txt:
     #   if i[14:] in dir:
      #      dir[i[14:]]+=1 #字典中有对应的key就把value+1
       # else:
        #    dir[i[14:]]=1 #字典中没有就新建一个，让他值为1
    #print(dir["Hans de Goede"])
gitFileDynamics("D:\li\linux")#运行该函数并传入参数。