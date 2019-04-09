import json
import math
import os


def create_inverted_index(dictionary, corpus):
    num_docs = len(corpus)
    inverted_index = {}
    index_row = {}
    postings_list = []
    for term in dictionary[0]:
        for doc in corpus:
            term_frequency = doc['Title'].count(term) + doc['Body'].count(term)
            if term_frequency != 0:
                postings_list.append({'DocID': doc['DocID'], 'Term Frequency': term_frequency, 'TF-IDF': 0})
            else:
                continue

        inverse_document_frequency = math.log((num_docs/len(postings_list)))

        for posting in postings_list:
            posting['TF-IDF'] = posting['Term Frequency'] * inverse_document_frequency

        inverted_index[term] = {'Postings': postings_list.copy()}
        postings_list.clear()
        index_row.clear()

    return inverted_index

