from flask import Flask, render_template, request
import json
import os
import BooleanRetrieval
import VSMRetrieval
import DocumentRetrieval

app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data/", "documents.json")
docs = json.load(open(json_url))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home/')
def home_screen():
    return render_template('Main.html')


@app.route('/search/', methods=['POST'])
def search():
    req = request.form
    search_query = req.get('search')
    collection = req.get('collection_select')
    search_model = req.get('search_select')
    search_type = req.get('search_type')

    if search_type == 'DocID':
        response = DocumentRetrieval.retrieve_documents(search_query.split(), False)
    else:
        if search_model == 'Boolean Retrieval':
            documents = BooleanRetrieval.evaluate_boolean_query(search_query)
            response = DocumentRetrieval.retrieve_documents(documents, False)
        else:
            documents = VSMRetrieval.evaluate_vsm(search_query)
            response = DocumentRetrieval.retrieve_documents(documents, False)

    return render_template('Search_Result.html', response=response, req=req)


@app.route('/search/<doc_id>')
def doc_select(doc_id):
    document = DocumentRetrieval.retrieve_documents([doc_id], True)

    return render_template('Document.html', document=document[0])


if __name__ == '__main__':
    app.run()








