import json
import os


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data/", "inverted_index_reuters.json")
dict_url = os.path.join(SITE_ROOT, "static/data/", "dictionary_reuters.json")

docs = json.load(open(json_url))
dictionary = json.load(open(dict_url))

thesaurus = []


def doc_id_to_list(dict_list):
    id_list = []

    for elem in dict_list:
        id_list.append(elem["DocID"])

    return id_list


def find_document(dict_list, doc_id):
    for doc in dict_list:
        if doc["DocID"] == doc_id:
            return doc

    return {}


def create_thesaurus():
    for word, doc_list in docs[0].items():

        doc_list_count = 0

        for doc in doc_list:
            doc_list_count +

        for rel_word, rel_doc_list in docs[0].items():
            if word != rel_word:
                intersection = list(set(doc_id_to_list(doc_list)) & set(doc_id_to_list(rel_doc_list)))
                sim_counter = 0
                total_counter = 0

                for doc_id in intersection:
                    doc1 = find_document(doc_list, doc_id)
                    doc2 = find_document(rel_doc_list, doc_id)

                    sim_counter += min(doc1["Term Frequency"], doc2["Term Frequency"])

