from flask import render_template
from app import app
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import Config
from app.database_ops import get_tags_for_coin


import requests
import json
import re


# define search twitter function
def search_for_recent_tweets(search_term, max_result):
    tweets_language = " lang:en"
    tweets_is_not_retweet = " -is:retweet"
    tweet_fields = "tweet.fields=text"
    query = search_term + tweets_is_not_retweet + tweets_language
    headers = {"Authorization": "Bearer {}".format(Config.TWITTER_BEARER_TOKEN)}
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}".format(
        query, tweet_fields, max_result
    )

    print(">> Call : " + url)

    # Making the twitter v2 API calls to get recent tweets
    # response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    # if response.status_code != 200:
    #     print("ERROR : Twitter API call Failed")
    #     print("ERROR : response.status_code : {} \n -> response.text: {}"
    #           .format(response.status_code, response.text))
    #     # raise Exception(response.status_code, response.text)
    #     return render_template('tweet_search_failure.html')
    #
    # return response.json()

    # UnComment For Ignoring calls and reading from the Dummy dataset files
    return get_tweets_from_file("crptocoin_tweets.json")


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

    # print("Overall sentiment dictionary is : ", sentiment_dict)
    # print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    # print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    # print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")
    #
    # print("Sentence Overall Rated As", end=" ")

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        sentiment_dict['over_all'] = 'Positive'
        # print("Positive")

    elif sentiment_dict['compound'] <= - 0.05:
        sentiment_dict['over_all'] = 'Negative'
        # print("Negative")

    else:
        sentiment_dict['over_all'] = 'Neutral'
        # print("Neutral")

    return sentiment_dict


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


def sentiment_percentage_calculator(total_input, total_one_type):
    percentage = (total_one_type * 100)/ total_input
    return percentage


def extract_texts(search_result):
    text_list = []
    for each in search_result['data']:
        text_list.append(clean_tweets(each['text']))
    return text_list


def clean_tweets(each_tweet):
    # print("Not Cleaned :" + each_tweet)
    each_tweet = re.sub('#', ' ', each_tweet)
    each_tweet = re.sub(r'@\S+', '', each_tweet)
    each_tweet = re.sub('#[A-Za-z0-9]+', '', each_tweet)
    each_tweet = re.sub('\\n', ' ', each_tweet)
    each_tweet = re.sub(r'http\S+', '', each_tweet)
    # print("\nAfter Cleaning :" + each_tweet)
    return each_tweet


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
    print("positive : {}% ".format(sentiment_percentage['positive_percentage']))
    print("negative : {}% ".format(sentiment_percentage['negative_percentage']))
    print("neutral  : {}% ".format(sentiment_percentage['neutral_percentage']))

    return overall_sentiment, sentiment_percentage
