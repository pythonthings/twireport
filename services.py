from collections import Counter
import re


def get_unique_hyperlinks(urls):
    '''
    .. function:: get_unique_hyperlinks(urls)

        Function to get the expanded unique domains sorted by count.

        :param urls:             Entity URLs from Twitter stream*
        :type urls:              list

        :return: list
    '''
    expanded_urls = []
    for url in urls:
        expanded_urls.append(url['expanded_url'])
    hyperlinks = [k for k, v in Counter(expanded_urls).items()]
    return hyperlinks


def get_unique_words(text):
    '''
    .. function:: get_unique_words(text)

        Function to get unique words sorted by count.

        :param text:             Text of the tweet*
        :type text:              str

        :return: list
    '''
    # Exclude the links from text
    words = re.sub(r'^https?:\/\/.*[\r\n]*', '', text)
    unique_words = [k for k, v in Counter(words.split()).items()]
    return unique_words


def get_processed_tweet_data(obj, conn):
    '''
    .. function:: get_processed_tweet_data(obj, conn)

        Function to process tweet data and send the required response to be saved in Redis hashmaps.

        :param obj:             Object to access live Twitter Stream API*
        :param conn:            Connection object for Redis Connection Pool*
        :type obj:              TwitterDictResponse
        :type conn:             Redis

        :return: dict
    '''
    urls = obj['entities']['urls']
    links = get_unique_hyperlinks(urls=urls)
    words = get_unique_words(text=obj['text'])
    tweet_data = {
        'username': obj['user']['name'],
        'tweet_count': conn.llen(obj['user']['id_str']),
        'links': links,
        'link_count': len(links),
        'words': words,
        'word_count': len(words),
    }
    return tweet_data
