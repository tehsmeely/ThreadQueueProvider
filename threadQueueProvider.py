import threading, Queue, random, time

class ThreadQueueProvider(threading.Thread):
	def __init__(self, maxSize=1):
		threading.Thread.__init__(self)
		self.maxSize = maxSize
		self.queue = Queue.Queue(maxsize=self.maxSize)
		self._isRunning = False
		self.flushQueue = True

	def run(self):
		print "Provider: starting"
		self._isRunning = True
		self._initQueue()
		self._loop()

		if self.flushQueue:
			self._flushQueue()
	
	def _initQueue(self):
		#stuff queue full of valid vals so it provides 
		for i in range(self.maxSize):
			try:
				self.queue.put(self.getVal(), False)
			except Queue.Full: #ignore full exception
				print "erroneous FULL on queue init"
				pass

	def _loop(self):
		nextVal = self.getVal()
		while self._isRunning:
			try:
				self.queue.put(nextVal, True, 1)
			except Queue.Full:
				pass
			else:
				nextVal = self.getVal()

	def _flushQueue(self):
		#stuff queue full of empty vals to avoid blocking queue listening on a dead thread
		for i in range(self.maxSize):
			try:
				self.queue.put(0, False)
			except Queue.Full: #ignore full exception
				pass

	def getVal(self):
		rn = random.randint(0, 100)
		print "Provider: genning random number: ", rn
		return rn