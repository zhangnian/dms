#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import sys

import net
import collect
import config

import log

log.set_logger(limit = 1024)
log.set_logger(level = 'DEBUG')

''' 数据采集任务守护进程 '''
class CollectTask:

    def upload(self):

    	log.info("数据采集任务守护进程启动")

    	obj = config.Config()
    	obj.load_config()
        log.info("加载配置完成")

    	collector = collect.Collect()
    	data_sender = net.DataSender()
        log.info("开始连接")
    	data_sender.connect("tcp://127.0.0.1:8899")
        log.info("连接成功")     

	while True:
            time.sleep(3)
        	#每隔一段时间将数据上报
            if 1 == obj.collect_mem_info:
            	data_sender.send_data(collector.meminfo2json())

            if 1 == obj.collect_disk_info:
            	data_sender.send_data(collector.diskinfo2json())

            if 1 == obj.collect_process_info:
            	data_sender.send_data(collector.processinfo2json())

            if 1 == obj.collect_loadavg:
            	data_sender.send_data(collector.loadavg2json())

        data_sender.close()

        log.info("数据采集任务守护进程停止")

#程序入口
if __name__ == "__main__":
    task = CollectTask()
    task.upload()


		
