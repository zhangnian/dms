#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import os
import json
import psutil
import datetime

''' 采集系统运行时数据 ''' 
class Collect:

	def __init__(self):
		self.dict_disk_info 	= {}
		self.dict_mem_info		= {}
		self.loadavg 			= {}
		self.process_info_list 	= []


	''' 获取磁盘信息 '''
	def collect_disk_info(self):
	    disk = os.statvfs("/")
	    self.dict_disk_info['available'] = disk.f_bsize * disk.f_bavail
	    self.dict_disk_info['capacity'] = disk.f_bsize * disk.f_blocks
	    self.dict_disk_info['used'] = disk.f_bsize * disk.f_bfree


	''' 获取内存信息 '''
	def collect_mem_info(self):
		f = open("/proc/meminfo")
		lines = f.readlines()
		f.close()

		for line in lines:
			if len(line) < 2:
				continue

			name = line.split(':')[0].rstrip()
			val  = line.split(':')[1].split()[0]

			self.dict_mem_info[name] = long(val) * 1024.0

		self.dict_mem_info['MemUsed'] = self.dict_mem_info['MemTotal'] - self.dict_mem_info['MemFree'] - self.dict_mem_info['Buffers']  - self.dict_mem_info['Cached']


	''' 获取CPU的负载信息 ''' 
	def collect_loadavg(self):
	    f = open("/proc/loadavg")
	    con = f.read().split()
	    f.close()

	    self.loadavg['lavg_1min']	= con[0]
	    self.loadavg['lavg_5min']	= con[1]
	    self.loadavg['lavg_15min']	= con[2]
	    self.loadavg['nr']			= con[3]
	    self.loadavg['last_pid']	= con[4]


	''' 获取进程列表信息 ''' 
	def collect_process_list(self):
	 	pids = psutil.get_pid_list()
	 	if len(pids) < 0:
	 		return

	 	for pid in pids:
	 		#通过pid得到进程信息
	 		each_process = psutil.Process(pid)
	 		proc_info = {}
	 		proc_info["PId"] = each_process.pid
	 		proc_info["PName"] = each_process.name
	 		proc_info["PExe"] = each_process.exe
	 		proc_info["PStatus"] = each_process.status
	 		proc_info["PNice"] = each_process.nice
	 		proc_info["PUserName"] = each_process.username
	 		proc_info["PCreateTime"] = datetime.datetime.fromtimestamp(each_process.create_time).strftime("%Y-%m-%d %H:%M:%S")
	 		proc_info["PNumFds"] = each_process.get_num_fds()
	 		proc_info["PNumThreads"] = each_process.get_num_threads()
	 		proc_info["PCpuPercent"] = each_process.get_cpu_percent()
	 		proc_info["PMemPercent"] = each_process.get_memory_percent()

	 		self.process_info_list.append(proc_info)



	''' 系统数据输出为JSON '''
	def diskinfo2json(self):
		self.collect_disk_info()
		return json.dumps(self.dict_disk_info)


	def meminfo2json(self):
		self.collect_mem_info()
		return json.dumps(self.dict_mem_info)


	def loadavg2json(self):
		self.collect_loadavg()
		return json.dumps(self.loadavg)


	def processinfo2json(self):
		self.collect_process_list()
		dict_cpuinfo = {}

		for proc in self.process_info_list:
			dict_cpuinfo[proc["PId"]] = proc

		return json.dumps(dict_cpuinfo)


if __name__ == "__main__":
	print Collect().processinfo2json()