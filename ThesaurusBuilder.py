import json
import os


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, 'static/data/', 'inverted_index_reuters.json')
dict_url = os.path.join(SITE_ROOT, 'static/data/', 'dictionary_reuters.json')
thesaurus_reuters = os.path.join(SITE_ROOT, 'static/data/', 'thesaurus_index.json')

docs = json.load(open(json_url))
dictionary = json.load(open(dict_url))

thesaurus = {}


def doc_id_to_list(dict_list):
    id_list = []

    for elem in dict_list:
        id_list.append(elem['DocID'])

    return id_list


def find_document(dict_list, doc_id):
    for doc in dict_list:
        if doc['DocID'] == doc_id:
            return doc

    return {}


def create_thesaurus():
    for word, doc_list in docs[0].items():
        if len(thesaurus.keys()) >= 200:
            json.dump(thesaurus, open(thesaurus_reuters, 'a'), indent=2)
            thesaurus.clear()

        thesaurus[word] = []
        doc_list_count = 0

        for doc in doc_list['Postings']:
            doc_list_count += doc['Term Frequency']

        for rel_word, rel_doc_list in docs[0].items():
            if word != rel_word and rel_word not in thesaurus.keys():
                intersection = list(set(doc_id_to_list(doc_list['Postings'])) & set(doc_id_to_list(rel_doc_list['Postings'])))
                intersect_counter = 0
                doc2_counter = 0

                for doc_id in intersection:
                    doc1 = find_document(doc_list['Postings'], doc_id)
                    doc2 = find_document(rel_doc_list['Postings'], doc_id)

                    intersect_counter += min(doc1['Term Frequency'], doc2['Term Frequency'])

                for rel_doc in rel_doc_list['Postings']:
                    doc2_counter += rel_doc['Term Frequency']

                jaccard = (intersect_counter*2)/(doc_list_count + doc2_counter)

                if jaccard != 0:
                    thesaurus[word].append({'word': rel_word, 'value': jaccard})


        thesaurus[word] = sorted(thesaurus[word], key=lambda k: k['value'], reverse=True)

        if len(thesaurus[word]) > 20:
            thesaurus[word] = thesaurus[word][:20]

