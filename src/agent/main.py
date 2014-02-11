#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import sys

import net
import collect
import daemon
import config

import log

log.set_logger(limit = 1024)
log.set_logger(level = 'DEBUG')

''' 数据采集任务守护进程 '''
class CollectDaemon(daemon.Daemon):

    def _run(self):

    	log.info("数据采集任务守护进程启动")

    	obj = config.Config()
    	obj.load_config()

    	collector = collect.Collect()
    	data_sender = net.DataSender()
    	data_sender.connect("tcp://127.0.0.1:8899")

        while True:
        	#每隔一段时间将数据上报
            time.sleep(obj.collect_interval)

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
    daemon = CollectDaemon('/tmp/daemon-collect.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)

        sys.exit(0)

    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)


		
