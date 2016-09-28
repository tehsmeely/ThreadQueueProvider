import threading, Queue, time, random

from threadQueueProvider import ThreadQueueProvider

random.seed()


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
			print "Getter: before sleep"
			time.sleep(5)
			print "Getter: getting val: {}".format(provider.getVal())

def getValFunct():
	rn = random.randint(1, 100)
	print "Provider generating random num: ", rn
	return rn

if __name__ == "__main__":
	provider = ThreadQueueProvider(maxSize=5, valueFunction=getValFunct)
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

	provider.close()
	getter._isRunning = False