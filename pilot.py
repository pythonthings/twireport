#!./venv/bin/python

from stream import Twitter
from services import get_processed_tweet_data
import redis

conn = redis.Redis('localhost')


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
        import ipdb
        ipdb.set_trace()
        user_id = tweet['user']['id_str']
        tweet_id = tweet['id_str']
        data = get_processed_tweet_data(obj=tweet, conn=conn)
        conn.lpush(user_id, tweet_id)
        conn.hmset(tweet_id, data)
        conn.expire(user_id, 5 * 60 + 5)
        conn.expire(tweet_id, 5 * 60 + 5)
        print(conn.hgetall(tweet_id), conn.lrange(user_id, 0, -1))


if __name__ == '__main__':
    # Prompt user to enter a keyword on stdin
    keyword = input('Please enter the keyword which you\'d like to track:\n')
    filter_tweets(keyword=keyword)
