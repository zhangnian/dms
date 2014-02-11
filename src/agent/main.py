#!/usr/bin/python
# -*- coding: utf-8 -*-
# 

import net
import collect
import daemon
import time
import os
import sys


''' 数据采集任务守护进程 '''
class CollectDaemon(daemon.Daemon):
    def _run(self):
    	collector = collect.Collect()
    	data_sender = net.DataSender()
    	data_sender.connect("tcp://127.0.0.1:8899")

        while True:
        	#每隔一段时间将数据上报
            time.sleep(3)
            data_sender.send_data(collector.loadavg2json())

        data_sender.close()


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


		
