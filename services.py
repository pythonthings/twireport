from collections import Counter
import re
import nltk
import operator
from urllib.parse import urlparse
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

stop_words = set(stopwords.words('english'))
punctuation = set([',', '\'', ':', '@', '#', 'https', 'http'])
blacklist = set.union(stop_words, punctuation)


def set_expiration(conn, *args, exp_time=5 * 60 + 5):
    for arg in args:
        conn.expire(arg, exp_time)


def get_expanded_urls(urls):
    expanded_urls = []
    for url in urls:
        parsed_uri = urlparse(url['expanded_url'])
        expanded_urls.append(parsed_uri.netloc)
    return expanded_urls


def get_words_from_tweet(text):
    # Exclude the links from text
    words = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)
    # filtered_sentence = " ".join(str(word) for word in words)
    # Remove articles, pronouns, propositions and conjunctions
    tokenized = sent_tokenize(words)
    print(tokenized)
    word_list = []
    for i in tokenized:
        word_list = nltk.word_tokenize(i)
        # import ipdb
        # ipdb.set_trace()
        word_list = [str(word) for word in word_list if word not in blacklist]
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
    .. function:: get_unique_words(text)

        Function to get unique words sorted by count.

        :param text:             Text of the tweet*
        :type text:              str

        :return: list
    '''
    word_count = len(words)
    words_and_count = Counter(words)
    return sorted(words_and_count.items(), key=operator.itemgetter(1), reverse=True)[:10]


# def get_processed_user_data(obj, conn):
#     '''
#     .. function:: get_processed_tweet_data(obj, conn)

#         Function to process tweet data and send the required response to be saved in Redis hashmaps.

#         :param obj:             Object to access live Twitter Stream API*
#         :param conn:            Connection object for Redis Connection Pool*
#         :type obj:              TwitterDictResponse
#         :type conn:             Redis

#         :return: dict
#     '''
#     # urls = obj['entities']['urls']
#     # links = get_unique_hyperlinks(urls=urls)
#     # words = get_unique_words(text=obj['text'])
#     tweet_data = {
#         'username': obj['user']['name'],
#         # 'links': links,
#         # 'link_count': len(links),
#         # 'words': words,
#         # 'word_count': len(words),
#     }
#     return tweet_data
