# !/usr/bin/python
# coding=utf-8
from flask import Flask
from flask_restplus import Api
from controller.CulturalSiteController import culturalsite_bp
from controller.CulturalCollectionController import culturalcollection_bp
from controller.CulturalObjectController import culturalobject_bp
from controller.VisitorController import visitor_bp
from controller.VisitController import visit_bp
import logging
import os
from neomodel import config

app = Flask(__name__)
api = Api(app, version="1.0", title="Vasari API", description="List, get, create, update a CulturalSite",)

app.register_blueprint(culturalsite_bp)
app.register_blueprint(culturalcollection_bp)
app.register_blueprint(culturalobject_bp)
app.register_blueprint(visitor_bp)
app.register_blueprint(visit_bp)

if __name__ == '__main__':
    app_environment = os.environ['VASARI_ENV']
    config.NEO4J_USERNAME = os.environ['NEO4J_USERNAME']
    config.NEO4J_PASSWORD = os.environ['NEO4J_USERNAME']
    if (app_environment == 'local'):
        config.DATABASE_URL = 'bolt://neo4j:gfd@localhost:7687' 
    elif (app_environment == 'container'):
        config.DATABASE_URL = 'bolt://neo4j:test@database:7687' # os.environ['NEO4J_BOLT_URL']
    config.ENCRYPTED_CONNECTION = False
    config.MAX_POOL_SIZE = 50
    #app.run(debug=True)
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
