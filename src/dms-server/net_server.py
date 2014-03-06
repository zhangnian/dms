# -*- coding:utf-8 -*-

import zmq

class net_server:
    def __init__(self):
        self.zmq_ctx = zmq.Context()

    def start(self):
        # 创建PULL socket，用于接收上报的监控数据
        self.pull_socket = self.zmq_ctx.socket(zmq.PULL)
        self.pull_socket.bind("tcp://127.0.0.1:8899")
        
        # 创建PUSH socket，用于将监控数据发送给数据分析与处理进程
        self.push_socket = self.zmq_ctx.socket(zmq.PUSH)
        self.push_socket.connect("tcp://127.0.0.1:9988")

        # 创建Poller对象，用于轮询各socket上的事件是否发生
        poller = zmq.Poller()
        poller.register(self.pull_socket, zmq.POLLIN)
        
        while True:
            events = dict(poller.poll())
            data = ""
            if self.pull_socket in events:
                data = self.pull_socket.recv()      # 不会阻塞
                print 'recv: %s' % data
                if len(data) > 0:
                    self.push_socket.send(data)         # 不会阻塞

    def stop(self):
        self.pull_socket.close()
        self.push_socket.close()
        self.zmq_ctx.term()


if __name__ == '__main__':
    srv = net_server()
    srv.start()