#!/bin/bash

# 定时
# 45 20 * * * (/bin/sh /my/python/scrapy/project/tuicool/crontab_task.sh)
# 进入proxyip项目目录
cd /my/python/scrapy/project/tuicool

# 启动爬虫，并指定日志文件，其中nohup....&表示可以在后台执行，不会因为关闭终端而导致程序执行中断。
nohup scrapy crawl hotArticles > tuicool.log 2>&1 &