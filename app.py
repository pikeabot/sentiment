import urllib2
import os
import flask
from os import listdir
from os.path import isfile, join
import json
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import database_exists
from flask.ext.sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import twitter
from models import *
from scraper import *

Base = declarative_base()

engine = create_engine('postgresql://centralbureacracy:centralfiling@localhost/twitdata')
metadata=MetaData(bind=engine)
if not engine.dialect.has_table(engine.connect(), "Twitstock"):
	Twitstock=Table('Twitstock',metadata,
        Column('id',Integer,primary_key=True),
        Column('screen_name',String(50)),
        Column('created_at',String(50)),
        Column('text',String(500)),
        Column('retweet_count',Integer),
        )

metadata.create_all()

if not engine.dialect.has_table(engine.connect(), "ChinaStockNews"):
	ChinaStockNews=Table('ChinaStockNews',metadata,
        Column('id',Integer,primary_key=True),
        Column('screen_name',String(50)),
        Column('created_at',String(50)),
        Column('text',String(500)),
        Column('retweet_count',Integer),
        )

metadata.create_all()
Session = sessionmaker(bind=engine)

session=Session()

seed_twitdata(session)