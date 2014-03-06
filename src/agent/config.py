#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import json

import log

''' 下载系统数据采集的配置 '''
class Config:

	def __init__(self):
		self.collect_cpu_info = 0
		self.collect_process_info = 0
		self.collect_mem_info = 0
		self.collect_disk_info = 0
		self.collect_network_info = 0
		self.collect_loadavg = 1
		self.collect_interval = 3

		log.set_logger(limit = 1024)
		log.set_logger(level = 'DEBUG')

	def load_config(self):
		try:
			self.collect_interval 		= dict_config["collect_interval"]
			self.collect_cpu_info 		= dict_config["collect_cpu"]
			self.collect_process_info 	= dict_config["collect_process"]
			self.collect_mem_info 		= dict_config["collect_mem"]
			self.collect_disk_info 		= dict_config["collect_disk"]
			self.collect_network_info 	= dict_config["collect_network"]
			self.collect_loadavg 		= dict_config["collect_loadavg"]
		except:
			#出现异常，将配置项设置为默认值
			self.collect_cpu_info 		= 0
			self.collect_process_info 	= 0
			self.collect_mem_info 		= 0
			self.collect_disk_info 		= 0
			self.collect_network_info 	= 0
			self.collect_loadavg 		= 1
			self.collect_interval 		= 3


if __name__ == "__main__":
	Config().load_config()