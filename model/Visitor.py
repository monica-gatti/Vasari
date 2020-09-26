# !/usr/bin/python
# coding=utf-8 
from neomodel import (config, StructuredNode, StringProperty, FloatProperty, DateTimeFormatProperty,
    RelationshipTo, StructuredRel, DoesNotExist, db, Traversal, match)
from datetime import datetime
from settings import *
from model.CulturalObject import *
from model.CustomsExceptions import *
from model.HasVisitedOnlineRelationship import *
from model.HasVisitedInProximityRelationship import *
from model.HasInteractedVRARRelationship import *
import sys, logging


class Visitor(StructuredNode):
    ID = StringProperty(unique_index=True, required=True)
    hasVisitedOnline = RelationshipTo(CulturalObject, 'HAS_VISITED_ONLINE', model=HasVisitedOnlineRelationship)
    hasVisitedInProximity = RelationshipTo(CulturalObject, 'HAS_VISITED_INPROXIMITY', model=HasVisitedInProximityRelationship)
    hasInteractedVRAR = RelationshipTo(CulturalObject, 'HAS_INTERACTED_VRAR', model=HasInteractedVRARRelationship)
    @property
    def serialize(self):
        return {
            'ID': self.ID
    }

def visitor_doesnt_exist(visitor_id):
    try:
        visitor = Visitor.nodes.get(ID=visitor_id) 
    except DoesNotExist:
        return True
    return False

def get_visitor(visitor_id):
    try:
        visitor = Visitor.nodes.get(ID=visitor_id)
        return dict(visitor.serialize)
    except DoesNotExist:
        raise ObjectNotFoundException(visitor_id)
    except:
        raise GenericErrorException(sys.exc_info()[0])
def get_visitors():
    try:
        visitors = Visitor.nodes                                                                                                                            
        list_of_visitors = list(visitors)
        return dict(json_visitors = [visitor.serialize for visitor in list_of_visitors])
    except Exception as e:
        raise GenericErrorException(sys.exc_info()[0]) 
def visitor_create(json_data):
    try:
        visitor = Visitor(ID=json_data.get("ID"));
        visitor.save()
        return dict(visitor.serialize)
    except Exception as e:
        raise GenericErrorException(sys.exc_info()[0])    
def visitor_delete(visitor_id):
    try:
        visitor = Visitor.nodes.get(ID=visitor_id);
        visitor.delete()
    except DoesNotExist:
        raise ObjectNotFoundException(visitor_id)
    except:
        raise GenericErrorException(sys.exc_info()[0])

def get_visitors_of_cultural_objects(culturalobject_id):#datefrom, dateto,culturalobject_id):
    #try:
        culturalObject = CulturalObject.nodes.get(ID=culturalobject_id) 
        definition = dict(node_class=Visitor, direction=match.INCOMING ,
                  relation_type=None, model=HasVisitedOnlineRelationship)
        relations_traversal = Traversal(culturalObject, 'HAS_VISITED_ONLINE', definition)
        all_object_relations = relations_traversal.all()                                                                                                                   
        list_of_visitors = list(all_object_relations)
        for visitor in list_of_visitors:
            rel = visitor.HasVisitedOnlineRelationship.relationship(culturalObject)
            print(rel.Type)
            logging.info(rel.TYPES)
        return dict(json_visitors = [visitor.serialize for visitor in list_of_visitors])
    #except Exception as e:
    #    raise GenericErrorException(sys.exc_info()[0]) 


def get_culturalobjects_visited_by_visitor(visitor_id):
#try:
    visitor = Visitor.nodes.get(ID=visitor_id)
    definition = dict(node_class=CulturalObject, direction=match.OUTGOING,
                relation_type=None, model=HasVisitedOnlineRelationship)
    relations_traversal = Traversal(visitor, 'HAS_VISITED_ONLINE', definition)
    all_object_relations = relations_traversal.all()                                                                                                                   
    list_of_cultural_objects = list(all_object_relations)
    #for visitor in list_of_visitors:
    #    logging.info(visitor)
    return dict(json_visitors = [culturalobject.serialize for culturalobject in list_of_cultural_objects ])
#except Exception as e:
#    raise GenericErrorException(sys.exc_info()[0]) 

