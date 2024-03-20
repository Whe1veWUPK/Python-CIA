# 写在前面
这个项目是由五位来自于东南大学的本科生所共同开发
以下是他们的github个人主页:(按字母表顺序)

  [huffb](https://github.com/huffb)$\quad$ [m1zukiL](https://github.com/m1zukiL)$\quad$ [Whe1ve](https://github.com/Whe1veWUPK) $\quad$ [Xavoric](https://github.com/Xavoric) $\quad$ [zywooooo1](https://github.com/zywooooo1)
# 环境配置需求
* [neo4j 数据库](https://neo4j.com/download/) 
* python 3.x 
* 一些需要下载的拓展包: ast, astpretty, py2neo,pyqt等
# 项目简介
* 是一个对Python项目的 ***修改影响分析(Change Impact Analysis)*** 工具
* 100 Percent Python
* 已开发完毕 目前精度达到函数级
# 项目结构介绍
* BackEnd 文件夹存放着所有后端脚本
* FrontEnd 文件夹存放着所有前端脚本
* ForTest 文件夹里是存放着的简单的测试项目
# 使用说明
* 运行FrontEnd 中的 main.py文件 即可运行程序进行后续操作 
* Setting 选项里是你的neo4j数据库地址 以及用户名和密码
* 点击browse 选择你想要分析的python项目根目录
* 点击 graph 构建出项目的 依赖图
* 点击 analyze 部分进行修改影响分析(需先构建出依赖图)


***Good Luck, hope you have a good day***