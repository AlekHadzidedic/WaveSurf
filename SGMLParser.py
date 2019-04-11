from html.parser import HTMLParser
from html.entities import name2codepoint
import re


class MySGMLParser(HTMLParser):

    def __init__(self):
        self.topics_flag = False
        self.title_flag = False
        self.body_flag = False
        self.no_body_flag = False
        self.document = []
        self.topics = []
        self.documents = {}
        self.doc_counter = 1
        super().__init__()

    def handle_starttag(self, tag, attrs):
        # print('Start tag :', tag)
        if tag == 'topics':
            # print(tag)
            self.topics_flag = True
        elif tag == 'title':
            self.title_flag = True
        elif tag == 'body':
            self.body_flag = True
        elif tag == 'date' and self.title_flag and not self.body_flag:
            self.no_body_flag = True

    def handle_endtag(self, tag):
        if tag == 'topics':
            self.topics_flag = False


    def handle_data(self, data):
        if self.topics_flag:
            self.topics.append(data)
        elif self.title_flag and not self.body_flag and not self.no_body_flag:
            self.document.append(data)
            self.document[0] = re.sub('[+:;(),.<>\[\]\(\\\'\)]', '', self.document[0])
            self.document[0] = self.document[0].lower()
            self.document[0] = self.document[0].replace('\"', '')
        elif self.title_flag and self.no_body_flag:
            self.title_flag = False
            self.no_body_flag = False
            # print(self.topics)
            topics = self.topics.copy()

            self.documents[self.doc_counter] = {'DocID': str(self.doc_counter),
                                                'Topics': topics,
                                                'Title': self.document[0],
                                                 'Body': ''}

            self.doc_counter += 1
            self.topics.clear()
            self.document.clear()
        elif self.title_flag and self.body_flag:
            self.document.append(data)

            cleaned_body = [self.document[len(self.document) - 1]]
            cleaned_body[0] = cleaned_body[0].replace('[\n', ' ')
            cleaned_body[0] = cleaned_body[0].replace('/', ' ')
            cleaned_body[0] = cleaned_body[0].replace('\"', '')
            cleaned_body[0] = re.sub('[+:;(),.<>\[\]\(\\\'\)]', '', cleaned_body[0])
            cleaned_body[0] = re.sub('\s+', ' ', cleaned_body[0]).strip()
            cleaned_body[0] = cleaned_body[0].replace('-', '')
            cleaned_body[0] = cleaned_body[0].lower()

            topics = self.topics.copy()

            self.documents[self.doc_counter] = {'DocID': str(self.doc_counter),
                                                'Topics': topics,
                                                'Title': self.document[0],
                                                'Body': cleaned_body[0]}

            self.doc_counter += 1
            self.topics.clear()
            self.document.clear()
            self.title_flag = False
            self.body_flag = False


    def handle_comment(self, data):
        print('Comment  :', data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print('Named ent:', c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print('Num ent  :', c)

    def handle_decl(self, data):
        print('Decl     :', data)
