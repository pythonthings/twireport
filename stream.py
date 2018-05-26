import redis
import time
from services import get_unique_hyperlinks, get_unique_words
from beautifultable import BeautifulTable

conn = redis.StrictRedis('localhost')
FIVE_MINUTES = 5 * 60 * 1000


def pretty_print_title(title, headers):
    print('\n\n' + title)
    print('*' * 80)
    table = BeautifulTable()
    table.column_headers = headers
    return table


def retrieve_user_data(start_time):
    table = pretty_print_title(title='User Report', headers=['Username', 'Number of tweets'])
    keys = conn.keys('user_*')
    for key in keys:
        # TODO username might have underscores
        username = key.split(b'_')[-1].decode('utf-8')
        tweet_count = conn.zcount(key, start_time - FIVE_MINUTES, start_time)
        table.append_row([username, tweet_count])
    print(table)


def retrieve_link_data():
    table = pretty_print_title(title='Link Report', headers=['Unique Domains'])
    keys = conn.keys('link_*')
    urls = []

    for key in keys:
        # import ipdb
        # ipdb.set_trace()
        data = conn.lrange(key, 0, -1)
        for d in data:
            urls.append(d.decode('utf-8'))
    unique_urls = get_unique_hyperlinks(urls)
    for url in unique_urls:
        table.append_row([url])
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
    for word in unique_words:
        table.append_row([word])
    print(table)


while True:
    start_time = time.time()
    retrieve_user_data(start_time=start_time)
    retrieve_link_data()
    retrieve_word_data()
    time.sleep(60.0 - ((time.time() - start_time) % 60.0))
