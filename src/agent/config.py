#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import json

''' 下载系统数据采集的配置 '''
class Config:

	def __init__(self):
		self.collect_cpu_info = 0
		self.collect_process_info = 0
		self.collect_mem_info = 0
		self.collect_disk_info = 0
		self.collect_network_info = 0
		self.collect_loadavg = 0
		self.collect_interval = 3

	def load_config(self):
		try:
			zmq_ctx = zmq.Context()
			socket = zmq_ctx.socket(zmq.REQ)
			socket.connect("tcp://127.0.0.1:9988")
			socket.send("download_config")
			json_config = socket.recv()
			socket.close()

			dict_config = json.loads(json_config)
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


