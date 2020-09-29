# !/usr/bin/python
# coding=utf-8 
from neomodel import config
import os

app_environment = os.environ['VASARI_ENV']
print(app_environment)
if (app_environment == 'local'):
    config.NEO4J_USERNAME = 'neo4j'
    config.NEO4J_PASSWORD = 'neo4j'
    #'V@sar!2020'
    config.ENCRYPTED_CONNECTION = False
    config.MAX_POOL_SIZE = 50
    config.DATABASE_URL = 'bolt://neo4j:V@sar!2020@0.0.0.0:7687'
elif (app_environment == 'container'):
    config.NEO4J_USERNAME = 'neo4j'
    config.NEO4J_PASSWORD = 'test'
    config.ENCRYPTED_CONNECTION = False
    config.MAX_POOL_SIZE = 50
    config.DATABASE_URL = 'bolt://neo4j:V@sar!2020@:data7687'
