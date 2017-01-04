# Flask CMDB

* [安装指南](#安装指南)
* [结构与功能](#结构与功能)
* [项目截图](#项目截图)


## 安装指南:
* 需要python2.7环境
* 需要模块，查看requestment.txt
* 初始化数据
* 数据库sql/reboot10.sql

### MYSQL数据库导入
```
mysql -uroot -p123456 -e 'create database reboot10'
mysql -uroot -p123456 reboot10 < sql/reboot10.sql
```
### MYSQL数据库字符集设置
```
[client]
default-character-set=utf8

[mysqld]
character-set-server=utf8
collation-server=utf8_general_ci
```

### 登录用户名和密码
* 用户: test
* 密码: 123123

## 结构与功能
* 仪表盘 
  * 欢迎界面
* 用户管理
  * 个人用户信息
    * 显示当前登录用户的个人信息 
  * 所有用户信息
    * 显示所有用户信息(只管理员可见)
* 资产管理
  * 服务器管理
    * 服务器信息
  * 机柜管理
    * 机柜信息
  * 机房管理
    * 机房信息  
* 值班系统
  * 当前值班人
    * 当前值班人个人信息
  * 值班列表
    * 本周值班人信息列表
* 工单管理
  * 工单申请
    * 显示申请界面
  * 工单申请列表
    * 已申请和待处理工单列表
  * 工单历史列表
    * 处理结束的历史工单列表 
* 代码更新
  * 更新信息
    * 代码更新界面
  * 更新历史
    * 更新成功的历史信息列表
* 设置
* 访问官网

## 项目截图
![sec](https://ooo.0o0.ooo/2016/11/22/5834136d7e85b.png)
![sec](https://ooo.0o0.ooo/2016/11/22/5834136dc8fce.png)
![sec](https://ooo.0o0.ooo/2016/11/22/5834136f8b787.png)
![sec](https://ooo.0o0.ooo/2016/11/22/5834136eda8be.png)
![sec](https://ooo.0o0.ooo/2016/11/22/5834136ed0fe2.png)
![sec](https://ooo.0o0.ooo/2016/11/22/5834137b087e9.png)
![sec](https://ooo.0o0.ooo/2016/11/23/58357428e7523.png)
![sec](https://ooo.0o0.ooo/2016/11/23/583574290c5cd.png)
![sec](https://ooo.0o0.ooo/2016/11/22/5834137ab0be7.png)
![sec](https://ooo.0o0.ooo/2016/11/22/5834137b54126.png)
![sec](https://ooo.0o0.ooo/2016/11/22/5834137bb871b.png)
![sec](https://ooo.0o0.ooo/2016/12/08/5848c98b75376.png)
![sec](https://ooo.0o0.ooo/2016/12/08/5848c98b85e61.png)
