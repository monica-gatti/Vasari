from model.CulturalObject import CulturalObject
from neomodel import (config, StructuredNode, StringProperty, FloatProperty, DateTimeFormatProperty,
    RelationshipTo, StructuredRel, db)
from datetime import datetime
from settings import *

class HasVisitedRelationship(StructuredRel):
    visitDatetime = DateTimeFormatProperty(True, "%Y-%m-%dT%H:%M:%S.%fZ")
    TYPES = {'2D': '2D', '3D': '3D', 'off-line': 'off-line'}
    Type = StringProperty(required=False, choices=TYPES)
    Position = StringProperty(unique_index=False, required=False)
    Precision = FloatProperty(unique_index=False, required=False)