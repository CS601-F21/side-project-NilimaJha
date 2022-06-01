#########################
#  Current Features
#########################
1. Analye Sentimeint of People (On Twitter) towards a given Coin based on the Tags associated for thart coin
	- Display Sentimeint analysis results in chart on the UI
2. Get and display Top Trending coins on CoinGecko in the last 24 hours 
3. Provide User option to Add a Coin to the Coin List
4. Provide User option to Add More Tags to a Given Coin Added to DB
5. Provide User option to Delete a Coin to the Coin List
6. Provide User option to Delete  Tags to a given Coin Added to DB.
7. Adding Loggin for the App

#########################
# Future Work 
########################
1. implement multiuser User login via Twitter and maintain their Profiles
2. Add more Graphs options for Results Visualization
3. Add option to Analyze all Coins in Users Profile and Display Consolidated sentiments for those coins in a graph


####### DB OPERATIONS Reference #######

########################
# Login to DB : 
########################
cd <Path of the Repository folder>
e.g :cd /Users/nilimajha/Desktop/Side Project - Current crypto View/side-project-NilimaJha/
ls - larth app.db
sqlite3 app.db

************************************************
* sqlite3 - SQL Commands to see Db details:
************************************************

########################
# See all tables 
########################
.table

########################
# Describe crypto_coins
########################
sqlite> .schema crypto_coins
CREATE TABLE crypto_coins (
	coin_id VARCHAR(25) NOT NULL, 
	coin_name VARCHAR(30), 
	coin_symbol VARCHAR(15), 
	coin_market_price FLOAT, 
	PRIMARY KEY (coin_id)
);
CREATE UNIQUE INDEX ix_crypto_coins_coin_name ON crypto_coins (coin_name);
CREATE UNIQUE INDEX ix_crypto_coins_coin_symbol ON crypto_coins (coin_symbol);

###############
# Describe tags
###############
sqlite> .schema tags
CREATE TABLE tags (
	tag_id INTEGER NOT NULL, 
	coin_id VARCHAR(25), 
	coin_tag VARCHAR(100), 
	PRIMARY KEY (tag_id), 
	FOREIGN KEY(coin_id) REFERENCES crypto_coins (coin_id)
);
CREATE INDEX ix_tags_coin_tag ON tags (coin_tag);

###############* Work involved *###############
1. Initial Prep 
	- Python intermediate bootcamp
	- python + Flask Framework Udemy Course
	- Basic HTML5 CSS course
	- Time taken ~ 20 Hours

2. Exploring Options and Understanding Varios APIs for DataSets for the project
	- Twitter APIs / tweepy apis / Coin CoinGecko
	- Time taken ~ 5 Hours

3. Research for What is sentiment Analysis and  best available/methodology tool for people sentiment analysis 
    - Went through various videos on YouTube to know about what is sentiment Analysis.
    - Studied about Sentiment Analysis using Vader and Text Blob. 
    - Time taken ~ 7 Hours	

4. Design and Setup Database 
	- Time taken ~ 3 hours

5. Code development/Testing
	- Time taken ~ 15 hours



