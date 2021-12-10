from flask import render_template
from app import app
import app.helper as h
from app.database_test import db_test
import requests
import json
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import numpy
import pandas
# import matplotlib.pyplot as plt

from config import Config


@app.route('/home')
def home():
    user = {'username': h.gadha()}
    return render_template('index.html', title='Home', user=user)


@app.route('/conditionalHome')
def conditional_home():
    greetings = {'greeting': 'Hello Nilima! This is not a default greeting.'}
    title = 'Actual Title'
    return render_template('conditional_home.html', title=title, greetings=greetings)


@app.route('/gettweets')
def get_tweets_from_twitter():
    print("entered get_tweets_from_twitter")
    # search_term = "#bitcoin -filter:retweets"
    # print("inside index & created search_term :" + search_term)
    # tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang='eng', since="2021-12-09",
    #                        tweet_mode="extended").items(10)
    # print("inside index & called cursor object of tweepy.")
    # all_tweets = [tweet.full_text for tweet in tweets]
    # # tweets_data_frame =
    # print(search_term)
    # print(all_tweets)
    # search term

    search_term = "bitcoin"

    # query1 = search_term + tweets_is_not_retweet + tweets_language
    # query = "bitcoin -is:retweet lang:en"
    # twitter fields to be returned by api call
    # tweet_fields = "tweet.fields=text,author_id,created_at"
    tweet_field = "text"
    max_result = 10;

    # twitter api call
    json_response = get_tweets_from_twitter(search_term=search_term, tweet_field=tweet_field, max_result=max_result)
    print("inside get_tweets_from_twitter got response")
    # pretty printing
    print("inside get_tweets_from_twitter printing response")
    print(json.dumps(json_response, indent=4, sort_keys=True))

    return "Hello from Index!"


# define search twitter function
def get_tweets_from_twitter(search_term, tweet_field, max_result):
    tweets_language = " lang:en"
    tweets_is_not_retweet = " -is:retweet"
    tweet_fields = "tweet.fields=" + tweet_field
    query = search_term + tweets_is_not_retweet + tweets_language
    headers = {"Authorization": "Bearer {}".format(Config.TWITTER_BEARER_TOKEN)}
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}".format(
        query, tweet_fields, max_result
    )

    # response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    # if response.status_code != 200:
    #     raise Exception(response.status_code, response.text)
    # return response.json()
    return


def get_tweets_from_file(file_name):
    # Opening JSON file
    f = open(file_name)

    # returns JSON object asa dictionary
    data = json.load(f)

    # data_frame = pandas.DataFrame(columns=['Tweets'])
    # Iterating through the json list
    # for i in data['data']:
    #     data_frame = pandas.DataFrame(i['text'], columns=['Tweets'])
    #     print(i['text'])

    # Closing file
    f.close()
    return data


@app.route('/readFile')
def index():
    file_name = "bitcoin_reviews.json"
    tweets = get_tweets_from_file(file_name)
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # for i in tweets['data']:
    #     print(i['text'])
    # cleaning data

    for i in tweets['data']:
        print(">>>>>>>:::::::>>>>>>>:::::::")
        # print(i['text'])
        # print("??????????????")
        print(clean_tweets(i['text']))
        sentiment_scores(i['text'])

    return "Hello from Index!"


def clean_tweets(each_tweet):
    print("Not Cleaned :" + each_tweet)
    each_tweet = re.sub('#', ' ', each_tweet)
    each_tweet = re.sub(r'@\S+', '', each_tweet)
    each_tweet = re.sub('#[A-Za-z0-9]+', '', each_tweet)
    each_tweet = re.sub('\\n', ' ', each_tweet)
    each_tweet = re.sub(r'http\S+', '', each_tweet)
    print("\nAfter Cleaning :" + each_tweet)
    return each_tweet


# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")

    print("Sentence Overall Rated As", end=" ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        print("Positive")

    elif sentiment_dict['compound'] <= - 0.05:
        print("Negative")

    else:
        print("Neutral")

