import json
import HTMLParser
import SGMLParser
import DictionaryBuilder
import InvertedIndexBuilder
import ThesaurusBuilder
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

raw_doc_url = os.path.join(SITE_ROOT, "static/data/", "UofOCourses.txt")
raw_doc_reuters_url = os.path.join(SITE_ROOT, "static/data/", "reut2-000.txt")
tokenized_doc_url = os.path.join(SITE_ROOT, "static/data/", "tokenized_docs.json")
tokenized_doc_reuters_url = os.path.join(SITE_ROOT, "static/data/", "tokenized_docs_reuters.json")
dict_url = os.path.join(SITE_ROOT, "static/data/", "dictionary.json")
dict_reuters_url = os.path.join(SITE_ROOT, "static/data/", "dictionary_reuters.json")
doc_url = os.path.join(SITE_ROOT, "static/data/", "documents.json")
doc_reuters_url = os.path.join(SITE_ROOT, "static/data/", "documents_reuters.json")
inverted_index_url = os.path.join(SITE_ROOT, "static/data/", "inverted_index.json")
inverted_index_reuters_url = os.path.join(SITE_ROOT, "static/data/", "inverted_index_reuters.json")
thesaurus_reuters = os.path.join(SITE_ROOT, "static/data/", "thesaurus_index.json")

# p = HTMLParser.MyHTMLParser()
# stringHtml = open(raw_doc_url, 'r').read()
# p.feed(stringHtml)
#
# dictionary = DictionaryBuilder.create_dictionary(True, True, True, json.load(open(doc_url)))
# json.dump(DictionaryBuilder.tokenized_documents, open(tokenized_doc_url, 'w'), indent=2)
#
# del dictionary['']
# del dictionary['&']
#
# json.dump([dictionary], open(dict_url, 'w'), indent=2)
#
# index = InvertedIndexBuilder.create_inverted_index(json.load(open(dict_url)), json.load(open(tokenized_doc_url)))
# json.dump([index], open(inverted_index_url, 'w'), indent=2)

# s = SGMLParser.MySGMLParser()
# string_sgml = open(raw_doc_reuters_url, 'r').read()
# s.feed(string_sgml)
#
# json.dump([s.documents], open(doc_reuters_url, 'w'), indent=2)
#
# dictionary_reuters = DictionaryBuilder.create_dictionary(True, True, True, json.load(open(doc_reuters_url)))
# json.dump(DictionaryBuilder.tokenized_documents, open(tokenized_doc_reuters_url, 'w'), indent=2)
# json.dump([dictionary_reuters], open(dict_reuters_url, 'w'), indent=2)
# index = InvertedIndexBuilder.create_inverted_index(json.load(open(dict_reuters_url)),
#                                                    json.load(open(tokenized_doc_reuters_url)))
# json.dump([index], open(inverted_index_reuters_url, 'w'), indent=2)

ThesaurusBuilder.create_thesaurus()
