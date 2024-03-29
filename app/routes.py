import logging
import os

from flask import render_template
from app import app
from config import Config
from app.database_ops import get_tags_for_coin
from app.database_ops import get_coin_details
import app.data_analysis_ops as da_ops


# method that handles request with path '/gettweets/<coin_name>'
@app.route('/gettweets/<coin_name>')
def get_tweets_from_twitter(coin_name):
    app.logger.debug("entered get_tweets_from_twitter")
    app.logger.debug("Got : " + coin_name)

    # getting all the associated tags from db for the coin selected by user.
    tag_list = get_tags_for_coin(coin_name)
    app.logger.debug("Got Tags :-> ")
    app.logger.debug(tag_list)

    # when no tag is associated with the given coins.
    if len(tag_list) == 0:
        app.logger.debug("*** NO Search Tags Associated with Coin ID ***")
        return render_template('no_tag_found.html', title='No Tag Found', coin_name=coin_name)

    final_tweet_list = []
    # for each tag in the tag table associated to the given coin, extract relevant tweets from Twitter.
    for each_tag in tag_list:
        search_term = each_tag
        search_result = da_ops.search_for_recent_tweets(search_term=search_term, max_result=Config.MAX_TWEETS)
        app.logger.debug(type(search_result))
        app.logger.debug(search_result)
        app.logger.debug("extracting & cleaning only the text")
        # cleaning all the text from each tweet and adding it to a final_tweet_list
        final_tweet_list.extend(da_ops.extract_texts(search_result))

    app.logger.debug("Data Collected for Tags: " + str(tag_list))
    app.logger.debug("inside get_tweets_from_twitter printing response")
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    app.logger.debug("FINAL TWEETS LIST")
    app.logger.debug(len(final_tweet_list))

    # getting sentiment of each tweet.
    overall_sentiment, sentiment_percentage = da_ops.run_sentiments(final_tweet_list)
    coin_id, coin_name, coin_symbol = get_coin_details(coin_name)
    coin_current_price = da_ops.get_coin_current_market_price(coin_id)

    # collecting Chart data
    return render_template('analysis_result.html',
                           title='Result For: {}'.format(coin_name),
                           overall_sentiment_percentage=sentiment_percentage,
                           coin_name=coin_name,
                           coin_symbol=coin_symbol.upper(),
                           coin_id=coin_id,
                           coin_current_price=coin_current_price,
                           result_type=overall_sentiment,
                           positive=sentiment_percentage['positive_percentage'],
                           negative=sentiment_percentage['negative_percentage'],
                           neutral=sentiment_percentage['neutral_percentage'])







