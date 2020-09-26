# !/usr/bin/python
# coding=utf-8 
from model.CulturalObject import CulturalObject
from neomodel import (config, StructuredNode, StringProperty, DateTimeFormatProperty,
    RelationshipTo, StructuredRel, db)
from datetime import datetime
from settings import *


class IncludesRelationship(StructuredRel):
    dateFrom = DateTimeFormatProperty(True, "%Y-%m-%dT%H:%M:%S.%fZ")
    dateTo = DateTimeFormatProperty(True, "%Y-%m-%dT%H:%M:%S.%fZ")