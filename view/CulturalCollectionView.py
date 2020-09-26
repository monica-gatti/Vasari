# !/usr/bin/python
# coding=utf-8 
from model.CulturalCollection import CulturalCollection
from flask import json
def get_cultural_collection_json(dictionaryCulturalCollection):
    return json.dumps(dictionaryCulturalCollection)
