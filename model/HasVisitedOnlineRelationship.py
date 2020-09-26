# !/usr/bin/python
# coding=utf-8 
from model.CulturalObject import CulturalObject
from neomodel import (config, StructuredNode, StringProperty, FloatProperty, DateTimeFormatProperty,
    RelationshipTo, StructuredRel, db)
from datetime import datetime
from settings import *

class HasVisitedOnlineRelationship(StructuredRel):
    visitDatetime = DateTimeFormatProperty(True, "%Y-%m-%dT%H:%M:%S.%fZ")
    type = StringProperty(unique_index=False, required=True)
    strength = FloatProperty(unique_index=False, required=False)