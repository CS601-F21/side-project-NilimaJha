from flask import render_template
from app import app
from config import Config
from app.database_ops import get_tags_for_coin
from app.database_ops import get_coin_details
import app.data_analysis_ops as da_ops


@app.route('/gettweets/<coin_name>')
def get_tweets_from_twitter(coin_name):
    print("entered get_tweets_from_twitter")
    print("Got : " + coin_name)
    tag_list = get_tags_for_coin(coin_name)
    print("Got Tags :-> ")
    print(tag_list)

    ## for testing  DELETE LATER
    print("*** Collecting for Tags: " + str(tag_list))
    ###########

    final_tweet_list = []
    for each_tag in tag_list:
        search_term = each_tag
        search_result = da_ops.search_for_recent_tweets(search_term=search_term, max_result=Config.MAX_TWEETS)
        print("+++++++++++>>>>")
        print(type(search_result))
        print("+++++++++++>>>> extract & clean only the text")
        final_tweet_list.extend(da_ops.extract_texts(search_result))
        print("+++++++++++>>>>")

    print("Data Collected for Tags: " + str(tag_list))

    # pretty printing
    print("inside get_tweets_from_twitter printing response")
    # print(json.dumps(json_response, indent=4, sort_keys=True))

    print("FINAL TWEETS LIST")
    print(len(final_tweet_list))
    overall_sentiment, sentiment_percentage = da_ops.run_sentiments(final_tweet_list)
    # print(final_tweet_list)
    coin_id, coin_name, coin_symbol = get_coin_details(coin_name)
    return render_template('analysis_result.html',
                           title='Result For: {}'.format(coin_name),
                           overall_sentiment_percentage=sentiment_percentage,
                           coin_name=coin_name,
                           coin_symbol=coin_symbol.upper(),
                           coin_id=coin_id,
                           result_type=overall_sentiment)
    # return "Hello from Index!"


#
# @app.route('/readFile')
# def index():
#     file_name = "crptocoin_tweets.json"
#     tweets = da_ops.get_tweets_from_file(file_name)
#     # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     # for i in tweets['data']:
#     #     print(i['text'])
#     # cleaning data
#
#     all_sentiments_score_list = []
#
#     for i in tweets['data']:
#         print(">>>>>>>:::::::>>>>>>>:::::::")
#         print(da_ops.clean_tweets(i['text']))
#         all_sentiments_score_list.append(da_ops.sentiment_scores(i['text']))
#
#     overall_sentiment_percentage = da_ops.find_overall_sentiment_score_percentage(all_sentiments_score_list)
#     if overall_sentiment_percentage['positive_percentage'] > overall_sentiment_percentage['negative_percentage']:
#         result_type = 'Positive'
#     elif overall_sentiment_percentage['negative_percentage'] > overall_sentiment_percentage['positive_percentage']:
#         result_type = 'Negative'
#     else:
#         result_type = "Neutral"
#     print(overall_sentiment_percentage['positive_percentage'])
#     print(overall_sentiment_percentage['negative_percentage'])
#     print(overall_sentiment_percentage['neutral_percentage'])
#     return render_template('analysis_result.html', title='Analysis Result', overall_sentiment_percentage=overall_sentiment_percentage, coin_name="Bitcoin", coin_symbol='BTC', coin_id='bitcoin', result_type=result_type)
#






