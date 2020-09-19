from flask import Flask, Blueprint,json, request
from flask_restplus import Api, Namespace, Resource, fields, reqparse
from datetime import datetime
from model.CulturalCollection import *
from model.CulturalSite import *
from model.CulturalObject import CulturalObject
from view.CulturalSiteView import *
from model.CustomsExceptions import *

culturalsite_ns = Namespace('culturalsites_ns')
culturalsite_bp = Blueprint('culturalsite_bp', __name__, url_prefix='/culturalsite_api')
culturalsite_api = Api(culturalsite_bp, version='0.1')
culturalsite_api.add_namespace(culturalsite_ns)

insert_cs_data = culturalsite_ns.model("Insert_cs_data",{"ID":fields.String(description="ID, unique identifier of the Cultural Site", required=True),
                                     "Name": fields.String(description="Name of the Cultural Site, for instance 'Musee du Louvre' or 'Scavi Archeologici di Pompei'", required=True)})
update_cs_data = culturalsite_ns.model("Update_cs_data",{"Name": fields.String(description="Name of the Cultural Site, for instance 'Musee du Louvre' or 'Scavi Archeologici di Pompei'", required=True)})

link_cs_data_to_cc = culturalsite_ns.model("Link_cs_data_to_cc",{"dateFrom": fields.DateTime(description="DateFrom, when a Cultural Collection starts to be associated to a Cultural Site", required=True),
                                     "dateTo": fields.DateTime(description="dateTo, when a Cultural Collection ends to be associated to a Cultural Site", required=True)})

@culturalsite_ns.route('/culturalsites/<string:culturalsite_id>')
class Site(Resource):
    #@api.doc(description='culturalsite_id is the unique identifier')
    def get(self, culturalsite_id):
        '''Fetch a given Cultural Site'''
        try:
            return get_cultural_site_json(get_cultural_site(culturalsite_id))
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500
    @culturalsite_ns.expect(update_cs_data)
    def post(self, culturalsite_id):
        '''Update a given Cultural Site'''
        try:
            json_data = request.json
            culturalsite_update(culturalsite_id,json_data)
            return get_cultural_site_json(get_cultural_site(culturalsite_id)), 200
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except ArgumentOutOfRangeException as a:
            return "Error:{0}".format(c), 500
        except Exception as e:
            return "Error:{0}".format(e), 500        
    def delete(self, culturalsite_id):
        '''Delete a given Cultural Site'''
        try:
            culturalsite_delete(culturalsite_id)
            return 'removed', 200
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@culturalsite_ns.route('/culturalsites')
class Sites(Resource):
    @culturalsite_ns.expect(insert_cs_data)
    def post(self):
        '''Create a new Cultural Site'''
        try:
            json_data = request.json
            culturalSite = culturalsite_create(json_data)
            return get_cultural_site_json(culturalSite), 201
        except Exception as e:
            return "Error:{0}".format(e), 500 
    def get(self):
        '''Retrieve all Cultural Sites'''
        #try:
        culturalSites = get_cultural_sites()
        return get_cultural_site_json(culturalSites), 200
        #except Exception as e:
        #    return "Error:{0}".format(e), 500

@culturalsite_ns.route('/culturalsites/<string:culturalsite_id>/culturalcollections/<string:culturalcollection_id>')
@culturalsite_ns.expect(link_cs_data_to_cc)
class SiteCollectionLink(Resource):
    def post(self, culturalsite_id, culturalcollection_id):
        '''Link a given Cultural Collection to a Cultural Site'''
        if culturalsite_doesnt_exist(culturalsite_id) is True:
            return "Cultural Site {0} doesn't exist".format(culturalsite_id), 404 
        if culturalcollection_doesnt_exist(culturalcollection_id) is True:
            return "Cultural Collection {0} doesn't exist".format(culturalcollection_id), 404 
        try:
            culturalSite = CulturalSite.nodes.get(ID=culturalsite_id);
            culturalCollection = CulturalCollection.nodes.get(ID=culturalcollection_id);
            json_data = request.json       
            fromDatetime= datetime.strptime(json_data.get('dateFrom'),"%Y-%m-%dT%H:%M:%S.%fZ")
            toDatetime= datetime.strptime(json_data.get('dateTo'),"%Y-%m-%dT%H:%M:%S.%fZ")
            rel = culturalSite.exhibits.connect(culturalCollection,{'dateFrom': fromDatetime, 'dateTo': toDatetime})
            rel.save()
            return json.dumps(dict(culturalSite.serialize))
        except Exception as e:
            return "Error:{0}".format(e), 500
@culturalsite_ns.route('/culturalsites/<string:culturalsite_id>/culturalobjects/<string:culturalobject_id>')
class SiteCollectionLink(Resource):
    def post(self, culturalsite_id, culturalobject_id):
        '''Link a given Cultural Collection to a Cultural Object'''
        if culturalsite_doesnt_exist(culturalsite_id) is True:
            return "Cultural Site {0} doesn't exist".format(culturalsite_id), 404 
        if culturalobject_doesnt_exist(culturalobject_id) is True:
            return "Cultural Object {0} doesn't exist".format(culturalobject_id), 404 
        try:
            culturalSite = CulturalSite.nodes.get(ID=culturalsite_id)
            culturalObject = CulturalObject.nodes.get(ID=culturalobject_id)
            rel = culturalSite.owns.connect(culturalObject)
            culturalSite.save()
            return json.dumps(dict(culturalSite.serialize))
        except Exception as e:
            return "Error:{0}".format(e), 500     