# FileSync
作业：品高软件大数据实训-大数据怎么存 文件同步器

姓名：何志威

## Update

### 2020.05.21

* :white_check_mark:大概了解了AWS for Python 的 SDK Boto3
* :white_check_mark:学习了如何使用 watchdog 或者 lazydog(Linux) 监控文件系统的事件
* :worried:watchdog 监控文件系统的事件粒度比较小，进行某些操作会触发一系列的事件，修改文件会连续触发两次修改事件
* :black_square_button:考虑将一些无用的事件过滤掉，并且对短时间内出现的重复事件进行合并



