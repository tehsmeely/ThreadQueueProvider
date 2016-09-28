import threading, Queue, random, time

class ThreadQueueProvider(threading.Thread):
	def __init__(self, maxSize=1, valueFunction=None):
		threading.Thread.__init__(self)
		self.maxSize = maxSize
		self.queue = Queue.Queue(maxsize=self.maxSize)
		self._isRunning = False
		self.flushQueue = True
		self.queuePushTimeout = 1
		if valueFunction is not None:
			self._getVal = valueFunction


	def run(self):
		"""Thread start override"""
		print "Starting ThreadQueueProvider"
		self._isRunning = True
		self._initQueue()
		self._loop()

		if self.flushQueue:
			self._flushQueue()


	#
	# Internal Methods
	#
	
	def _initQueue(self):
		"""stuff queue full of valid vals so it provides"""
		for i in range(self.maxSize):
			try:
				self.queue.put(self._getVal(), False)
			except Queue.Full:  #ignore full exception, just stuff it (this shouldnt ever get hit)
				pass

	def _loop(self):
		nextVal = self._getVal()
		while self._isRunning:
			try:
				self.queue.put(nextVal, True, self.queuePushTimeout)
			except Queue.Full:
				pass
			else:
				nextVal = self._getVal()

	def _flushQueue(self):
		"""stuff queue full of empty vals to avoid blocking queue listening on a dead thread"""
		for i in range(self.maxSize):
			try:
				self.queue.put(0, False)
			except Queue.Full: #ignore full exception, just stuff it
				pass

	def _getVal(self):
		"""Internal method to be overwritten in subclass, or re-set using init arg valueFunction"""
		return None

	#
	# External Methods
	#

	def getVal(self, block=True, timeout=None):
		"""
		Gets the latest value from the Queue and returns it, saves requiring queue referencing in other thread
		Allows similar arguments as Queue.get()
		"""
		return self.queue.get(block, timeout)

	def close(self):
		"""Close the running of the thread - in its own time, which may be up to self.queuePushTimeout seconds long"""
		self._isRunning = False
