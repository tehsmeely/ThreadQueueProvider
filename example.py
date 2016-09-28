import threading, Queue, time

from threadQueueProvider import ThreadQueueProvider




class Getter(threading.Thread):
	def __init__(self, provider):
		threading.Thread.__init__(self)
		self.provider = provider
		self._isRunning = False

	def run(self):
		print "Getter: starting"
		self._isRunning = True
		self._loop()

	def _loop(self):
		while self._isRunning:
			time.sleep(5)
			print "Getter: getting val: {}".format(provider.queue.get())



if __name__ == "__main__":
	provider = ThreadQueueProvider(maxSize=5)
	getter = Getter(provider)


	provider.start()
	getter.start()


	while True:
		try:
			inpt = raw_input()
			if inpt == "x":
				break
		except Exception as e:
			print e
			break

	provider._isRunning = False
	getter._isRunning = False