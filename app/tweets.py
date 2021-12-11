from flask import render_template, redirect
from app import app
# from app import oauth
import requests
# from app import api
import tweepy


@app.route('/gettweet')
def get_tweets_from_twitter():
    print("entered index")
    search_term = "#bitcoin -filter:retweets"
    print("inside index & created search_term :" + search_term)
    # tweets = tweepy.cursor(api.search_tweets, q=search_term, lang='eng', since="2021-12-01", tweet_mode="extended").items(100)
    print("inside index & called cursor object of tweepy.")
    # all_tweets = [tweet.full_text for tweet in tweets]
    # tweets_data_frame =
    print(search_term)
    # print(all_tweets)
    return "Hello from Index!"