import os
import json


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data/", "documents.json")
docs = json.load(open(json_url))


def retrieve_documents(doc_id_list, is_doc_id_endpoint):
    documents = []

    for doc_id in doc_id_list:
        if doc_id in docs[0].keys():
            documents.append(docs[0][doc_id].copy())

    if not is_doc_id_endpoint:
        for doc in documents:
            doc['Body'] = doc['Body'][:doc['Body'].index('.') + 1]

    return documents


