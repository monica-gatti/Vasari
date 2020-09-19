from model.CulturalSite import CulturalSite
from flask import json
def get_cultural_site_json(dictionaryCulturalSite):
    return json.dumps(dictionaryCulturalSite)