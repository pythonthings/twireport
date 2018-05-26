#!./venv/bin/python

import time

import redis

from api import Twitter
from services import (get_expanded_urls, get_sanitized_tweet_words,
                      set_expiration)

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
        tweet_id = tweet['id_str']
        expanded_urls = get_expanded_urls(urls=tweet['entities']['urls'])
        words = get_sanitized_tweet_words(text=tweet['text'])
        cur_time = time.time()
        link_key = 'link_{}'.format(tweet_id)
        word_key = 'word_{}'.format(tweet_id)
        conn.zadd('user_{}:{}'.format(tweet['user']['id_str'], tweet['user']['name']), **{tweet_id: cur_time})
        if expanded_urls:
            conn.lpush(link_key, *expanded_urls)
        if words:
            conn.lpush(word_key, *words)
        set_expiration(conn=conn, args=[link_key, word_key])


if __name__ == '__main__':
    # Prompt user to enter a keyword on stdin
    conn.flushdb()
    keyword = input('Please enter the keyword which you\'d like to track:\n')
    filter_tweets(keyword=keyword)
