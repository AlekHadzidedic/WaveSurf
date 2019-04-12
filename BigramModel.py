import json
import os
import nltk
from nltk.corpus import brown

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data/", "documents_reuters.json")
dict_url = os.path.join(SITE_ROOT, "static/data/", "dictionary_reuters.json")
docs = json.load(open(json_url))
dictionary = json.load(open(dict_url))


def create_language_model():
    all_words = ''

    for values in docs[0].values():
        all_words += values['Title'] + ' ' + values['Body'] + ' '

    freq_words = nltk.FreqDist(all_words.split(' '))

    cfreq_words_2gram = nltk.ConditionalFreqDist(nltk.bigrams(all_words.split(' ')))

    cprob_words_2gram = nltk.ConditionalProbDist(cfreq_words_2gram, nltk.MLEProbDist)

    return cprob_words_2gram


bigram_prob = create_language_model()


def query_expansion(query):
    if len(query.split(' ')) == 1:
        print(bigram_prob[query].samples())
        for key in bigram_prob[query].samples():
            print(bigram_prob[query].prob(key))


query_expansion('bahia')