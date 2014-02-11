#!/usr/bin/env python 
# -*- coding: utf-8 -*- 


import zmq


''' 通讯组件 '''
class DataSender:
	def __init__(self):
		self.zmq_ctx = zmq.Context()  

	def connect(self, remote):
		self.socket = self.zmq_ctx.socket(zmq.PUSH)  
		self.socket.connect(remote)

	def send_data(self, msg):
		self.socket.send(msg)

	def close(self):
		self.socket.close()


