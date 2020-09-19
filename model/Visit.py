from neomodel import (config, StructuredNode, StringProperty, FloatProperty, DateTimeFormatProperty,
    RelationshipTo, StructuredRel, DoesNotExist, db, Traversal, match)
from model.CulturalObject import *
from model.Visitor import *
from datetime import datetime, timedelta

class Visit:
    def __init__(self, visitor, culturalObject, visitDatetime, type, strength, value, precision):
        self.visitor = visitor
        self.culturalObject = culturalObject
        self.visitDatetime = visitDatetime
        self.type = type
        self.strength = strength
        self.value = value
        self.precision = precision
    @property
    def serialize(self):
        return {
        'visitor': self.visitor.ID,
        'culturalObject': self.culturalObject.ID,
        'visitDatetime': self.visitDatetime,
        'type': self.type,
        'strength': self.strength,
        'value': self.value,
        'precision': self.precision
    }

def get_online_visits_to_cultural_object(culturalobject_id, datefrom, dateto):
    #try:
        culturalObject = CulturalObject.nodes.get(ID=culturalobject_id) 
        definition = dict(node_class=Visitor, direction=match.INCOMING ,
                  relation_type='HAS_VISITED_ONLINE', model=HasVisitedOnlineRelationship)
        relations_traversal = Traversal(culturalObject, 'HAS_VISITED_ONLINE', definition)
        all_object_relations = relations_traversal.all()                                                                                                                   
        list_of_visitors = list(all_object_relations)
        list_of_visits = []
        print(type(datefrom))
        for visitor in list_of_visitors:
            rel = visitor.hasVisitedOnline.relationship(culturalObject)
            visit = Visit(visitor, culturalObject, rel.visitDatetime, rel.type, precision=None, value=None, strength=rel.strength)
            if(rel.visitDatetime >= datefrom and rel.visitDatetime < dateto):
                list_of_visits.append(visit)
        return dict(json_visits = [visit.serialize for visit in list_of_visits])
    #except Exception as e:
    #    raise GenericErrorException(sys.exc_info()[0]) 


def get_proximity_visits_to_cultural_object(culturalobject_id, datefrom, dateto):#datefrom, dateto,culturalobject_id):
    #try:
        culturalObject = CulturalObject.nodes.get(ID=culturalobject_id) 
        definition = dict(node_class=Visitor, direction=match.INCOMING ,
                  relation_type='HAS_VISITED_INPROXIMITY', model=HasVisitedInProximityRelationship)
        relations_traversal = Traversal(culturalObject, 'HAS_VISITED_INPROXIMITY', definition)
        all_object_relations = relations_traversal.all()                                                                                                                   
        list_of_visitors = list(all_object_relations)
        list_of_visits = []
        for visitor in list_of_visitors:
            rel = visitor.hasVisitedInProximity.relationship(culturalObject)
            visit = Visit(visitor, culturalObject, rel.visitDatetime, rel.type, precision=rel.precision, value=None, strength=None)
            if(rel.visitDatetime >= datefrom and rel.visitDatetime < dateto):
                list_of_visits.append(visit)
        return dict(json_visits = [visit.serialize for visit in list_of_visits])
    #except Exception as e:
    #    raise GenericErrorException(sys.exc_info()[0]) 

def get_VRAR_interactions_with_cultural_object(culturalobject_id, datefrom, dateto):#datefrom, dateto,culturalobject_id):
    #try:
        culturalObject = CulturalObject.nodes.get(ID=culturalobject_id) 
        definition = dict(node_class=Visitor, direction=match.INCOMING ,
                  relation_type='HAS_INTERACTED_VRAR', model=HasVisitedInProximityRelationship)
        relations_traversal = Traversal(culturalObject, 'HAS_INTERACTED_VRAR', definition)
        all_object_relations = relations_traversal.all()                                                                                                                   
        list_of_visitors = list(all_object_relations)
        list_of_visits = []
        for visitor in list_of_visitors:
            rel = visitor.hasInteractedVRAR.relationship(culturalObject)
            visit = Visit(visitor, culturalObject, rel.visitDatetime, rel.type, precision=None, value=rel.value, strength=None)
            if(rel.visitDatetime >= datefrom and rel.visitDatetime < dateto):
                list_of_visits.append(visit)
        return dict(json_visits = [visit.serialize for visit in list_of_visits])
    #except Exception as e:
    #    raise GenericErrorException(sys.exc_info()[0]) 

