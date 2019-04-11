import json
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data/", "documents.json")
bi
docs = json.load(open(json_url))