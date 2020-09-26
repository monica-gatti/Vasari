# !/usr/bin/python
# coding=utf-8 
from flask import Flask, Blueprint, json, request
from flask_restplus import Api, Namespace, Resource, fields
from datetime import datetime
from model.CulturalObject import CulturalObject, culturalobject_doesnt_exist
from model.Visitor import *
from view.VisitorView import *
from model.CustomsExceptions import *
from datetime import datetime
from model.CustomsExceptions import *
import sys

visitor_ns = Namespace('Visitor_ns')
visitor_bp = Blueprint('visitor_bp', __name__, url_prefix='/visitor_api')
visitor_api = Api(visitor_bp, version='0.1')
visitor_api.add_namespace(visitor_ns)

insert_vi_data = visitor_ns.model("Insert_vi_data",{"ID":fields.String(description="ID", required=True)})
has_visited_online_data = visitor_ns.model("has_visited_online_data",{"visitDatetime": fields.DateTime(description="The datetime of the visit", required=True),
                                    "strength":fields.Float(description="Strength of the relationship", required=True)})
has_visited_inproximity_data = visitor_ns.model("has_visited_inproximity_data",{"visitDatetime": fields.DateTime(description="The datetime of the visit", required=True),
                                    "precision":fields.Float(description="Precision of the position, required for type=off-line", required=False)})
has_interacted_ARVR_data = visitor_ns.model("has_interacted_ARVR_data",{"visitDatetime": fields.DateTime(description="The datetime of the visit", required=True),
                                    "value":fields.String(description="Value from the QRCode", required=True)})


@visitor_ns.route('/visitor/<string:visitor_id>')
class VisitorR(Resource):
    #@api.doc(description='visitor_id is the unique identifier, 404 if not found')
    def get(self, visitor_id):
        '''Fetch a given Visitor'''
        try:
            return get_visitor_json(get_visitor(visitor_id))
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500
    def delete(self, visitor_id):
        '''Delete a given Visitor'''
        try:
            visitor_delete(visitor_id)
            return 'removed', 200
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@visitor_ns.route('/visitors')
class Visitors(Resource):
    @visitor_ns.expect(insert_vi_data)
    def post(self):
        '''Create a new Visitor'''
        try:
            json_data = request.json
            visitor_id = json_data.get('ID')
            visitor = visitor_create(json_data)
            return get_visitor_json(visitor), 201
        except Exception as e:
            return "Error:{0}".format(e), 500 
    def get(self):
        '''Retrieve all Cultural Collections'''
        try:
            visitors = get_visitors()
            return get_visitor_json(visitors), 200
        except Exception as e:
            return "Error:{0}".format(e), 500    

@visitor_ns.route('/visitors/<string:visitor_id>/culturalobjectsvisitedonline/<string:culturalobject_id>')
@visitor_ns.expect(has_visited_online_data)
class HasVisitedOnlineCulturalObject(Resource):
    def post(self, visitor_id, culturalobject_id):
        '''Link a given visitor to a Cultural Object with online interaction mobile app-web site'''
        if visitor_doesnt_exist(visitor_id) is True:
            return "Visitor {0} doesn't exist".format(visitor_id), 404 
        if culturalobject_doesnt_exist(culturalobject_id) is True:
            return "Cultural Object {0} doesn't exist".format(culturalobject_id), 404 
        try:
            visitor = Visitor.nodes.get(ID=visitor_id);
            culturalObject = CulturalObject.nodes.get(ID=culturalobject_id);
            json_data = request.json       
            visitDatetime= datetime.strptime(json_data.get('visitDatetime'),"%Y-%m-%dT%H:%M:%S.%fZ")
            strength = float(json_data.get('strength'))
            rel = visitor.hasVisitedOnline.connect(culturalObject,{'visitDatetime': visitDatetime, 'type': '2D', 'strength':strength})
            rel.save()
            return json.dumps(dict(visitor.serialize))
        except Exception as e:
            return "Error:{0}".format(e), 500 

@visitor_ns.route('/visitors/<string:visitor_id>/culturalobjectsvisitedinproximity/<string:culturalobject_id>')
@visitor_ns.expect(has_visited_inproximity_data)
class HasVisitedInProximityCulturalObject(Resource):
    def post(self, visitor_id, culturalobject_id):
        '''Link a given visitor to a Cultural Object with off-line interaction wifi-beacon'''
        if visitor_doesnt_exist(visitor_id) is True:
            return "Visitor {0} doesn't exist".format(visitor_id), 404 
        if culturalobject_doesnt_exist(culturalobject_id) is True:
            return "Cultural Object {0} doesn't exist".format(culturalobject_id), 404 
        try:
            visitor = Visitor.nodes.get(ID=visitor_id);
            culturalObject = CulturalObject.nodes.get(ID=culturalobject_id);
            json_data = request.json       
            visitDatetime= datetime.strptime(json_data.get('visitDatetime'),"%Y-%m-%dT%H:%M:%S.%fZ")
            precision = float(json_data.get('precision'))
            rel = visitor.hasVisitedInProximity.connect(culturalObject,{'visitDatetime': visitDatetime, 'type': 'off-line', 'precision':precision})
            rel.save()
            return json.dumps(dict(visitor.serialize))
        except Exception as e:
            return "Error:{0}".format(e), 500

@visitor_ns.route('/visitors/<string:visitor_id>/culturalobjectinteractedVRAR/<string:culturalobject_id>')
@visitor_ns.expect(has_interacted_ARVR_data)
class HasInteractedVRARwithCulturalObject(Resource):
    def post(self, visitor_id, culturalobject_id):
        '''Link a given visitor to a Cultural Object with AR VR interaction '''
        if visitor_doesnt_exist(visitor_id) is True:
            return "Visitor {0} doesn't exist".format(visitor_id), 404 
        if culturalobject_doesnt_exist(culturalobject_id) is True:
            return "Cultural Object {0} doesn't exist".format(culturalobject_id), 404 
        try:
            visitor = Visitor.nodes.get(ID=visitor_id);
            culturalObject = CulturalObject.nodes.get(ID=culturalobject_id);
            json_data = request.json       
            visitDatetime= datetime.strptime(json_data.get('visitDatetime'),"%Y-%m-%dT%H:%M:%S.%fZ")
            value = json_data.get('value')
            rel = visitor.hasInteractedVRAR.connect(culturalObject,{'visitDatetime': visitDatetime, 'type': '3D', 'value':value})
            rel.save()
            return json.dumps(dict(visitor.serialize))
        except Exception as e:
            return "Error:{0}".format(e), 500

@visitor_ns.route('/culturalobjects/<string:culturalobject_id>/visitors')
class HasVisitedCulturalObject(Resource):
    def get(self, culturalobject_id):
        '''Get visitors of a Cultural Object'''
        if culturalobject_doesnt_exist(culturalobject_id) is True:
            return "Cultural Object {0} doesn't exist".format(culturalobject_id), 404 
        try:
            visitors = get_visitors_of_cultural_objects(culturalobject_id)
            return json.dumps(visitors)
        except Exception as e:
            return "Error:{0}".format(e), 500 

@visitor_ns.route('/visitors/<string:visitor_id>/cultural_objects')
class VisitedCulturalObject(Resource):
    def get(self, visitor_id):
        '''Get Cultural Objects visited by a visitor'''
        #try:
        cultural_objects = get_culturalobjects_visited_by_visitor(visitor_id)
        return json.dumps(cultural_objects)
        #except Exception as e:
        #    return "Error:{0}".format(e), 500 