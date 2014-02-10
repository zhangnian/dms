import os
import json


class Collect:

	def __init__(self):
		self.dict_disk_info = {}
		self.dict_mem_info	= {}
		self.loadavg 		= {}

	def collect_disk_info(self):
	    disk = os.statvfs("/")
	    self.dict_disk_info['available'] = disk.f_bsize * disk.f_bavail
	    self.dict_disk_info['capacity'] = disk.f_bsize * disk.f_blocks
	    self.dict_disk_info['used'] = disk.f_bsize * disk.f_bfree


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


	def collect_loadavg(self):
	    f = open("/proc/loadavg")
	    con = f.read().split()
	    f.close()

	    self.loadavg['lavg_1min']	= con[0]
	    self.loadavg['lavg_5min']	= con[1]
	    self.loadavg['lavg_15min']	= con[2]
	    self.loadavg['nr']			= con[3]
	    self.loadavg['last_pid']	= con[4]

	def diskinfo2json(self):
		return json.dumps(self.dict_disk_info)


	def meminfo2json(self):
		return json.dumps(self.dict_mem_info)


	def loadavg2json(self):
		return json.dumps(self.loadavg)


if __name__ == "__main__":
	obj = Collect()
	obj.collect_disk_info()
	obj.collect_mem_info()
	obj.collect_loadavg()

	print obj.diskinfo2json()
	print obj.meminfo2json()
	print obj.loadavg2json()