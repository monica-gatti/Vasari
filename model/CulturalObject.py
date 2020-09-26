# !/usr/bin/python
# coding=utf-8 
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, FloatProperty,DateTimeProperty,DateTimeFormatProperty,
    UniqueIdProperty, RelationshipTo, StructuredRel, db, DoesNotExist, DeflateError, RelationshipFrom)
from datetime import datetime
from settings import *
from model.CustomsExceptions import *
import sys

class CulturalObject(StructuredNode):
    ID = StringProperty(unique_index=True, required=True)
    Name = StringProperty(unique_index=False, required=True)
    Room = StringProperty(unique_index=False, required=True)
    @property
    def serialize(self):
        return {
            'ID': self.ID,
            'Name': self.Name,
            'Room': self.Room
    }
def culturalobject_doesnt_exist(culturalobject_id):
    try:
        culturalObject = CulturalObject.nodes.get(ID=culturalobject_id) 
    except DoesNotExist:
        return True
    return False
def get_cultural_object(culturalobject_id):
    try:
        culturalObject = CulturalObject.nodes.get(ID=culturalobject_id)
        return dict(culturalObject.serialize)
    except DoesNotExist:
        raise ObjectNotFoundException(culturalobject_id)
    except:
        raise GenericErrorException(sys.exc_info()[0])
def get_cultural_objects():
    try:
        culturalObjects = CulturalObject.nodes                                                                                                                            
        list_of_culturalObjects = list(culturalObjects)
        return dict(json_cultural_objects = [culturalObject.serialize for culturalObject in list_of_culturalObjects])
    except Exception as e:
        raise GenericErrorException(sys.exc_info()[0]) 
def culturalobject_update(culturalobject_id,json_data):
    try:
        culturalObject = CulturalObject.nodes.get(ID=culturalobject_id);
        culturalObject.Name= json_data.get("Name")
        culturalObject.Room=json_data.get("Room")
        culturalObject.save()
    except DoesNotExist:
        raise ObjectNotFoundException(culturalobject_id)
    except DeflateError:
        raise ArgumentOutOfRangeException("please check fields")
    except:
        raise GenericErrorException(sys.exc_info()[0])
def culturalobject_create(json_data):
    try:
        culturalObject = CulturalObject(ID= json_data.get('ID'), Name= json_data.get('Name'), Room = json_data.get("Room"))
        culturalObject.save()
        return dict(culturalObject.serialize)
    except Exception as e:
        raise GenericErrorException(sys.exc_info()[0])    
def culturalobject_delete(culturalobject_id):
    try:
        culturalObject = CulturalObject.nodes.get(ID=culturalobject_id);
        culturalObject.delete()
    except DoesNotExist:
        raise ObjectNotFoundException(culturalobject_id)
    except:
        raise GenericErrorException(sys.exc_info()[0])


