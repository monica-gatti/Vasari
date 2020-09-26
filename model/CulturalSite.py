# !/usr/bin/python
# coding=utf-8
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, FloatProperty,DateTimeProperty,DateTimeFormatProperty,
    UniqueIdProperty, RelationshipTo, StructuredRel, db, DoesNotExist, DeflateError)
from datetime import datetime
from settings import *
from model.CulturalCollection import CulturalCollection
from model.CulturalObject import CulturalObject
from model.CustomsExceptions import *
import sys

class ExhibitsRelationship(StructuredRel):
    dateFrom = DateTimeFormatProperty(True, "%Y-%m-%dT%H:%M:%S.%fZ")
    dateTo = DateTimeFormatProperty(True, "%Y-%m-%dT%H:%M:%S.%fZ")
class CulturalSite(StructuredNode):
    ID = StringProperty(unique_index=True, required=True)
    Name = StringProperty(unique_index=False, required=True)
    exhibits = RelationshipTo(CulturalCollection, 'EXHIBITS', model=ExhibitsRelationship)
    owns = RelationshipTo('CulturalObject', 'OWNS')
    @property
    def serialize(self):
        return {
            'ID': self.ID,
            'Name': self.Name,
    }

#from neomodel import db
#db.set_connection('bolt://neo4j:neo4j@localhost:7687')

def culturalsite_doesnt_exist(culturalsite_id):
    try:
        culturalSite = CulturalSite.nodes.get(ID=culturalsite_id) 
    except DoesNotExist:
        return True
    return False
def get_cultural_site(culturalsite_id):
    try:
        culturalSite = CulturalSite.nodes.get(ID=culturalsite_id)
        return dict(culturalSite.serialize)
    except DoesNotExist:
        raise ObjectNotFoundException(culturalsite_id)
    except:
        raise GenericErrorException(sys.exc_info()[0])
def get_cultural_sites():
    try:
        culturalSites = CulturalSite.nodes
        list_of_culturalSites = list(culturalSites)
        return dict(json_cultural_sites = [culturalSite.serialize for culturalSite in list_of_culturalSites])
    except Exception as e:
        raise GenericErrorException(sys.exc_info()[1]) 
def culturalsite_update(culturalsite_id,json_data):
    try:
        culturalSite = CulturalSite.nodes.get(ID=culturalsite_id);
        culturalSite.Name= json_data.get("Name")
        culturalSite.save()
    except DoesNotExist:
        raise ObjectNotFoundException(culturalsite_id)
    except DeflateError:
        raise ArgumentOutOfRangeException("please check fields")
    except:
        raise GenericErrorException(sys.exc_info()[0])
def culturalsite_create(json_data):
    try:
        culturalSite = CulturalSite(ID= json_data.get('ID'), Name= json_data.get('Name'))
        culturalSite.save()
        return dict(culturalSite.serialize)
    except Exception as e:
        raise GenericErrorException(sys.exc_info()[0]) 
def culturalsite_delete(culturalsite_id):
    try:
        culturalSite = CulturalSite.nodes.get(ID=culturalsite_id);
        culturalSite.delete()
    except DoesNotExist:
        raise ObjectNotFoundException(culturalsite_id)
    except:
        raise GenericErrorException(sys.exc_info()[0])
