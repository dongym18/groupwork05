# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:51:52 2020

@author: Administrator
"""

from subprocess import Popen, PIPE
from collections import Counter
import csv

def Author_currence(repo):
    #第一步：获取需要的记录。
    '''cmd = 'git log --no-merges --pretty=format:"%h, %an"'#git log --no-merges --pretty=format:"%h, %an"
    p = Popen(cmd, cwd=repo, stdout=PIPE)#实例化带管道的Popen对象以便传输数据。
    data, res = p.communicate()#获取记录，数据类型为“bytes"(字节字符串)。
    txt = data.decode('latin').encode('utf8').decode('utf8').split("\n")  #将获取的字节字符串解码为文本字符串（str），并按照换行符（\n)分割元素创建列表。
    #print(txt)'''
    
    txt = ["a55b68e06b59, Ben Skeggs"
,"672007957846, Jeremy Fitzhardinge"
,"a10e9e1dbb39, Ben Skeggs"
,"1a97b4ace09d, Younes Manton"
,"26cfa81357b6, Ben Skeggs"
,"ffe2dee49023, Christoph Bumiller"
,"33dbc27f1ab3, Ben Skeggs"
,"7962fce9a052, Ilya Zykov"
,"a6707f830e39, Colin Cross"
,"2b374956f3af, JP Abgrall"
,"cae9bf11ef0d, Colin Cross"
,"71b2c82bdf67, Arve HjÃ¸nnevÃ¥g"
,"e801e128b220, Bhavesh Parekh"
,"06a1074e1c78, Colin Cross"
,"eb943f6be011, San Mehat"
,"58526090ece3, Christopher Lais"
,"4755b72e2614, San Mehat"
,"4964cd41cd96, San Mehat"
,"3c762a49b120, Arve HjÃ¸nnevÃ¥g"
,"8bfe15f3de0a, Mike Lockwood"
,"16b665543864, Arve HjÃ¸nnevÃ¥g"
,"5249f4883045, Arve HjÃ¸nnevÃ¥g"
,"3537cdaa1620, San Mehat"
,"0445f1548fc6, Arve HjÃ¸nnevÃ¥g"
,"81057ec1ded5, Arve HjÃ¸nnevÃ¥g"
,"fdfc8089429b, San Mehat"
,"f4dc23861d9d, Greg Kroah-Hartman"
,"e59bbb8ea3fb, Greg Kroah-Hartman"
,"c11a166cd4c1, Colin Cross"
,"c1b197ae67a2, Arve HjÃ¸nnevÃ¥g"
,"23687af9317c, Corentin Chary"
,"355b0502f6ef, Greg Kroah-Hartman"
,"c8381c15b14b, Axel Lin"
,"782ee87702fb, Axel Lin"
,"b870defebde4, Jingoo Han"
,"3d461c912462, Sean MacLennan"
,"d37e0208df56, Sean MacLennan"
,"3b28499c5519, Sean MacLennan"
,"ea74fedced82, Sean MacLennan"
,"f1c602f9991c, Sean MacLennan"
,"80c0d83aec52, Sean MacLennan"
,"28998e005bb6, Andreas Ruprecht"
,"c1fcc4c9bd50, Martyn Welch"
,"6d3ff1cc99eb, Andreas Ruprecht"
,"d83fb184945c, Thomas Meyer"
,"201320435d01, Xi Wang"
,"2a58b19fd97c, Xi Wang"
,"fee6433bdd1a, Marcos Paulo de Souza"
,"ca76edebce4a, Marcos Paulo de Souza"
,"f001d7e28c2e, Marcos Paulo de Souza"
,"6318237691e2, Marcos Paulo de Souza"
,"ac31e9e8e67c, Marcos Paulo de Souza"
,"428c1fb50ec5, Marcos Paulo de Souza"
,"9a8f5e07200d, Mark Brown"
,"bf55499e6ee9, Stephen Warren"
,"741e8c2d8177, Axel Lin"
,"b21cb324f141, Axel Lin"
,"341975bf3af8, Jussi Kivilinna"
,"2deed786d993, Jussi Kivilinna"
,"7f4e3e3fa5ba, Jussi Kivilinna"
,"ec2a5466b3ce, stephen hemminger"
,"614c76df1d12, Dmitry Kravkov"
,"5dc5503f5a40, Dan Carpenter"
,"746ae30f821a, Dan Carpenter"
,"7e02e5433e00, Wolfgang Grandegger"
,"b440752d5dc9, Wolfgang Grandegger"
,"c7e963f68888, Robert Marklund"
,"1839a6c6f1eb, Wolfgang Grandegger"
,"e92036a6516d, RongQing.Li"
,"115d2a3de2fd, Wolfgang Grandegger"]
    #创建初始字典
    l1 = []
    csv_file = open('test.csv','w',newline='',encoding='utf8')
    writer = csv.writer(csv_file)
    for i in txt:
        l1.append(i[14:])
    #print(dir0)
    name = Counter(l1)
    #print(name)
    for i in txt:
        writer.writerow([i[0:12],i[14:],name[i[14:]]])
    csv_file.close()


Author_currence("E:\SourceTreeClone\linux-stable\linux-stable")#运行该函数并传入参数。