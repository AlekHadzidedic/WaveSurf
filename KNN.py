import json
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data/", "documents_reuters.json")
dict_url = os.path.join(SITE_ROOT, "static/data/", "dictionary_reuters.json")
index_url = os.path.join(SITE_ROOT, "static/data/", "inverted_index_reuters.json")
topic_url = os.path.join(SITE_ROOT, "static/data/", "topic_doc_reuters.json")
tokenized_url = os.path.join(SITE_ROOT, "static/data/", "tokenized_docs_reuters.json")
weighted_url = os.path.join(SITE_ROOT, "static/data/", "weighted_tokenized_reuters.json")
no_topic_url = os.path.join(SITE_ROOT, "static/data/", "no_topic_doc_reuters.json")
docs = json.load(open(json_url))
dictionary = json.load(open(dict_url))
tokenized = json.load(open(tokenized_url))
index = json.load(open(index_url))

topic_docs = []
no_topic_docs = []

def find_tokenized_doc(d_id):
    for doc in tokenized:
        if doc['DocID'] == d_id:
            return doc

def get_word_score(d_id, term):
    if term in index[0].keys():
        postings = index[0][term]['Postings']

        for posting in postings:
            if posting['DocID'] == d_id:
                return posting['TF-IDF']

def knn_classification(num_neighbors):
    for doc_id, values in docs[0].items():
        weighted_dict = {}

        document = find_tokenized_doc(doc_id)

        for word in document['Title']:
            if word not in weighted_dict:
                weighted_dict[word] = get_word_score(doc_id, word)

        for word in document['Body']:
            if word not in weighted_dict:
                weighted_dict[word] = get_word_score(doc_id, word)

        weighted_dict_copy = weighted_dict.copy()

        if len(values['Topics']) > 0:
            topic_docs.append({'DocID': doc_id, 'Terms': weighted_dict_copy, 'Topics': values['Topics']})
        else:
            no_topic_docs.append({'DocID': doc_id, 'Terms': weighted_dict_copy, 'Topics': values['Topics']})

        weighted_dict.clear()

    for entry in no_topic_docs:
        ranked_document = []

        for topic_entry in topic_docs:
            score = 0

            for term_dict in (entry['Terms']):
                print(entry['Terms'][term_dict])
                if term_dict in topic_entry['Terms']:
                    score += entry['Terms'][term_dict]**2


knn_classification(3)