import math
import json
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data/", "inverted_index.json")
index = json.load(open(json_url))
index = index[0]

json_url = os.path.join(SITE_ROOT, "static/data/", "tokenized_docs.json")
documents = json.load(open(json_url))

num_docs = len(documents)


def evaluate_vsm(query_string):
    query_tokens = query_string.split()
    query_weights = {}
    document_weights = {}

    for token in query_tokens:
        if token in index.keys():
            postings = index[token]['Postings']

            for doc in postings:
                if doc['DocID'] not in document_weights.keys():
                    document_weights[str(doc['DocID'])] = {'Terms': {token: doc['TF-IDF']}, 'Score': 0}
                else:
                    document_weights[doc['DocID']]['Terms'][token] = doc['TF-IDF']

            inverse_document_frequency = math.log((num_docs / len(documents)))
            query_weights[token] = inverse_document_frequency

    for key, value in document_weights.items():
        for token in query_tokens:
            if token not in value['Terms'].keys():
                value['Terms'][token] = 0

            value['Score'] += query_weights[token]*value['Terms'][token]

    if bool(document_weights):
        ranked_results = sorted(document_weights, key=lambda x: document_weights[x]['Score'], reverse=True)
    else:
        ranked_results = []

    return ranked_results
