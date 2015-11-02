import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, relationship
from flask.ext.sqlalchemy import SQLAlchemy

Base = declarative_base()


class Twitstock(Base):
	__tablename__='Twitstock'
	id = Column(Integer, primary_key=True)
	screen_name=Column(String(50))
	created_at=Column(String(50))
	text = Column(String(500))
	retweet_count = Column(Integer)

class ChinaStockNews(Base):
	__tablename__='ChinaStockNews'
	id = Column(Integer, primary_key=True)
	screen_name=Column(String(50))
	created_at=Column(String(50))
	text = Column(String(500))
	retweet_count = Column(Integer)


