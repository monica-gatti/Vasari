# !/usr/bin/python
# coding=utf-8
from model.CulturalSite import CulturalSite
from flask import json
def get_cultural_site_json(dictionaryCulturalSite):
    return json.dumps(dictionaryCulturalSite)