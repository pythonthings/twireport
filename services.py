import operator
import re
from collections import Counter
from urllib.parse import urlparse

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

stop_words = set(stopwords.words('english'))
punctuation = set([',', '\'', ':', '@', '#', 'https', 'http'])
blacklist = set.union(stop_words, punctuation)


def set_expiration(conn, args, exp_time=5 * 60 + 5):
    '''
    .. function:: set_expiration(conn, args, exp_time=5 * 60 + 5)

        Set expiration time of the argument key in Redis cache

        :param conn:             Object that connects with Redis ConnectionPool*
        :param args:             List of arguments*
        :param exp_time:         Expiration time to set on the key (seconds)
        :type conn:              RedisConnection
        :type args:              list
        :type exp_time:          int
    '''
    for arg in args:
        conn.expire(arg, exp_time)


def get_expanded_urls(urls):
    '''
    .. function:: get_expanded_urls(urls)

        Function to get expanded URLs and extract domains out of it.

        :param urls:             URLs included in the tweet*
        :type urls:              list

        :return: list
    '''
    expanded_urls = []
    for url in urls:
        parsed_uri = urlparse(url['expanded_url'])
        expanded_urls.append(parsed_uri.netloc)
    return expanded_urls


def get_sanitized_tweet_words(text):
    '''
    .. function:: get_sanitized_tweet_words(text)

        Function to tokenize all the words in tweet and extract sanitized word list.

        :param text:             Text of the tweet*
        :type text:              str

        :return: list
    '''
    # Exclude the links from text
    words = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)
    tokenized = sent_tokenize(words)
    word_list = []
    for i in tokenized:
        word_list = nltk.word_tokenize(i)
        word_list = [str(word) for word in word_list if word not in blacklist or not word.startswith('//t.co')]
    return word_list


def get_unique_hyperlinks(urls):
    '''
    .. function:: get_unique_hyperlinks(urls)

        Function to get the expanded unique domains sorted by count.

        :param urls:             Entity URLs from Twitter stream*
        :type urls:              list

        :return: list
    '''
    hyperlinks = [k for k, v in Counter(urls).items()]
    return hyperlinks


def get_unique_words(words):
    '''
    .. function:: get_unique_words(words)

        Function to get unique words sorted by count.

        :param words:             Text of the tweet*
        :type words:              str

        :return: list
    '''
    words_and_count = Counter(words)
    return sorted(words_and_count.items(), key=operator.itemgetter(1), reverse=True)[:10]
