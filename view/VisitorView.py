from model.Visitor import Visitor
from flask import json
def get_visitor_json(dictionaryVisitor):
    return json.dumps(dictionaryVisitor)