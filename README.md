# sentiment
Scraping Twitter and other websites for sentiment

This repo gets the last 200 tweets from several Twitter users related to the China stock market crash. Data is stored in a Postgres table. If the table is missing the tables will be created. 

python app.py will run the script and pull tweets and store them in the database. 
