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
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, and_
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from flask.ext.sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import twitter
from models import *

engine = create_engine('postgresql://centralbureacracy:centralfiling@localhost/twitdata')
#Base.metadata.create_all(engine)

if not engine.dialect.has_table(engine.connect(), "Twitstock"):
		Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session=Session()


tw_count=session.query(Twitstock).count()
rn_count=session.query(ChinaStockNews).count()

print session.query(Twitstock).filter(Twitstock.text.ilike('%russia%')).first().created_at
print session.query(RussiaNews).filter(ChinaStockNews.text.ilike('%russia%')).count()

s=session.query(Twitstock, ChinaStockNews)\
			.filter(Twitstock.screen_name==ChinaStockNews.screen_name)\
			.filter(and_(Twitstock.text.ilike('%military%'), Twitstock.text.ilike("%russia%"))).first()

print s