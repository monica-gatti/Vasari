# !/usr/bin/python
# coding=utf-8
from flask import Flask, Blueprint,json, request
from flask_restplus import Api, Namespace, Resource, fields, reqparse
from werkzeug.contrib.fixers import ProxyFix
from datetime import datetime
from model.CulturalObject import *
from view.CulturalObjectView import *

culturalobject_ns = Namespace('CulturalObject_ns')
culturalobject_bp = Blueprint('culturalobject_bp', __name__, url_prefix='/culturalobject_api')
culturalobject_api = Api(culturalobject_bp, version='0.1')
culturalobject_api.add_namespace(culturalobject_ns)

insert_co_data = culturalobject_ns.model("Insert_co_data",{"ID":fields.String(description="Unique identified of the Cultural Object", required=True),"Name":fields.String(description="Title of the Cultural Object", required=True),
                                     "Room": fields.String(description="Location of the Cultural Object", required=True)})
update_co_data = culturalobject_ns.model("Update_co_data",{"Name":fields.String(description="Title of the Cultural Object", required=True),"Room": fields.String(description="Location of the Cultural Object", required=True)})

@culturalobject_ns.route('/culturalobject/<string:culturalobject_id>')
class Collection(Resource):
    #@api.doc(description='culturalobject_id is the unique identifier')
    def get(self, culturalobject_id):
        '''Fetch a given Cultural Object'''
        try:
            return get_cultural_object_json(get_cultural_object(culturalobject_id))
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500
    @culturalobject_ns.expect(update_co_data)
    def post(self, culturalobject_id):
        '''Update a given Cultural Object'''
        json_data = request.json
        try:
            culturalobject_update(culturalobject_id,json_data)
            return get_cultural_object_json(get_cultural_object(culturalobject_id))
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except ArgumentOutOfRangeException as a:
            return "Error:{0}".format(c), 500
        except Exception as e:
            return "Error:{0}".format(e), 500        
    def delete(self, culturalobject_id):
        '''Delete a given Cultural Object'''
        try:
            culturalobject_delete(culturalobject_id)
            return 'removed', 200
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@culturalobject_ns.route('/culturalobject')
class Objects(Resource):
    @culturalobject_ns.expect(insert_co_data)
    def post(self):
        '''Create a new Cultural Object'''
        try:
            json_data = request.json
            culturalObject = culturalobject_create(json_data)
            return get_cultural_object_json(culturalObject), 201
        except Exception as e:
            return "Error:{0}".format(e), 500
    def get(self):
        '''Retrieve all Cultural Object'''
        try:
            culturalObjects = get_cultural_objects()
            return get_cultural_object_json(culturalObjects), 200
        except Exception as e:
            return "Error:{0}".format(e), 500    

    

