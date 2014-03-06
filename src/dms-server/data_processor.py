# -*- coding:utf-8 -*-

import zmq
import threading
import Queue
import json

''' 工作线程，每个线程都有一个私有的任务队列 ''' 
class WorkerThread(threading.Thread):
    def __init__(self, id):
        self.id = id
        self.task_queue = Queue.Queue(maxsize = 100)
        threading.Thread.__init__(self)
        
    def put_task(self, data):
        self.task_queue.put(data)
        
        
    def run(self):
        while True:
            data = self.task_queue.get()
            self.proccess(data)
        
    def proccess(self, data):
        print '线程%d处理数据：%s' % (self.id, data)
        if self.id == 0:
            self.process_loadavg(data)
        
    def process_loadavg(self, data):
        print data

    def proccess_cpu(self, data):
        pass
    
    def proccess_mem(self, data):
        pass
        
    def proccess_disk(self, data):
        pass

class data_processor:
        def __init__(self):
            self.zmq_ctx = zmq.Context()
            self.worker_thread = []
            self.task2thr = { 0 : "loadavg", 1: "mem", 2 : "disk", 3 : "others" }

        def start(self):
            # 创建工作线程
            for i in range(0, 4):
                worker_thr = WorkerThread(i)
                self.worker_thread.append(worker_thr)
            
            # 启动工作线程
            for thr in self.worker_thread:
                thr.start()
            
            print '启动工作线程池成功'
            
            self.pull_socket = self.zmq_ctx.socket(zmq.PULL)
            self.pull_socket.bind("tcp://127.0.0.1:9988")

            while True:
                data = self.pull_socket.recv()
                if len(data) <= 0:
                    continue
                
                dict_data = json.loads(data)
                for key in dict_data.keys():
                    for thr in self.task2thr:
                        if key == self.task2thr[thr]:
                            pos = int(thr)
                            
                self.worker_thread[pos].put_task(data)  
            
                
        def stop(self):
            self.pull_socket.close()
            self.zmq_ctx.term()


if __name__ == '__main__':
        processor = data_processor()
        processor.start()
