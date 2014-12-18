import httplib
import time
import oauth2 as oauth
from config import *
import urllib2
import os
from os import listdir
from os.path import isfile, join
import json
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from flask.ext.sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import twitter
from models import *

Base = declarative_base()


engine = create_engine('postgresql://centralbureacracy:centralfiling@localhost/twitdata')
#Base.metadata.create_all(engine)

#if not engine.dialect.has_table(engine.connect(), "Twitstock"):
#		Base.metadata.create_all(engine)

if not engine.dialect.has_table(engine.connect(), "RussiaNews"):
		Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session=Session()

'''
connect directly to twitter to scrape accounts
'''
#url='https://api.twitter.com/oauth2/token'
#url='https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=Schuldensuehner&count=2'
url='https://api.twitter.com/1.1/statuses/mentions_timeline.json?count=2&since_id=14927799'
def twit_oauth(url):
	consumer = oauth.Consumer(key=TW_CONSUMER_KEY, secret=TW_CONSUMER_SECRET)
	token = oauth.Token(key=TW_ACCESS_TOKEN, secret=TW_ACCESS_TOKEN_SECRET)
	client = oauth.Client(consumer, token)
	resp, content = client.request( url, "GET")
	r=json.dumps(resp)
	return r
#return content home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', 'abcdefg', 'hijklmnop' )

def stocktwit_oauth(url):
	consumer = oauth.Consumer(key=ST_CONSUMER_KEY, secret=ST_CONSUMER_SECRET)
	token = oauth.Token(key=ST_ACCESS_TOKEN, secret=ST_ACCESS_TOKEN_SECRET)
	client = oauth.Client(consumer, token)
	resp, content = client.request( url, "GET")
	r=json.load(resp)[0]
	return r

'''
scrape HTML using BeautifulSoup
'''
def soupify(url):
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
	headers = { 'User-Agent' : user_agent }
	#req = urllib2.Request('http://www.herinterest.com/60-flirty-text-messages/', None, headers)
	#req = urllib2.Request('https://twitter.com/ConanOBrien', None, headers)
	#req = urllib2.Request('https://twitter.com/justinbaldoni', None, headers)
	#req = urllib2.Request('https://twitter.com/brenton_clarke', None, headers)
	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()

	return BeautifulSoup(page)

'''
get tweets from TWitter for users and add to declarative_base
'''
def seed_twitdata():
	#screen_name='Schuldensuehner'
	users=['stockmarketpnt', 'WinStockTraders', 'yurybarmin', 'kengfeed', 'PerchwellHQ', 'ETFDAILYNEWS', 'MarkAmesExiled',
			'hsilverb', 'CNBC', 'zbswanepoel', 'zerohedge', 'katie_martin_FX', 'KaiPflughaupt', 'intlGR', 'InvestorPlace',
			'TheStreetAlerts', 'BiiwiiNFTRH', 'TuurDemeester', 'rougek68', 'danielhoeg', 'STOCK_GIRL', 'DouglasLucas', 
			'mgrenier731', 'SurvivalistBlog', 'sarahlain12', 'KeithMcCullough', 'markbartontv', 'alanchiu', 'WSJ', 
			'nicolas_veron', 'MarketWatch', 'CNNMoney', 'Slate', 'ForeignPolicy', 'voxdotcom', 'CarnegieCorp', 
			'guardian', 'TheEconomist', 'ReutersOpinion', 'jonathanchait', 'FT', 'pencadlys', 'AP', 'RussiaInsider',
			'RT_com', 'SputnikInt']

	api = twitter.Api(consumer_key=TW_CONSUMER_KEY,
		 					consumer_secret=TW_CONSUMER_SECRET,
		 					access_token_key=TW_ACCESS_TOKEN,
		 					access_token_secret=TW_ACCESS_TOKEN_SECRET)

	for screen_name in users:
		
		statuses = api.GetUserTimeline(screen_name=screen_name)
		for s in statuses:
			session.add(Twitstock(text=s.text, 
								created_at=s.created_at,
								screen_name=screen_name, 
								retweet_count=s.retweet_count))

		session.commit()

'''
add tweets scraped from html to declarative_base
'''
def add_soup_tweets_db():
	soup = soupify('https://twitter.com/brenton_clarke')


	#print soup.find("div", {"class:ProfileTweet-text js-tweet-text u-dir"})
	tweets=soup.find_all("p", class_="ProfileTweet-text js-tweet-text u-dir")
	for t in tweets:
		fd=fdata(text=t.get_text(), category='n')
		session.add(fd)

	text=soup.find_all("strong")
	for t in text:
		str=t.get_text().strip().split('.', 1)
		try: 
			int(str[0])
			fd = fdata(text= str[1], category = 'f')
			session.add(fd)
		except:
			pass

	session.commit()

