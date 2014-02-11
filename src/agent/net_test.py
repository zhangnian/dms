import net

if __name__ == "__main__":
	obj = net.Net()

	obj.connect("tcp://127.0.0.1:8899")

	for i in range(0, 1000000):
		obj.send_msg("hello, world!")
	obj.close()
	print 'send completed.'