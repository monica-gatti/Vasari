from model.CulturalObject import CulturalObject
from neomodel import (config, StructuredNode, StringProperty, FloatProperty, DateTimeFormatProperty,
    RelationshipTo, StructuredRel, db)
from datetime import datetime
from settings import *

class HasInteractedVRARRelationship(StructuredRel):
    visitDatetime = DateTimeFormatProperty(True, "%Y-%m-%dT%H:%M:%S.%fZ")
    type = StringProperty(unique_index=False, required=True)
    value = FloatProperty(unique_index=False, required=False)