import json
import HTMLParser
import DictionaryBuilder
import InvertedIndexBuilder
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

raw_doc_url = os.path.join(SITE_ROOT, "static/data/", "UofOCourses.txt")
tokenized_doc_url = os.path.join(SITE_ROOT, "static/data/", "tokenized_docs.json")
dict_url = os.path.join(SITE_ROOT, "static/data/", "dictionary.json")
doc_url = os.path.join(SITE_ROOT, "static/data/", "documents.json")
inverted_index_url = os.path.join(SITE_ROOT, "static/data/", "inverted_index.json")

p = HTMLParser.MyHTMLParser()
stringHtml = open(raw_doc_url, 'r').read()
p.feed(stringHtml)

dictionary = DictionaryBuilder.create_dictionary(True, True, True, json.load(open(doc_url)))
json.dump(DictionaryBuilder.tokenized_documents, open(tokenized_doc_url, 'w'), indent=2)

del dictionary['']
del dictionary['&']

json.dump([dictionary], open(dict_url, 'w'), indent=2)

index = InvertedIndexBuilder.create_inverted_index(json.load(open(dict_url)), json.load(open(tokenized_doc_url)))
json.dump([index], open(inverted_index_url, 'w'), indent=2)


