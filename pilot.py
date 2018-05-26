#!./venv/bin/python

from api import Twitter
from services import get_expanded_urls, get_words_from_tweet, set_expiration
import time
import redis

conn = redis.StrictRedis('localhost')


def connect_to_twitter():
    '''
    Connect to Twitter Stream API using the API wrapper in stream.py in the following steps:

    Authenticate
    ============
    Authenticate app using OAuth

    Connect
    =======
    Connect to the streaming API using oauth object received from previous step

    Returns authenticated and stream connected Twitter object
    '''
    twitter = Twitter()
    twitter.authenticate()
    twitter.connect()
    return twitter


def filter_tweets(keyword):
    '''
    Filter the tweets for a given keyword obtained from user
    '''
    twitter = connect_to_twitter()
    stream = twitter.filter(keyword=keyword)
    for tweet in stream:
        # import ipdb
        # ipdb.set_trace()
        user_id = tweet['user']['id_str']
        user_name = tweet['user']['name']
        tweet_id = tweet['id_str']
        urls = tweet['entities']['urls']
        text = tweet['text']
        expanded_urls = get_expanded_urls(urls=urls)
        words = get_words_from_tweet(text=text)
        cur_time = time.time()
        link_key = 'link_{}'.format(tweet_id)
        word_key = 'word_{}'.format(tweet_id)
        conn.zadd('user_{}_{}'.format(user_id, user_name), **{tweet_id: cur_time})
        if expanded_urls:
            conn.lpush(link_key, *expanded_urls)
        if words:
            conn.lpush(word_key, *words)
        set_expiration([link_key, word_key])
        # print(conn.hgetall(tweet_id), conn.lrange(user_id, 0, -1))


if __name__ == '__main__':
    # Prompt user to enter a keyword on stdin
    conn.flushdb()
    keyword = input('Please enter the keyword which you\'d like to track:\n')
    filter_tweets(keyword=keyword)
