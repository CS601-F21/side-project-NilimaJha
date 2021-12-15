from flask import render_template
from app import app
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import Config

import requests
import json
import re


# define search twitter function
# this method makes api 
def search_for_recent_tweets(search_term, max_result):
    tweets_language = " lang:en"
    tweets_is_not_retweet = " -is:retweet"
    tweet_fields = "tweet.fields=text"
    query = search_term + tweets_is_not_retweet + tweets_language
    headers = {"Authorization": "Bearer {}".format(Config.TWITTER_BEARER_TOKEN)}
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}".format(
        query, tweet_fields, max_result
    )

    app.logger.debug(">> Call : " + url)

    ####Making the twitter v2 API calls to get recent tweets
    response = requests.request("GET", url, headers=headers)
    app.logger.debug(response.status_code)
    if response.status_code != 200:
        app.logger.debug("ERROR : Twitter API call Failed")
        app.logger.debug("ERROR : response.status_code : {} \n -> response.text: {}"
              .format(response.status_code, response.text))
        # raise Exception(response.status_code, response.text)
        return render_template('tweet_search_failure.html')

    return response.json()

    # # UnComment For Ignoring calls and reading from the Dummy dataset files
    # return get_tweets_from_file("crptocoin_tweets.json")


# backup method to get tweets from static data set
# that is the tweets stored in a file in case the Twitter API is not working.
def get_tweets_from_file(file_name):
    # Opening JSON file
    f = open(file_name)
    # loading JSON as python dict
    data = json.load(f)
    # Closing file
    f.close()
    return data


# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    # app.logger.debug("Overall sentiment dictionary is : ", sentiment_dict)
    # app.logger.debug("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    # app.logger.debug("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    # app.logger.debug("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")
    #
    # app.logger.debug("Sentence Overall Rated As", end=" ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        sentiment_dict['over_all'] = 'Positive'
    elif sentiment_dict['compound'] <= - 0.05:
        sentiment_dict['over_all'] = 'Negative'
    else:
        sentiment_dict['over_all'] = 'Neutral'

    return sentiment_dict


# method to calculate overall sentiment percentage from the sentiment scores of each tweet.
def find_overall_sentiment_score_percentage(all_sentiments_score):
    total_positive = 0
    total_negative = 0
    total_neutral = 0

    for each_sentiment_score in all_sentiments_score:
        if each_sentiment_score['over_all'] == 'Positive':
            total_positive = total_positive + 1
        elif each_sentiment_score['over_all'] == 'Negative':
            total_negative = total_negative + 1
        else:
            total_neutral = total_neutral + 1

    positive_percentage = sentiment_percentage_calculator(len(all_sentiments_score), total_positive)
    negative_percentage = sentiment_percentage_calculator(len(all_sentiments_score), total_negative)
    neutral_percentage = sentiment_percentage_calculator(len(all_sentiments_score), total_neutral)
    sentiment_percentage = {'positive_percentage': positive_percentage, 'negative_percentage': negative_percentage, 'neutral_percentage': neutral_percentage}
    return sentiment_percentage


# method to calculate percentage.
def sentiment_percentage_calculator(total_input, total_one_type):
    percentage = (total_one_type * 100) / total_input
    return percentage


# method for extracting tweets text from search result obtained from Twitter.
def extract_texts(search_result):
    text_list = []
    for each in search_result['data']:
        text_list.append(clean_tweets(each['text']))
    return text_list


# Method to clean the tweets extracted from the Twitter.
def clean_tweets(each_tweet):
    # app.logger.debug("Not Cleaned :" + each_tweet)
    each_tweet = re.sub('#', ' ', each_tweet)
    each_tweet = re.sub(r'@\S+', '', each_tweet)
    each_tweet = re.sub('#[A-Za-z0-9]+', '', each_tweet)
    each_tweet = re.sub('\\n', ' ', each_tweet)
    each_tweet = re.sub(r'http\S+', '', each_tweet)
    # app.logger.debug("\nAfter Cleaning :" + each_tweet)
    return each_tweet


# method to find the overall sentiment of the search from the percentage calculation.
def run_sentiments(final_tweet_list):
    all_sentiments_score_list = []
    for each_tweet in final_tweet_list:
        all_sentiments_score_list.append(sentiment_scores(each_tweet))

    sentiment_percentage = find_overall_sentiment_score_percentage(all_sentiments_score_list)

    if sentiment_percentage['positive_percentage'] > sentiment_percentage['negative_percentage']:
        overall_sentiment = 'Positive'
    elif sentiment_percentage['negative_percentage'] > sentiment_percentage['positive_percentage']:
        overall_sentiment = 'Negative'
    else:
        overall_sentiment = "Neutral"
    app.logger.debug("positive : {}% ".format(sentiment_percentage['positive_percentage']))
    app.logger.debug("negative : {}% ".format(sentiment_percentage['negative_percentage']))
    app.logger.debug("neutral  : {}% ".format(sentiment_percentage['neutral_percentage']))

    return overall_sentiment, sentiment_percentage


# method to get top trending searched coin name from CoinGecko.
def top_trending_searched_coins():
    top_searched_coins = []
    get_top_searched_api_url = "https://api.coingecko.com/api/v3/search/trending"
    response = requests.request("GET", get_top_searched_api_url)

    app.logger.info(response.status_code)
    if response.status_code != 200:
        app.logger.info("ERROR : Top Trending Searched Coins details Couldn't be collected from CoinGecko API")
        return top_searched_coins

    response_data = response.json()
    for each in response_data['coins']:
        top_searched_coins.append(each['item']['id'])

    return top_searched_coins


# method to get coin's current market price using CoinGecko API.
def get_coin_current_market_price(coin_id):
    url = "https://api.coingecko.com/api/v3/coins/{}".format(coin_id)

    current_market_price = "UNKNOWN"

    response = requests.request("GET", url)

    app.logger.info(response.status_code)
    if response.status_code != 200:
        app.logger.info("ERROR : Top Trending Searched Coins details Couldn't be collected from CoinGecko API")
        return current_market_price

    response_data = response.json()

    return response_data['market_data']['current_price']['usd']
