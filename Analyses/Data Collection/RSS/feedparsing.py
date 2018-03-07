import pickle
import feedparser
from apscheduler.schedulers.blocking import BlockingScheduler

#get the pickle of the list from the appropriate outlet.
nytimes = []
breitbart = []
dailycaller = []
wsj = []
politico = []
slate = []
infowars = []
foxnews = []
cnn = []
thehill = []
motherjones = []

outlets = [[nytimes, 'nytimes', ['http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml']], [breitbart, 'breitbart', ['http://feeds.feedburner.com/breitbart?format=xml']], [dailycaller, 'dailycaller', ['http://dailycaller.com/section/politics/feed/']], [wsj, 'wsj', ['http://online.wsj.com/xml/rss/3_7087.xml']], [politico, 'politico', ['http://www.politico.com/rss/politics08.xml']], [slate, 'slate', ['http://feeds.slate.com/slate']], [infowars, 'infowars', ['https://www.infowars.com/feed/custom_feed_rss']], [foxnews, 'foxnews', ['http://feeds.foxnews.com/foxnews/politics']], [cnn, 'cnn', ['http://rss.cnn.com/rss/cnn_allpolitics.rss']], [thehill, 'thehill', ['http://thehill.com/rss/syndicator/19109']]] 

def setup():
	for outlet in outlets:
		filename = outlet[1] + '_urls.pickle'
		pickle.dump(outlet[0], open(filename, 'wb'))



#outlet[2] is a list of the feeds from that outlet.




#make a set of it.

#list the set.

#repickle.

#next feed.



def parse_it():
	for outlet in outlets:
		current_outlet = outlet[0]

		#parse the feed.

		for url in outlet[2]:
			feed = feedparser.parse(url)


			for item in feed['entries']:

				if item['link'] not in current_outlet:
					current_outlet.append(item['link'])
					print(item['link'])


		#dump it

		filename = outlet[1] + '_urls.pickle'
		pickle.dump(current_outlet, open(filename, 'wb'))




setup()

sched = BlockingScheduler()

@sched.scheduled_job('interval', id='feedparse', hours=1)
def job_function():
    parse_it()

parse_it()

sched.start()