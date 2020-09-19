from flask import Flask
from flask_restplus import Api
from controller.CulturalSiteController import culturalsite_bp
from controller.CulturalCollectionController import culturalcollection_bp
from controller.CulturalObjectController import culturalobject_bp
from controller.VisitorController import visitor_bp
from controller.VisitController import visit_bp
import logging

app = Flask(__name__)
api = Api(app, version="1.0", title="Vasari API", description="List, get, create, update a CulturalSite",)

app.register_blueprint(culturalsite_bp)
app.register_blueprint(culturalcollection_bp)
app.register_blueprint(culturalobject_bp)
app.register_blueprint(visitor_bp)
app.register_blueprint(visit_bp)

app.run(debug=True)