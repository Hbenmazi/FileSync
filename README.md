# FileSync
作业：品高软件大数据实训-大数据怎么存 文件同步器

姓名：何志威

## Update

:white_check_mark::完成  :o::困难  :ballot_box_with_check:: 解决方案  :black_square_button::计划​

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



