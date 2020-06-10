作业：品高软件大数据实训

姓名：何志威

## Update

:white_check_mark::完成  :o::困难  :ballot_box_with_check:: 解决方案  :black_square_button::计划​

***

### 2020.06.10

:white_check_mark:完成6月8日课程扩展一

***

### 2020.06.09

:white_check_mark:学习通过PyCharm进行远程开发，训练一个花瓣分类模型

:white_check_mark:学习数据预处理，了解了各种类型数据的处理方式

***

### 2020.06.08

:white_check_mark:学习使用本地Flink的开发环境对接三个Kafka主题数据，使用Flink实时运算数据

:white_check_mark:学习将实时运算的数据发送给机器学习服务，进行智能预测

:white_check_mark:学习使用函数计算服务，体验大数据如何与云计算融合

***

### 2020.06.05

:white_check_mark:完成大数据离线计算大作业

***

### 2020.06.04

:white_check_mark:完成6月2日课程扩展三

***

### 2020.06.03

:white_check_mark:完成6月2日课程扩展一

:white_check_mark:完成6月2日课程扩展二



***

### 2020.06.02

:white_check_mark:学习了如何使用本地Flink程序输出socket消息源内容

:white_check_mark:学习了本地Flink程序中读取Kafka消息

:white_check_mark:学习了如何将S3对象存储数据提价到Kafka

***

### 2020.06.01

:white_check_mark:学习了如何将sql语言和高级编程语言融合

:white_check_mark:学习了在spark上进行多表查询

:white_check_mark:学习了spark和greenplum共享数据

:white_check_mark:学习了如何将数据导入mysql

***

### 2020.05.29

:white_check_mark:完成实操三扩展题

![image-20200529100131898](https://github.com/Hbenmazi/FileSync/blob/master/image/image-20200529100131898.png)

:white_check_mark:完成实操四扩展题

![image-20200529100148405](https://github.com/Hbenmazi/FileSync/blob/master/image/image-20200529100148405.png)

***

### 2020.05.28

:white_check_mark:完成实操二扩展题

![image-20200529100046104](https://github.com/Hbenmazi/FileSync/blob/master/image/image-20200529100046104.png)

***

### 2020.05.27

:white_check_mark:完成实操一扩展题

![image-20200529095953926](https://github.com/Hbenmazi/FileSync/blob/master/image/image-20200529095953926.png)

***

### 2020.05.26

:white_check_mark:修复了一些Bug

:white_check_mark:撰写设计文档 录制演示视频

***

### 2020.05.25

:white_check_mark:学习了S3的文件分块上传的机制

:white_check_mark:学习了S3对象的ETag属性的计算

:white_check_mark:完成了大文件分块上传功能

:white_check_mark:完成断点续传功能

:white_check_mark:完成UI与逻辑层结合

:o:对于文本文件的保存操作，即使没有修改文件内容，也会触发一次文件修改事件（修改时间改变了），导致重复上传

* :ballot_box_with_check:上传之前先检查S3中该文件的ETag，如果与本地计算出的相同，则不再上传

:o:创建大文件时会触发两次文件修改事件，首先是元数据的修改，其次是文件内容的修改。由于文件较大，这两次修改事件之间会隔一段比较长的时间，因而无法通过时间间隔以聚合两个事件。

* :ballot_box_with_check:第一个事件触发时，先循环至获取该文件的读取权限再上传。第二个事件触发时通过检验ETag避免重复上传。

***

### 2020.05.22

:white_check_mark:完成了上传/删除文件功能

:white_check_mark:完成了创建、删除和修改事件的处理

:white_check_mark:用PyQt5设计了简单的GUI界面  



:o:由于S3没有文件夹的概念，所以当本地创建一个空文件夹时没有相应的API调用

* :ballot_box_with_check:上传一个空的对象，并将它的key命名为文件夹的名字且以"/"结尾

:o:由于WindowsAPI的限制，无法判断删除事件的主体是文件夹还是文件，而且当文件夹被删除时，只会触发一个删除事件，不会递归地触发该目录下其它文件的删除事件。

* :ballot_box_with_check:将文件夹和文件的删除事件统一处理：先获取删除的路径，在获取S3上所有以该路径为前缀的Object，然后统一删除  

  

:black_square_button:完善GUI的设计

:black_square_button:开始实现分块上传/下载功能



***

### 2020.05.21

:white_check_mark:大概了解了AWS for Python 的 SDK Boto3

:white_check_mark:学习了如何使用 watchdog 或者 lazydog(Linux) 监控文件系统的事件

:o:watchdog 监控文件系统的事件粒度比较小，进行某些操作会触发一系列的事件，修改文件会连续触发两次修改事件

:black_square_button:考虑将一些无用的事件过滤掉，并且对短时间内出现的重复事件进行合并



