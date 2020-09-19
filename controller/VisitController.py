from flask import Flask, Blueprint,json, request
from flask_restplus import Api, Namespace, Resource, fields, reqparse
from model.CulturalObject import *
from model.Visitor import *
from model.Visit import *
from view.VisitView import *
from datetime import datetime
from model.CustomsExceptions import *
from flask_restful import inputs
import urllib.parse

visit_ns = Namespace('Visit_ns')
visit_bp = Blueprint('visit_bp', __name__, url_prefix='/visit_api')
visit_api = Api(visit_bp, version='0.1')
visit_api.add_namespace(visit_ns)

id_parser = reqparse.RequestParser()
id_parser.add_argument('datefrom', help='Insert a String with format 2020-01-01T00:00:00.000Z')
id_parser.add_argument('dateto', help='Insert a String with format 2020-12-31T23:59:59.999Z')

@visit_ns.route('/onlinevisits/<string:culturalobject_id>')
@visit_ns.doc(parser=id_parser)
class Collection(Resource):
    def get(self, culturalobject_id):
        '''Returns the list of online visits for this cultural object in the period from-to'''
        args = id_parser.parse_args()
        dtfrom = datetime.strptime(urllib.parse.unquote(args['datefrom']),"%Y-%m-%dT%H:%M:%S.%fZ")
        dtto = datetime.strptime(urllib.parse.unquote(args['dateto']),"%Y-%m-%dT%H:%M:%S.%fZ")
        try:
            return get_visits_to_cultural_object_json(get_online_visits_to_cultural_object(culturalobject_id, dtfrom, dtto))
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@visit_ns.route('/inproximityvisits/<string:culturalobject_id>')
@visit_ns.doc(parser=id_parser)
class Collection(Resource):
    def get(self, culturalobject_id):
        '''Returns the list of proximity visits for this cultural object in the period from-to'''
        args = id_parser.parse_args()
        dtfrom = datetime.strptime(urllib.parse.unquote(args['datefrom']),"%Y-%m-%dT%H:%M:%S.%fZ")
        dtto = datetime.strptime(urllib.parse.unquote(args['dateto']),"%Y-%m-%dT%H:%M:%S.%fZ")
        try:
            return get_visits_to_cultural_object_json(get_proximity_visits_to_cultural_object(culturalobject_id, dtfrom, dtto))
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@visit_ns.route('/arvrinteractions/<string:culturalobject_id>')
@visit_ns.doc(parser=id_parser)
class Collection(Resource):
    def get(self, culturalobject_id):
        '''Returns the list of VR AR interactions for this cultural object in the period from-to'''
        args = id_parser.parse_args()
        dtfrom = datetime.strptime(urllib.parse.unquote(args['datefrom']),"%Y-%m-%dT%H:%M:%S.%fZ")
        dtto = datetime.strptime(urllib.parse.unquote(args['dateto']),"%Y-%m-%dT%H:%M:%S.%fZ")
        try:
            return get_visits_to_cultural_object_json(get_VRAR_interactions_with_cultural_object(culturalobject_id, dtfrom, dtto))
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@visit_ns.route('/visits/<string:culturalobject_id>/visitorsnumber')
@visit_ns.doc(parser=id_parser)
class Collection(Resource):
    def get(self, culturalobject_id):
        '''Returns the number of 2D, 3D, off-line visits for the cultural object in the period from-to for every 5 minutes interval'''
        args = id_parser.parse_args()
        dtfrom = datetime.strptime(urllib.parse.unquote(args['datefrom']),"%Y-%m-%dT%H:%M:%S.%fZ")
        dtto = datetime.strptime(urllib.parse.unquote(args['dateto']),"%Y-%m-%dT%H:%M:%S.%fZ")
        print(type(dtfrom))
        try:
            return get_number_of_visits_to_cultural_object(culturalobject_id, dtfrom, dtto)
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@visit_ns.route('/visits/<string:culturalobject_id>/cumulativevisitorsnumberday')
@visit_ns.doc(parser=id_parser)
class Collection(Resource):
    def get(self, culturalobject_id):
        '''Returns the number of 2D, 3D, off-line visits for the cultural object in the period from-to for every 5 minutes interval'''
        args = id_parser.parse_args()
        dtfrom = datetime.strptime(urllib.parse.unquote(args['datefrom']),"%Y-%m-%dT%H:%M:%S.%fZ")
        dtto = datetime.strptime(urllib.parse.unquote(args['dateto']),"%Y-%m-%dT%H:%M:%S.%fZ")
        print(type(dtfrom))
        try:
            return get_cumulative_number_of_visits_to_cultural_object_day(culturalobject_id, dtfrom, dtto)
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

@visit_ns.route('/visits/<string:culturalobject_id>/cumulativevisitorsnumberyear')
@visit_ns.doc(parser=id_parser)
class Collection(Resource):
    def get(self, culturalobject_id):
        '''Returns the number of 2D, 3D, off-line visits for the cultural object in the period from-to for every day interval '''
        args = id_parser.parse_args()
        dtfrom = datetime.strptime(urllib.parse.unquote(args['datefrom']),"%Y-%m-%dT%H:%M:%S.%fZ")
        dtto = datetime.strptime(urllib.parse.unquote(args['dateto']),"%Y-%m-%dT%H:%M:%S.%fZ")
        try:
            return get_cumulative_number_of_visits_to_cultural_object_year(culturalobject_id, dtfrom, dtto)
        except ObjectNotFoundException as c:
            return "Error:{0}".format(c), 404
        except Exception as e:
            return "Error:{0}".format(e), 500

