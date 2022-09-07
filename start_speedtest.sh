#!/bin/bash

# 第一部分脚本的作用，利用expect连接上本地的ubuntu，然后切换到~目录下，执行stairspeedtest
#输出的结果自动放到文件夹下的/results下面，生成一副图和log，用于后续的python脚本分析结果
#在第二部分的expect中，连接openwrt，通过edit_proxy_cfg.py这个模块，获取和修改节点配置信息
#最后uci commit，init.t重载passwall服务
#本脚本作为最主要的，需要在计划任务中配合passwall的节点更新，记得设置好

link="xxxxxx" #在这里面填入你想自动测速选择的订阅链接，默认只能一个机场订阅

group_name="xxxx"  #这里填你想给测速时生成的组名称，无关紧要

# 这里我加一个让openwrt先更新订阅，然后关闭passwall，最后重启passwall
/usr/bin/expect <<-EOF

set timeout 10

spawn ssh root@192.168.1.3

expect {
    "password*" {send "password\n";exp_continue}  #这里填openwrt机器的密码，
    "yes/no*" {send "yes\n"}
}

expect "OpenWrt*"

set timeout 20

send "lua \/usr\/share\/passwall\/subscribe.lua start\n"

expect "null to execute the next command"

send "\/etc\/init.d\/passwall stop\n"

expect "null to execute the next command"

EOF

#第二部分开始测速和数据处理

/usr/bin/expect <<-EOF

set timeout 10

spawn ssh rong@192.168.1.9

expect {
    "password*" {send "password\n";exp_continue}  #这里填用来测速的机器的密码，因为自动测速不能放在openwrt上完成
    "yes/no*" {send "yes\n"}
}

expect "Ubuntu*"

send "cd stairspeedtest\/\n"

send ".\/stairspeedtest\n"

expect "Link:*"

send "$link\n"

expect "Custom Group Name:\n"

set timeout 1800

send "$group_name\n"

expect eof

EOF


cd /home/username   #这里填ubuntu机器的用户名，关键的测速文件auto_proxy以及stairspeed test会在这个目录下

python auto_proxy.py  
# 解析上面获得的results目录下的log文件的脚本
#然后将处理完的文件传给openwrt，进行节点获取和修改

/usr/bin/expect <<-EOF

set timeout 10

spawn ssh root@192.168.1.3

expect {
    "password*" {send "password\n";exp_continue}  #同上面 openwrt密码
    "yes/no*" {send "yes\n"}
}

expect "OpenWrt*"

send "scp username@192.168.1.9:~\/node_result.txt .\n"   #ubuntu用户名

expect {
    "password*" {send "password\n";exp_continue}  #右边的password是ubuntu密码
    "yes/no*" {send "yes\n"}
}

expect "100%*"

set timeout 50

send "python edit_proxy_cfg.py\n"

expect "nothing else"

set timeout 30

send "\/etc\/init.d\/passwall start\n"

expect "nothing else"

EOF

exit





