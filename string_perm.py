import itertools
from nltk.corpus import stopwords


class WordType():
    '''
    Defines different types of words which are to be removed from the tweets.
    '''
    conjunction = ['and', 'or']
    articles = ['a', 'an', 'the']
    pronouns = ['he', 'she', 'it', 'they', 'i', 'we', 'them', 'per', 'all',
                'some', 'none', 'both', 'little', 'most', 'much', 'neither', 'one', 'many']
    prepositions = ['of', 'for', 'to', 'on', 'in']
    others = ['RT']


def get_all_permutations(w_type):
    '''
    Get all permutations of a given string.

    Example Usage
    -------------
    >> from string_perm import get_all_permutations
    >> get_all_permutations(w_type='articles')

    ['A',
     'a',
     'AN',
     'An',
     'aN',
     'an',
     'THE',
     'THe',
     'ThE',
     'The',
     'tHE',
     'tHe',
     'thE',
     'the']
    '''
    all_perm = []
    wordlist = getattr(WordType, w_type)
    for word in wordlist:
        all_perm.extend(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in word))))

    return all_perm


stop_words = set(stopwords.words('english'))
punctuation = set([',', '\'', ':', '@', '#', 'https', 'http'])
conjunction = set(get_all_permutations(w_type='conjunction'))
articles = set(get_all_permutations(w_type='articles'))
pronouns = set(get_all_permutations(w_type='pronouns'))
prepositions = set(get_all_permutations(w_type='prepositions'))
others = set(get_all_permutations(w_type='others'))

blacklist = set.union(stop_words, punctuation, conjunction, articles, pronouns, prepositions, others)
