from model.CulturalObject import CulturalObject
from model.IncludesRelationship import IncludesRelationship
from neomodel import (config, StructuredNode, StringProperty, DateTimeFormatProperty,
    RelationshipTo, StructuredRel, db, DoesNotExist, DeflateError)
from datetime import datetime
from settings import *
from model.CustomsExceptions import *
import sys

class CulturalCollection(StructuredNode):
    ID = StringProperty(unique_index=True, required=True)
    Name = StringProperty(unique_index=False, required=True)
    TYPES = {'semantic': 'semantic', 'physic': 'physic'}
    Type = StringProperty(required=False, choices=TYPES)
    Category = StringProperty(unique_index=False, required=False)
    Location = StringProperty(unique_index=False, required=False) 
    includes = RelationshipTo(CulturalObject, 'INCLUDES', model=IncludesRelationship)
    @property
    def serialize(self):
        return {
            'ID': self.ID,
            'Name': self.Name,
            'Type': self.Type,
            'Category': self.Category,
            'Location': self.Location
    }
def culturalcollection_doesnt_exist(culturalcollection_id):
    try:
        culturalCollection = CulturalCollection.nodes.get(ID=culturalcollection_id) 
    except DoesNotExist:
        return True
    return False
def get_cultural_collection(culturalcollection_id):
    try:
        culturalCollection = CulturalCollection.nodes.get(ID=culturalcollection_id)
        return dict(culturalCollection.serialize)
    except DoesNotExist:
        raise ObjectNotFoundException(culturalcollection_id)
    except:
        raise GenericErrorException(sys.exc_info()[0])
def get_cultural_collections():
    try:
        culturalCollections = CulturalCollection.nodes                                                                                                                            
        list_of_culturalCollections = list(culturalCollections)
        return dict(json_cultural_collections = [culturalCollection.serialize for culturalCollection in list_of_culturalCollections])
    except Exception as e:
        raise GenericErrorException(sys.exc_info()[0])   
def culturalcollection_update(culturalcollection_id,json_data):
    try:
        culturalCollection = CulturalCollection.nodes.get(ID=culturalcollection_id);
        culturalCollection.Name= json_data.get("Name")
        culturalCollection.Type=json_data.get("Type")
        culturalCollection.Category=json_data.get("Category")
        culturalCollection.Location=json_data.get("Location")
        culturalCollection.save()
    except DoesNotExist:
        raise ObjectNotFoundException(culturalcollection_id)
    except DeflateError:
        raise ArgumentOutOfRangeException(json_data.get("Type"))
    except:
        raise GenericErrorException(sys.exc_info()[0])
def culturalcollection_create(json_data):
    try:
        culturalCollection = CulturalCollection(ID= json_data.get('ID'), Name= json_data.get('Name'), Type = json_data.get("Type"), Category = json_data.get("Category"), Location = json_data.get("Location"))
        culturalCollection.save()
        return dict(culturalCollection.serialize)
    except Exception as e:
        raise GenericErrorException(sys.exc_info()[0])    
def culturalcollection_delete(culturalcollection_id):
    try:
        culturalCollection = CulturalCollection.nodes.get(ID=culturalcollection_id);
        culturalCollection.delete()
    except DoesNotExist:
        raise ObjectNotFoundException(culturalcollection_id)
    except:
        raise GenericErrorException(sys.exc_info()[0])