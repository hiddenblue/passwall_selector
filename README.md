# Passwall Selector
自动机场测速并选择最佳节点

### 这个项目针对的就是很多垃圾机场，节点ping测速和真实的带宽上限不匹配的问题

借助平台上另一个stairspeedtest项目，可以自动筛选出最佳节点，然后自动修改passwall的配置文件。

- 筛选最佳节点主要是三个标准：
1. 直接ping的延迟
2. siteping的延迟 主要还是访问google的速度
3. 实际带宽，也就是平均速度，avgspeed

- 修改的参数主要有三项：
1. passwall配置文件的节点列表
2. passwall当前使用的节点
3. 后备节点，默认开启自动切换，备用节点有两个

### 项目文件主要是三个
**两个python脚本，一个shell脚本**
