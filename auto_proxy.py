import os
import logging
import time
import copy
import re
# 这里引入一个日志模块，输入运行的日志信息，就这么写，先不管能不能用

# 我可以在这个里面限定一些条件，比如Avgping小于50  AvgSpeed要大于25MB，设定变量 googleping也就是SitePing要小于600，当然也可以用下面的中位数方法
# avgping_limit = 50
# avgspeed_limit = 25
# siteping_limit = 600

#  print("程序开始执行，请检查设定的阈值，设定的是平均ping要求小于%dms，平均速度要求大于%dMbps，google站点访问ping为%dms\n"%(avgping_limit,avgspeed_limit,siteping_limit))

logging.basicConfig(
    filename="proxy.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S %p",
    level=10
)
logging.info("logging correct\n")
# print("hello world!")
h1 = logging.FileHandler(filename="proxy.log",encoding="utf-8")
sh = logging.StreamHandler()

# 这里我要实现一个简单的检查本地目录信息，包括results文件夹的存在和找到目标log文件
print(os.getcwd())

if os.path.isdir("stairspeedtest")==True:
    print("目标目录stairspeedtest存在，继续检查stairspeedtest log文件存在\n")
else:
    print("stairspeedtest文件夹不存在，错误，退出")
    exit()
os.chdir("./stairspeedtest/results/")
print(os.getcwd())

# 这里我把字符串列表排一下序，不然容易出错，按扩展名排序。
def last_3(elem):
    return elem[-3:]
dir_list=os.listdir(".")
dir_list.sort(key=last_3)
# print(dir_list)

# 这里学到了反向遍历的方法，从后往前遍历方便删除特定元素
for i in range(len(dir_list)-1,-1,-1):
    if dir_list[i].find("log") == -1:
        dir_list.remove(dir_list[i])

#这里需要加个按前几位排序，方便测试环境
def take_y_m_d(elem):
    return elem[0:8]
dir_list.sort(key=take_y_m_d)

target_file=dir_list[-1]
if target_file.find("log")!=-1:
    print(target_file,"\n","已经找到目标文件\n")
else:
    print("get target directory error exit\n")
    exit()

# 这里可以简单的做一个时间匹配，要求只检索和当天时间相同的结果，太久远的记录不匹配。 开发过程暂时不启用算了
todaytime= time.strftime("%Y%m%d")
if target_file.find(todaytime)!=-1:
    print("VALID TIME! CORRECT!\n")
else:
    print("INVALID TIME! ERROR!\n")
    exit()

# 完成了找到目标文件的功能，后面开始进行测速结果文件的查找和匹配 筛选
# file=open("../results/","r",encoding="UTF-8-sig")
# content=file.read(5)
# print(content)
# 我想使用with open这个方法，感觉比open方便一些

with open(target_file,"r",encoding="utf-8") as f:
    content=f.read()
# print(content)
data_list=content.split("\n\n")

# 这里很奇怪用for i in data_list无法做到分离
for i in range(len(data_list)):
    data_list[i]=data_list[i].split("\n")
# print(data_list)
data_list.remove(data_list[0])
data_list.remove(data_list[-1])
# print(data_list)

# 只保留上述列表的基础数据，其余的都丢了
'''
0 [speed^[大流量]联通→日本dg]
1 AvgPing=40.00
2 AvgSpeed=17.02MB
3 GroupID=0
4 ID=4
5 MaxSpeed=27.37MB
6 Online=true
7 PkLoss=0.00%
8 RawPing=38,36,50,37,37,42
9 RawSitePing=597,606,643,687,639,620,643,715,601,586
10 RawSpeed=0,0,282464,1847960,6362364,6930112,16458046,17046482,31184190,20727160,26330074,31062408,18424742,34994168,21983282,30155760,23708220,18895004,32025384,18876346
11 SitePing=633.70
12 ULSpeed=N/A
13 UsedTraffic=178647083'''

'''[
0'[speed^[主力]移动1→香港gc]',
1 'AvgPing=13.17',
2  'AvgSpeed=49.39MB',
3   'SitePing=306.30'
   ]'''
print(len(data_list))

data=copy.deepcopy(data_list)
for i in range(len(data_list)-1,-1,-1):
    temp=data_list[i][11]
    data_list[i]=data_list[i][0:3]
    data_list[i].append(temp)
    data_list[i][1]
    data_list[i][1]=float(data_list[i][1][8:])
    data_list[i][3] = float(data_list[i][3][9:])
    if data_list[i][2]!="AvgSpeed=N/A":
        data_list[i][2]=float(data_list[i][2][9:-3])
    else:
        data_list.remove(data_list[i])

print(data_list,"\n")
print(len(data_list))
avgping_list=[]
avgspeed_list = []
siteping_list = []
for i in range(len(data_list)-1,-1,-1):

    avgping_list.append(data_list[i][1])

    avgspeed_list.append(data_list[i][2])

    siteping_list.append(data_list[i][3])

avgping_list.sort()
avgspeed_list.sort(reverse=True)

index=[0,1,2]
# 对index的值进行不同的设定，三个参数的权重不同，最低的是直接ping
siteping_list.sort()
index[0]=int((len(data_list)*8)/10)
index[1]=int((len(data_list)*5)/10)
index[2]=int((len(data_list)*4)/10)
print(avgping_list,"\n",avgspeed_list,"\n",siteping_list,"\n",index)

avgping_limit = avgping_list[index[0]]
avgspeed_limit = avgspeed_list[index[1]]
siteping_limit = siteping_list[index[2]]
print("程序开始执行，请检查设定的阈值，设定的是取0.6中位数，平均ping要求小于%dms，平均速度要求大于%dMbps，google站点访问ping小于%dms\n"%(avgping_limit,avgspeed_limit,siteping_limit))

# 下面开始正式的筛选节点
for i in range(len(data_list)-1,-1,-1):
    if data_list[i][1]<avgping_limit and data_list[i][2]>avgspeed_limit and data_list[i][3]<siteping_limit:
        continue
    else:
        data_list.remove(data_list[i])
def takesecond(elem):
    return elem[2]
data_list.sort(key=takesecond,reverse=1)
print("筛选完成")

# 去掉一些不太靠谱的节点，印度节点
for i in range(len(data_list)-1,-1,-1):
    if "印度" in data_list[i][0]:
        data_list.remove(data_list[i])

print("符合设定阈值的节点个数为%d个，分别是\n"%len(data_list))
for i in data_list:
    print(i)

with open("../../node_result.txt","w",encoding="utf-8") as file:
    file.write(str(data_list))
print("结果写入node_result.txt完成")