def get_number_of_visits_to_cultural_object(culturalobject_id, datefrom, dateto):
    culturalObject = CulturalObject.nodes.get(ID=culturalobject_id)
    online = get_online_visits_to_cultural_object(culturalobject_id, datefrom, dateto)
    interaction = get_VRAR_interactions_with_cultural_object(culturalobject_id, datefrom, dateto)
    offline = get_proximity_visits_to_cultural_object(culturalobject_id, datefrom, dateto)
    numVisits = {"DateFrom":datefrom.strftime("%m/%d/%Y, %H:%M:%S"), "DateTo":dateto.strftime("%m/%d/%Y, %H:%M:%S"), "CulturalObjectID":culturalobject_id, "2DVisits":len(online['json_visits']), "3DVisits":len(interaction['json_visits']), "offlineVisits":len(offline['json_visits'])} 
    return numVisits

def get_cumulative_number_of_visits_to_cultural_object_day(culturalobject_id, datefrom, dateto):
    culturalObject = CulturalObject.nodes.get(ID=culturalobject_id)
    minutes = 5
    minutes_added = timedelta(minutes = minutes)
    dtUp = datefrom + minutes_added
    dtBottom = datefrom
    cumulateVisitsList = [] 
    while(dtUp < dateto):
        print('dtUp' + dtUp.strftime("%m/%d/%Y, %H:%M:%S"))
        print('dtBottom' + dtBottom.strftime("%m/%d/%Y, %H:%M:%S"))
        online = get_online_visits_to_cultural_object(culturalobject_id, dtBottom, dtUp)
        interaction = get_VRAR_interactions_with_cultural_object(culturalobject_id, dtBottom, dtUp)
        offline = get_proximity_visits_to_cultural_object(culturalobject_id, dtBottom, dtUp)
        numVisits = {"DateFrom":dtBottom.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "DateTo":dtUp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "CulturalObjectID":culturalobject_id, "2DVisits":len(online['json_visits']), "3DVisits":len(interaction['json_visits']), "offlineVisits":len(offline['json_visits'])} 
        cumulateVisitsList.append(numVisits)
        dtBottom = dtUp    
        dtUp = dtUp + minutes_added
    return cumulateVisitsList

    
def get_cumulative_number_of_visits_to_cultural_object_year(culturalobject_id, datefrom, dateto):
    culturalObject = CulturalObject.nodes.get(ID=culturalobject_id)
    days = 1
    days_added = timedelta(days = days)
    dateStartOfDay = datetime(year=datefrom.year, month=datefrom.month, day=datefrom.day)
    print('dateStartOfDay' + dateStartOfDay.strftime("%m/%d/%Y, %H:%M:%S"))
    dtUp = dateStartOfDay + days_added
    dtBottom = dateStartOfDay
    cumulateVisitsList = [] 
    while(dtUp < dateto):
        print('dtUp' + dtUp.strftime("%m/%d/%Y, %H:%M:%S"))
        print('dtBottom' + dtBottom.strftime("%m/%d/%Y, %H:%M:%S"))
        online = get_online_visits_to_cultural_object(culturalobject_id, dtBottom, dtUp)
        interaction = get_VRAR_interactions_with_cultural_object(culturalobject_id, dtBottom, dtUp)
        offline = get_proximity_visits_to_cultural_object(culturalobject_id, dtBottom, dtUp)
        numVisits = {"DateFrom":dtBottom.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "DateTo":dtUp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "CulturalObjectID":culturalobject_id, "2DVisits":len(online['json_visits']), "3DVisits":len(interaction['json_visits']), "offlineVisits":len(offline['json_visits'])} 
        cumulateVisitsList.append(numVisits)
        dtBottom = dtUp    
        dtUp = dtUp + days_added
    return cumulateVisitsList