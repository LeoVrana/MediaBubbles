#Run in the virtual env!
import pickle
import re
import itertools
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from newsplease import NewsPlease
import urllib


output = open('Outputs.txt', 'a')
all_URLs = []
brokens = ['http://www.breitbart.com/big-hollywood/2017/12/09/disney-suspends-executive-jon-heely-felony-child-sex-abuse-charges/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+breitbart+%28Breitbart+News%29','http://dailycaller.com/2017/11/23/report-flynns-lawyers-signal-possible-cooperation-with-mueller/','https://www.infowars.com/why-the-don-jr-wikileaks-exchange-means-nothing/','http://www.breitbart.com/national-security/2017/12/08/report-venezuelans-opening-medical-flea-markets/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+breitbart+%28Breitbart+News%29','http://www.breitbart.com/big-hollywood/2017/12/07/hollywood-reacts-al-franken-resignation-hope-fake-news/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+breitbart+%28Breitbart+News%29','https://www.infowars.com/crazy-joe-scarborough-thought-he-should-be-vice-president/','https://www.infowars.com/weinstein-inquiry-police-departments-likely-to-join-forces-experts-say/' ,'https://www.infowars.com/come-on-heres-how-cbs-news-spelled-correction-after-pushing-fakenews-about-trump/','http://money.cnn.com/2017/12/08/news/economy/november-jobs-report/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_allpolitics+%28RSS%3A+CNN+-+Politics%29','https://www.infowars.com/exclusive-video-of-rep-joe-barton-masturbating/','http://dailycaller.com/2017/11/22/nfl-considering-making-protesting-the-anthem-illegal-heres-where-the-protesters-will-now-be-forced-to-kneel/','http://dailycaller.com/2017/11/26/exclusive-cfpbs-leandra-english-is-a-pupil-of-elizabeth-warren/','https://www.infowars.com/breaking-live-head-of-google-announces-plan-to-censor-russian-news-false-flag-imminent/','http://dailycaller.com/2017/11/14/house-conservatives-plan-to-introduce-tax-reform-amendment-repealing-obamacare-mandate/','http://thehill.com/homenews/senate/360468-gop-senator-obamacare-mandate-a-tax-on-the-poor-and-working-class','https://www.nytimes.com/video/us/politics/100000005551798/jeff-sessions-testimony-capitol-hill.html?partner=rss&emc=rss','https://www.nytimes.com/video/us/politics/100000005551798/jeff-sessions-testimony-capitol-hill.html?partner=rss&emc=rss','http://dailycaller.com/2017/11/14/rand-paul-calls-for-individual-mandate-repeal-in-tax-bill/','https://www.nytimes.com/video/us/politics/100000005549866/roy-moore-alabama-sexual-misconduct.html?partner=rss&emc=rss','https://www.nytimes.com/video/us/politics/100000005545308/maga-day-an-interview-with-steve-bannon.html?partner=rss&emc=rss','https://www.nytimes.com/video/us/politics/100000005542204/diverse-candidates-make-history-in-local-elections.html?partner=rss&emc=rss','https://www.nytimes.com/video/us/politics/100000005538314/trump-voters-one-year-later.html?partner=rss&emc=rss','https://www.nytimes.com/video/us/politics/100000005542149/chris-christie-gets-in-argument-with-voter.html?partner=rss&emc=rss','https://www.nytimes.com/video/us/politics/100000005538729/trumps-striking-change-in-tone-on-china.html?partner=rss&emc=rss','https://www.infowars.com/democrat-calls-for-censoring-infowars-on-twitter/','https://www.infowars.com/roger-stone-can-rosenstein-investigate-rosenstein/','https://www.infowars.com/dilbert-creator-scott-adams-the-lefts-bullying-is-backfiring-on-them/','https://www.infowars.com/the-next-american-revolution-has-begun/','https://www.nytimes.com/video/us/politics/100000005532355/trump-says-he-knew-of-no-russian-ties-documents-say-different.html?partner=rss&emc=rss','https://www.nytimes.com/video/us/politics/100000005526699/conservative-media-robert-mueller.html?partner=rss&emc=rss','https://www.nytimes.com/video/us/politics/100000005524742/who-is-george-papadopoulos.html?partner=rss&emc=rss','http://thehill.com/homenews/administration/357665-trump-sloppy-michael-moore-show-on-broadway-was-a-total-momb','http://thehill.com/policy/international/357629-pence-to-military-on-north-korea-be-ready','http://checkyourfact.com/2017/10/26/fact-check-does-the-us-have-a-71-billion-trade-deficit-with-mexico/','http://checkyourfact.com/2017/10/26/fact-check-does-the-us-lose-almost-all-trade-disputes/','https://www.infowars.com/video-colbert-completely-discredited-after-dems-admit-peegate-dossier-was-a-forged-fraud/','http://checkyourfact.com/2017/10/25/fact-check-is-climate-change-a-bigger-fiscal-issue-than-entitlements/','http://checkyourfact.com/2017/10/25/fact-check-did-republicans-pay-for-the-trump-dossier/','http://checkyourfact.com/2017/10/25/fact-check-would-small-businesses-pay-the-lowest-tax-rate-in-over-80-years-under-the-gop-tax-plan/','https://www.infowars.com/the-truth-about-weinsteingate-revealed/', 'https://www.infowars.com/what-is-the-deep-state-hiding-about-the-jfk-hit/']

