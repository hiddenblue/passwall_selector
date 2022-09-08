# Passwall Selector
passwall自动机场测速并选择最佳节点

## Function:

这个项目针对的就是很多垃圾机场，节点ping测速和真实的带宽上限不匹配的问题
借助平台上另一个<a href="https://github.com/hiddenblue/stairspeedtest-reborn">stairspeedtest</a>项目，可以自动筛选出最佳节点，然后自动修改passwall的配置文件，主要使用了python内置库和shell

<img src="https://user-images.githubusercontent.com/62304226/189033187-b0df172d-feac-4b0f-b02b-b4ad4b75b3bb.png" width=60%>

**这个会把机场不符合你要求的节点自动删除**

<img src="https://user-images.githubusercontent.com/62304226/189033672-c3ebf722-02d4-4961-9440-7cddcc280da1.png" width=60%>

**如图，你可以用crontab把它部署在夜深人静的时候，它可以自动执行，无需操心**


- 筛选最佳节点主要是三个标准：
1. 直接ping的延迟
2. siteping的延迟 主要还是访问google的速度
3. 实际带宽，也就是平均速度，avgspeed

- 修改的参数主要有三项：
1. passwall配置文件的节点列表
2. passwall当前使用的节点
3. 后备节点，默认开启自动切换，备用节点有两个


## Usage:
项目文件主要是三个**两个python脚本，一个shell脚本**

#### auto_proxy.py

这部分的作用是对stair speedtest的机场测速结果`/stairspeedtest/results/xxx.log`进行处理
里面设定了节点筛选的基本指标。

#### edit_proxy_cfg.py

是在openwrt上，利用openwrt自带的uci配置文件管理工具修改/etc/config/passwall配置的核心工具


#### start_speedtest.sh 

是利用expect命令行交互工具和ubuntu、openwrt交互的脚本，主要完成passwall订阅更新，停止运行，运行上述两个脚本，以及后面的恢复工作。





## requirements:
openwrt和用于控制的ubuntu需要安装python3，我使用的是python3.6。

因为对于openwrt这样的精简的嵌入式linux系统而言，python实在太庞大了，所以**这个脚本可能最适用于x86的软路由**，当然我的脚本无需编译，其他平台内存性能足够应该也可以使用

**openwrt**安装python3

`opkg install python3`  //opkg 安装python3

`ln -s /usr/bin/python3.9 /usr/bin`  //建立软链接，类似于快捷方式。 当然这里你可以用`ls /usr/bin/`看一下你opkg安装的python3的版本，不一定是3.9

**ubuntu**安装python3

`apt install python3`  //Debian系 安装python3，Redhat系用yum应该也差不多


##Addition:

写这个纯粹是受不了买的机场速度实在太垃圾了，图个乐呵，各位看官看看就成。写的比较乱，不过可以参考大致的流程自己写一个，坑都被我踩完了。

