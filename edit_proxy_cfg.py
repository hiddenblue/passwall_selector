import os
import re
import subprocess
import time
# 这个是passwall自动测速切换脚本的第二部分，这部分的主要功能就是读取前面过滤机场测速结果获得的node_result.txt
# 经过eval正则等处理后，只保留最前面的名称（因为在auto_proxy中已经默认按节点最高速度进行排序了；然后用uci 工具提取出
# passwall现有配置文件的node信息，和noderesult信息比对，删掉多余的垃圾节点，最后修改配置，设置好当前tcp udp节点，
# 还有自动切换节点，特别的，udp节点是特地筛选出的site_ping值最低的节点
# 里面调用了很多linux shell的命令，查看前请先了解 uci grep awk 等常用数据处理命令，函数变量命名比较长，通俗易懂

""" 
def get_all_nodeid():  #这场也可以改成用show看到后的隐藏section名字
    os.system("uci show passwall | grep nodes | awk -F '.' '{print $2}' | awk -F '=' '{print $1}' | grep -v global > nodeid.txt")
    print("mission completed") 
    
def read_all_nodeid():
    print(os.getcwd())
    # print(os.path.isfile("nodeid.txt"))
    if os.path.isfile("nodeid.txt"):
        print("目标文件存在，可以继续执行")
    else:
        print("出错，目标文件nodeid.txt不存在")
        exit()
    nodeid_list = []
    with open("nodeid.txt", "r", encoding="utf-8") as nodefile:
        for line in nodefile:
            newline = line.rstrip("\n")
            nodeid_list.append(newline)
    # print(node_able_list)
    return nodeid_list     
""" 
# 这部分代码因为感觉比较冗长而被放弃了，完全不需要通过system的转向中间文件带来的结果，一个subprocess.check_output搞定

# 重构的代码，充分利用linux的命令的简洁性，虽然不一定好维护，返回的nodeid_list是一个处理好的字符串组成的数组，没有多余的东西，完美
#  给我的启示就是尽量减少文件读写次数，可以少很多代码，打开关闭文件很费操作

# 做一个备份，免得哪天手抖配置文件就全没了,顺带建一个文件夹整个时间日志自动命名

todaytime= time.strftime("%Y%m%d")
if os.path.isdir("./pwbackup"):
    print("pwbackup文件夹已存在，无需创建")
else:
    os.mkdir("./pwbackup")
    print("不存在，故创建了pwbackup文件夹")
os.system("cp /etc/config/passwall ./pwbackup/passwall%s"%todaytime)


def get_all_nodeid():
    nodeid_raw=subprocess.check_output("uci show passwall | grep nodes | awk -F '.' '{print $2}' | awk -F '=' '{print $1}' | grep -v global",shell=True).decode("utf-8")
    nodeid_list=nodeid_raw.strip().strip("\n").split("\n")
    return nodeid_list


def get_able_nodes():
    print(os.getcwd())
    # print(os.path.isfile("node_result.txt"))
    if os.path.isfile("node_result.txt"):
        print("目标文件存在，可以继续执行")
    else:
        print("出错，目标文件node_result.txt不存在")
        exit()
    # 打开文件，用eval转化成原来的列表数据类型
    with open("./node_result.txt", "r", encoding="utf-8") as file1:
        f1 = file1.read()
    # content 是auto_proxy得到的优质节点的列表
    content = eval(f1)
    mini_site_ping_index=0
    #这里插入一段获取最小siteping的代码
    #mini_site_ping_index=0  放到全局去定义了，不然后面无法使用
    for i in range(len(content)):
        if content[i][3]<=content[mini_site_ping_index][3]:
            mini_site_ping_index=i

    # print(content)
    for i in range(len(content)):
        content[i]=content[i][0]
    # print(content)
    # print(len(content))
    return content,mini_site_ping_index

raw_node_dict={}
# 这里建立一个简单的字典保存原始的名称，后面设置最快节点是排序时用得上

def del_extra_node():
    find_node = re.compile("'(.+)'")
    s=0
    for nodeid in nodeid_list:
        s=s+1
        nodename=subprocess.check_output("uci show passwall.%s.remarks | awk -F= '{print $2}' "%nodeid,shell=True).decode("utf-8")
        nodename_short=re.search(find_node,nodename)[0][3:-1]
        # 上面用subprocess获得id对应的节点中文名字，用正则匹配得到关键部分，后面开始服套用前面写的代码
        #nodename指的是通过uci获得的节点中文名 nodename_short正则过滤得到的是后面的''中间的内容
        flag=0
        for eight_node in content:
            flag=flag+1
            if eight_node.find(nodename_short)!=-1:
                raw_node_dict[eight_node]=nodeid
                print("匹配成功\n")
                print(eight_node, nodename_short,"\n")
                break
            if flag == len(content):
                # pass
                os.system("uci delete passwall.%s"%nodeid)
    return True

# 写完这三个还剩几个重要的步骤：1.修改当前使用节点，2. 修改备用节点 3.可以照搬之前的整一个备用模块，引入时间命名


#  需要获取可用节点第一个内容然后修改到passwall配置文件，因为并没有当前筛选完的nodeid的列表
def chang_current_node():
    try:
        # 1.修改当前使用节点，这里我后来加了一个udp节点
        os.system("uci set passwall.@global[0].tcp_node=%s" % raw_node_dict[content[0]])
        os.system("uci set passwall.@global[0].udp_node=%s" % raw_node_dict[content[mini_site_ping_index]])
        # 2.修改备用节点
        os.system("uci delete passwall.@auto_switch[0].tcp_node")
        os.system("uci add_list passwall.@auto_switch[0].tcp_node=%s" % raw_node_dict[content[1]])
        os.system("uci add_list passwall.@auto_switch[0].tcp_node=%s" % raw_node_dict[content[2]])
        print("修改节点成功，即将uci commit 保存配置信息，写入文件\n")
        os.system("uci commit passwall")
        print("修改节点成功，写入passwall文件完成，后面将开始init.d 重启passwall\n")

    except:
        print("修改节点失败，请检查")

content,mini_site_ping_index=get_able_nodes()
nodeid_list=get_all_nodeid()
del_extra_node()
chang_current_node()
