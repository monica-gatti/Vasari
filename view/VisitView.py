# !/usr/bin/python
# coding=utf-8 
from model.Visitor import Visitor
from flask import json
def get_visits_to_cultural_object_json(dictionaryVisit):
    return json.dumps(dictionaryVisit)
def get_cumulative_visits_to_cultural_object_json(culturalObjectID, datefrom, dateto, dictionaryCumulativeVisit):
    return json.dumps(dictionaryCumulativeVisit)