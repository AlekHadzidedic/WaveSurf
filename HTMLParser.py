from html.parser import HTMLParser
from html.entities import name2codepoint
import json
import os


class MyHTMLParser(HTMLParser):

    def __init__(self):
        self.title_flag = False
        self.body_flag = False
        self.french_flag = False
        self.document = []
        self.documents = {}
        self.doc_counter = 1
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if len(attrs) >= 1:
            if attrs[0][0] == 'class' and attrs[0][1] == 'courseblocktitle noindent':
                self.title_flag = True
            elif attrs[0][0] == 'class' and attrs[0][1] == 'courseblockdesc noindent':
                self.body_flag = True

    def handle_endtag(self, tag):
        print('End tag  :', tag)
        if tag == 'html':
            SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
            doc_url = os.path.join(SITE_ROOT, "static/data/", "documents.json")
            json.dump([self.documents], open(doc_url, 'w'), indent=2)

    def handle_data(self, data):
        if self.title_flag and not self.body_flag:
            data = data.strip('\n')
            data = data.strip('')
            self.document.append(data)
            if 'é' in data:
                self.french_flag = True

        elif self.title_flag and self.body_flag:
            data = data.strip('\n')
            self.document.append(data)
            if not self.french_flag:
                self.documents[self.doc_counter] = {'DocID': str(self.doc_counter),
                                                    'Title': self.document[0],
                                                    'Body': self.document[2]}
                self.doc_counter += 1
                self.document.clear()
            else:
                self.document.clear()
                self.french_flag = False

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