#print(matches) # works

#print(len(matches)) # 701

def the_work():
	outlets = ['breitbart', 'nytimes', 'dailycaller', 'wsj', 'politico', 'slate', 'infowars', 'foxnews', 'cnn', 'thehill'] 

	#Load the URLs from each outlet into the list, all_URLs
	for outlet in outlets:
		#define pickle name we are looking for
		filename = outlet + "_urls.pickle"
		URLs = pickle.load(open(filename, 'rb'))
		all_URLs.append(URLs)
		#dump an empty pickle afterward
		pickle.dump(URLs, open(filename, 'wb'))

	#Now we have a flat list of all the URLs.
	URL_list = list(itertools.chain(*all_URLs))

	#to_process is a way of making sure we pick up from where we left off.
	to_process = pickle.load(open("to_process.pickle", 'rb'))
	for URL in URL_list:
		to_process.append(URL)

	to_process = list(set(to_process))

	#to process is like our to do list. update it here.
	pickle.dump(to_process, open("to_process.pickle", 'wb'))



	for URL in to_process:
		old_URLs = pickle.load(open('old_URLs.pickle', 'rb'))
		if URL in old_URLs:
			continue
		elif 'checkyourfact.com' in URL:
			continue
		else:
			#some are redirects, so...
			print("Getting that URL from " + URL)
			try:
				req = requests.get(URL)
			except:
				brokens.append(URL)
				old_URLs.append(URL)
				continue
			real_URL = req.url	
			if "/video/" in real_URL:
				brokens.append(URL)
				old_URLs.append(URL)
				print("It was just a video.")
				continue
			print("Real URL is " + real_URL)
			if real_URL in brokens:
				old_URLs.append(real_URL)
				old_URLs.append(URL)
				pickle.dump(old_URLs, open('old_URLs.pickle', 'wb'))
				continue
			article = NewsPlease.from_url(real_URL)
			# try:
			# 	article = NewsPlease.from_url(real_URL)
			# except (TypeError, urllib.error.HTTPError, urllib.error.URLError):
			# 	print("There was an error, adding this to brokens:" + real_URL)
			# 	brokens.append(URL)
			# 	brokens.append(real_URL)
			# 	continue

			output.write(article.title) # the title
			output.write("\t")
			output.write(real_URL) # the URL of the article
			output.write("\t") 
			output.write(str(article.date_publish))
			output.write("\t") 
			try: 
				text_without_breaks = re.sub(r'\n', ' ', article.text)
			except TypeError:
				text_without_breaks = "NO TEXT.\n"
			print(text_without_breaks)
			output.write(text_without_breaks)
			output.write("\n")
			old_URLs.append(real_URL)
			old_URLs.append(URL)
			old_URLs = list(set(old_URLs))
			pickle.dump(old_URLs, open('old_URLs.pickle', 'wb'))


the_work()
sched = BlockingScheduler()
@sched.scheduled_job('interval', id='generate', minutes=20)
def job_function():
    the_work()

sched.start()


#need to open the pickle
#iterate through the urls therein
#write to the new article list

#Title\tURL\tDate\tText\n

#going to need to find duplicates in the beginning