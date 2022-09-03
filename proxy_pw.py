import os
import re
import time
# 这里的话，需要导入之前测速得到文件  os.path.isfile()返回值是布尔型，false or true

print(os.getcwd())
# print(os.path.isfile("node_result.txt"))
if os.path.isfile("node_result.txt"):
    print("目标文件存在，可以继续执行")
else:
    print("出错，目标文件不存在")
    exit()
# 打开文件，用eval转化成原来的列表数据类型
with open("./node_result.txt", "r", encoding="utf-8") as file1:
    f1 = file1.read()
# content 是auto_proxy得到的优质节点的列表
content = eval(f1)
print(content)
for i in range(len(content)):
    content[i]=content[i][0]
print(content)
print(len(content))

# 这里有个小细节，需要头尾两端的空行才行，实际上应该是回车 注意read readline readlines的区别，一定要区分，一个是每行列表一个是一个长字符串
with open("passwall", "r+", encoding="utf-8") as file2:
    f=file2.read()
    for i in range(len(f)-1,-1,-1):
        # print(f[i],i)
        if f[i] != "\n":
            linemark=i
            break
    f=f[0:i+1]
    file2.write(f)

# 个人感觉先用回车和空格拆分比较好 f2和config是passwall的配置文件
with open("passwall", "r", encoding="utf-8") as file2:
    f2 = file2.read()  # 句柄只能调用一次
    # for line in file2:
    #     print(line)
# print(f2)

# 做一个备份，免得哪天手抖配置文件就全没了,顺序建一个文件夹整个时间日志自动命名
if os.path.isdir("./pwbackup"):
    print("pwbackup文件夹已存在，无需创建")
else:
    os.mkdir("./pwbackup")
    print("不存在，故创建了pwbackup文件夹")
with open("./pwbackup/backup_passwall","w",encoding="utf-8") as file3:
    file3.write(f2)

config=f2.split("\n\n")
for i in range(len(config)):
    config[i]=config[i].split("\n")
print(config,"\n\n\n666")
print(len(config))
# 在这里写好正则匹配的规则
find_node = re.compile("'(.+)'")

s = 0
temp=[]
for i in range(len(config)-3,14,-1):
    print(config[i])
    s=s+1
    print(s)
    # print(config[i][-4])
    print(i, "mark3")
    print(len(config),"mark")
    print(len(config[i]),"mark2")
    print(config[i])
    re_sult=re.search(find_node,config[i][-4]).group(1)[2:]
    # 这里有个steam节点很巧从前往后是不符合规律的，只有从后前-4是合理的
    print(re_sult)
    # 下面用了一个简单的累加统计，当循环执行次数达到上限时，才会把元素添加进去
    flag=0
    for j in content:
        flag=flag+1
        if j.find(re_sult) != -1:
            print("匹配成功\n")
            print(j, re_sult)
            break
        if flag == len(content):
            temp.append(i)

print(temp)
print(len(temp))
for nums in temp:
    config.remove(config[nums])
# print(config)

current_node = config[0][12][18:50]  # 这是从当前使用节点提取的id
print(config[15])
print(config[15][0][14:46])  # 这是默认排序的第一个节点
print(config[16][0][14:46])  # 这是默认排序的第二个节点
print(config[17][0][14:46])  # 这是默认排序的第三个节点 长度为22

print(config[8][7][16:48])  # 第一个备用节点的位置
print(config[8][8][16:48])  # 第二个备用节点的位置
if len(content) > 1:
    config[0][12].replace(config[0][12][18:50], config[15][0][14:46])  # 替换当前节点
    if len(content) > 2:
        config[8][7].replace(config[8][7][16:48], config[16][0][14:46])
        if len(content) > 3:
            config[8][8].replace(config[8][8][16:48], config[17][0][14:46])
    print("节点替换完成\n")
else:
    print("可用节点不足，替换失败\n")

for i in range(len(config)):
    for j in range(len(config[i])):
        print(config[i][j])
    print("\n")

print("----"*20,"\n\n")

# for i in range(len(config)):
#     config[i]=str(config[i])
#     print(type(config[i]))
#     print(config[i])
#     config[i].join("\n")
#     print(config[i])
# config=str(config)
# new_config=config.join("\n")


# print("下面是自动脚本替换过的船新配置")
# print(new_config)


with open("passwall","w",encoding="utf-8") as file4:
    for i in range(len(config)):
        for j in range(len(config[i])):
            file4.write(config[i][j])
            file4.write("\n")
        file4.write("\n")

print("任务执行完成，开心")
