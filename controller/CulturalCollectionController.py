from flask import Flask, Blueprint,json, request
from flask_restplus import Api, Namespace, Resource, fields, reqparse
from model.CulturalObject import *
from model.CulturalCollection import *
from view.CulturalCollectionView import *
from datetime import datetime
from model.CustomsExceptions import *

culturalcollection_ns = Namespace('CulturalCollection_ns')
culturalcollection_bp = Blueprint('culturalcollection_bp', __name__, url_prefix='/culturalcollection_api')
culturalcollection_api = Api(culturalcollection_bp, version='0.1')
culturalcollection_api.add_namespace(culturalcollection_ns)

insert_cc_data = culturalcollection_ns.model("Insert_cc_data",{"ID":fields.String(description="ID, unique identifier of the collection", required=True),
                                     "Name": fields.String(description="Name, the title of the Collection/Exhibition", required=True),
                                     "Type": fields.String(description="Type of the collection: physic or semantic based", required=True),
                                     "Category": fields.String(description="Set Category field if Type semantic, for instance 'landscapes' ", required=False),
                                     "Location": fields.String(description="Set Location field if Type physic, for instance 'North Side'", required=False)})
update_cc_data = culturalcollection_ns.model("Update_cc_data",{"Name": fields.String(description="Name, the title of the Collection/Exhibition", required=True),
                                     "Type": fields.String(description="Type of the collection: physic or semantic based", required=True),
                                     "Category": fields.String(description="Set Category field if Type semantic, for instance 'landscapes", required=False),
                                     "Location": fields.String(description="Set Location field if Type physic, for instance 'North Side'", required=False)})
link_cc_data_to_co = culturalcollection_ns.model("Link_cc_data_to_cc",{"dateFrom": fields.DateTime(description="DateFrom, when the Cultural Object starts to be associated to the Cultural Collection", required=True),
                                     "dateTo": fields.DateTime(description="dateTo, when the Cultural Object ends to be associated to the Cultural Collection", required=True)})

@culturalcollection_ns.route('/culturalcollection/<string:culturalcollection_id>')
class Collection(Resource):
    #@api.doc(description='culturalcollection_id is the unique identifier of the Cultural Collection')
    def get(self, culturalcollection_id):
        '''Fetch a given Cultural Collection'''
        try:
            return get_cultural_collection_json(get_cultural_collection(culturalcollection_id))
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500
    @culturalcollection_ns.expect(update_cc_data)
    def post(self, culturalcollection_id):
        '''Update a given Cultural Collection'''
        json_data = request.json
        try:
            culturalcollection_update(culturalcollection_id,json_data)
            return get_cultural_collection_json(get_cultural_collection(culturalcollection_id)), 200
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except ArgumentOutOfRangeException as a:
            return "Error:{0}".format(c), 500
        except Exception as e:
            return "Error:{0}".format(e), 500         
    def delete(self, culturalcollection_id):
        '''Delete a given Cultural Collection'''
        try:
            culturalcollection_delete(culturalcollection_id)
            return 'removed', 200
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@culturalcollection_ns.route('/culturalcollections')
class Collections(Resource):
    @culturalcollection_ns.expect(insert_cc_data)
    def post(self):
        '''Create a new Cultural Collection'''
        try:
            json_data = request.json
            #culturalcollection_id = json_data.get('ID')
            culturalCollection = culturalcollection_create(json_data)
            return get_cultural_collection_json(culturalCollection), 201
        except Exception as e:
            return "Error:{0}".format(e), 500 
    def get(self):
        '''Retrieve all Cultural Collections'''
        try:
            culturalCollections = get_cultural_collections()
            return get_cultural_collection_json(culturalCollections), 200
        except Exception as e:
            return "Error:{0}".format(e), 500    

@culturalcollection_ns.route('/culturalcollections/<string:culturalcollection_id>/culturalobjects/<string:culturalobject_id>')
@culturalcollection_ns.expect(link_cc_data_to_co)
class CollectionLinkObject(Resource):
    def post(self, culturalcollection_id, culturalobject_id):
        '''Link a given Cultural Collection to a Cultural object'''
        if culturalcollection_doesnt_exist(culturalcollection_id) is True:
            return "Cultural Collection {0} doesn't exist".format(culturalcollection_id), 404 
        if culturalobject_doesnt_exist(culturalobject_id) is True:
            return "Cultural Object {0} doesn't exist".format(culturalobject_id), 404 
        try:
            culturalCollection = CulturalCollection.nodes.get(ID=culturalcollection_id);
            culturalObject = CulturalObject.nodes.get(ID=culturalobject_id);
            json_data = request.json       
            fromDatetime= datetime.strptime(json_data.get('dateFrom'),"%Y-%m-%dT%H:%M:%S.%fZ")
            toDatetime= datetime.strptime(json_data.get('dateTo'),"%Y-%m-%dT%H:%M:%S.%fZ")
            rel = culturalCollection.includes.connect(culturalObject,{'dateFrom': fromDatetime, 'dateTo': toDatetime})
            rel.save()
            return json.dumps(dict(culturalCollection.serialize))
        except Exception as e:
            return "Error:{0}".format(e), 500         
    
