import threading, time, sqlite3


##Import the module
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parentdir) 
from threadQueueProvider import ThreadQueueProvider


class DatabaseProvider(ThreadQueueProvider):
	"""
		ThreadQueueProvider child class - Provides jokes randomly taken from a database, hot and fresh.
		Allows access to the sqlite3 database from just one thread, while allowing as many others to poll it
		In this context, may consider increasing the 
	"""
	def __init__(self):
		ThreadQueueProvider.__init__(self)
		self.db = None
		self.i = 0

	def run(self):
		self.db = initialiseDB() #dummy in-memory sqlite3 Database
		ThreadQueueProvider.run(self)

	def _getVal(self):
		#This is the overridden method from ThreadQueueProvider
		self.i += 1 # maintaining i to verify results are unique
		return "({}) {} - {}".format(self.i, *self.db.execute("""SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1;""").fetchone())



class Getter(threading.Thread):
	"""Sleeping thread which periodically gets a value from the provider function"""
	def __init__(self, provider, name="Getter", delay=2):
		threading.Thread.__init__(self)
		self.provider = provider
		self.delay = delay
		self.name = name
		self._isRunning = False
	def run(self):
		self._isRunning = True
		self._loop()
	def _loop(self):
		while self._isRunning:
			val = self.provider.getVal()
			print "{}: {}".format(self.name, val)
			time.sleep(self.delay)
	def close(self):
		self._isRunning = False




def initialiseDB():
	db = sqlite3.connect(":memory:")
	db.execute("""CREATE TABLE jokes (joke TEXT, source TEXT)""")
	for joke in JOKES:
		db.execute("""INSERT INTO jokes VALUES (?, ?)""", joke)
	db.commit()
	return db
JOKES = [  #From http://www.mirror.co.uk/tv/tv-news/edinburgh-fringe-35-funniest-one-8686179
("My dad has suggested that I register for a donor card. He's a man after my own heart.","Masai Graham"),
("Why is it old people say 'there's no place like home' yet when you put them in one...","Stuart Mitchell"),
("I've been happily married for four years - out of a total of 10.","Mark Watson"),
("Apparently, one in three Britons are conceived in an IKEA bed, which is mad because those places are really well lit.","Mark Smith"),
("I went to a pub quiz in Liverpool, had a few drinks so I wasn't much use. Just for a laugh I wrote The Beatles or Steven Gerrard for every answer... came second.","Will Duggan"),
("Brexit is a terrible name, sounds like cereal you eat when you are constipated.", "Tiff Stevenson"),
("I often confuse Americans and Canadians. By using long words.","Gary Delaney"),
("Why is Henry's wife covered in tooth marks? Because he's Tudor.","Adele Cliff"),
("Don't you hate it when people assume you're rich because you sound posh and went to private school and have loads of money?","Annie McGrath"),
("Is it possible to mistake schizophrenia for telepathy, I hear you ask.","Jordan Brookes"),
("My motto in life is always give 100%. Which makes blood donation quite tricky.","Tony Cowards"),
("Hillary Clinton has shown that any woman can be President. As long as your husband did it first.", "Michelle Wolf"),
("I spotted a Marmite van on the motorway. It was heading yeastbound.", "Roger Swift"),
("Back in the day, Instagram just meant a really efficient drug dealer.", "Arthur Smith"),
("I'll tell you what's unnatural in the eyes of God. Contact lenses.", "Zoe Lyons"),
("Elton John hates ordering Chinese food. Soya seems to be the hardest word.", "Phil Nicol"),
("I don't know why my elderly neighbour bothers subscribing to newspapers if he's just going to let them pile up outside his house.", "Glenn Moore"),
("When I'm listening to U2, I turn down the treble a little bit. Just to take The Edge off.", "Darren Walsh"),
("Spent the last three days alone trying to learn escapology. I need to get out more.", "Pete Firman"),
("I've made a terrible spelling mistake in the wedding order of service. My stepfather, of course, is a COUNT'", "Anna Morris"),
("I sometimes feel suicidal so my therapist suggested I do CBT. So I did, and now I can ride a motorbike. How's that going to help?", "Eric Lampeart"),
("My dad was an Army engineer who specialised in clearing minefields. He always wanted me to follow in his footsteps.", "Tony Cowards"),
("Everyone has a racist gran. I call mine Ku Klux nan", "Liam Withnail"),
("I lost a court case battle against a popular fabric softener; I fought Lenor, and Lenor won", "Glenn Moore"),
("It took me two hours before I realised my pot of herbs had gone missing. I thought: 'No way? Where's the thyme gone!'", "Anthony Wright"),
("From my window all I can see is fish fingers. I've got a Birds Eye view.", "Leo Kearse"),
("Getting dumped on Pancake Day - you'd flip.", "Sarah Callaghan"),
("In tennis, what does deuce mean? It's a refreshing drink drunk by players between games.", "Radio Active"),
("I love my area, but it's been getting a bit gentrified recently - I can tell because my dealer's joined LinkedIn.", "Ed Night"),
("My mum likes the saying 'Life is not measured by the number of breaths we take, but by the moments that take our breath away.' I'm asthmatic, that's out of order.", "Brennan Reece"),
("I think we should change the name of Type 1 Diabetes and Type 2 Diabetes to Not Your Fault Diabetes and Mostly Your Fault Diabetes.", "Michelle Wolf"),
("I can't exercise for long. When I get back from a run my girlfriend usually asks if I've forgotten something.", "Pete Otway"),
("Do you know what I'd do if I found you in bed with my wife? I'd tuck you in.", "Paul McMullan"),
("At University I studied archaeology. I scraped through my exams.", "Stuart Mitchell"),
("If you want your child to have a head start in the science industry then consider naming it 'Et Al'. Get its name on a lot of science papers straight away.", "Stuart Laws"),
]

if __name__ == "__main__":
	##Create Database Provider. Database isnt loaded until start()
	dbProvider = DatabaseProvider()

	##Create our debug getters which will get jokes from DatabaseProvider
	getters = [
		Getter(dbProvider, "A", 3),
		Getter(dbProvider, "B", 5),
		Getter(dbProvider, "C", 7)
	]

	##Start all of them!
	dbProvider.start() #this doesnt need to be started first, but the getters will block until ready 
	for getter in getters:
		getter.start()

	##Now wait and see what the getters output. Stop on interrupt etc
	try:
		time.sleep(30)
	except:
		pass


	##Close all our threads
	print "Killing threads" 
	dbProvider.close()
	for getter in getters:
		getter.close()

