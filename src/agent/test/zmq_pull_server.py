import zmq

class zmq_pull_server:

	def __init__(self):
		self.zmq_ctx = zmq.Context()
		self.msg_cnt = 0

	def start(self):
		socket = self.zmq_ctx.socket(zmq.PULL)
		socket.bind("tcp://127.0.0.1:8899")

		while True:
			msg = socket.recv()
			self.msg_cnt = self.msg_cnt + 1
			if 0 == self.msg_cnt % 10000:
				print "msg count: %d" % self.msg_cnt

	def stop(self):
		self.socket.close()


if __name__ == "__main__":
	server = zmq_pull_server()
	server.start()