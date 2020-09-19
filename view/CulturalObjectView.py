from model.CulturalObject import CulturalObject
from flask import json
def get_cultural_object_json(dictionaryCulturalObject):
    return json.dumps(dictionaryCulturalObject)