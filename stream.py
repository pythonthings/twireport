import time

import redis
from beautifultable import BeautifulTable

from services import get_unique_hyperlinks, get_unique_words

conn = redis.StrictRedis('localhost')
count = 0


def pretty_print_title(title, headers):
    print('\n\n' + title)
    print('*' * 80)
    table = BeautifulTable()
    table.column_headers = headers
    return table


def remove_user_data(start_time):
    keys = conn.keys('user_*')
    for key in keys:
        # Remove tweet IDs which won't be needed in next iteration
        conn.zremrangebyscore(key, start_time, start_time + 61)


def retrieve_user_data():
    table = pretty_print_title(title='User Report {}'.format(count), headers=['Username', 'Number of tweets'])
    keys = conn.keys('user_*')
    for key in keys:
        username = key.split(b':')[-1].decode('utf-8')
        tweet_count = conn.zcard(key)
        if tweet_count:
            table.append_row([username, tweet_count])
    print(table)


def retrieve_link_data():
    table = pretty_print_title(title='Link Report', headers=['Unique Domains'])
    keys = conn.keys('link_*')
    urls = []

    for key in keys:
        dataset = conn.lrange(key, 0, -1)
        for data in dataset:
            urls.append(data.decode('utf-8'))

    url_count = len(urls)
    unique_urls = get_unique_hyperlinks(urls)
    for url in unique_urls:
        table.append_row([url])
    print('\nTotal link count: {}'.format(url_count))
    print(table)


def retrieve_word_data():
    table = pretty_print_title(title='Word Report', headers=['Content Report'])
    keys = conn.keys('word_*')
    words = []
    for key in keys:
        data = conn.lrange(key, 0, -1)
        for d in data:
            words.append(d.decode('utf-8'))

    unique_words = get_unique_words(words)
    unique_word_count = len(unique_words)
    for word in unique_words[:10]:
        table.append_row([word[0]])
    print('\nUnique word count: {}'.format(unique_word_count))
    print(table)


# Run an infinite loop and call the functions to generate the report every 1 minute
while True:
    count = count + 1
    start_time = time.time()
    if count != 1 and count % 5 == 1:
        remove_user_data(start_time=start_time - 300)
    time.sleep(60.0 - ((time.time() - start_time) % 60.0))
    retrieve_user_data()
    retrieve_link_data()
    retrieve_word_data()
