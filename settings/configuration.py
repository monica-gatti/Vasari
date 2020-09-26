# !/usr/bin/python
# coding=utf-8 
from neomodel import config
config.NEO4J_USERNAME = 'neo4j'
config.NEO4J_PASSWORD = 'neo4j'
#'V@sar!2020'
config.ENCRYPTED_CONNECTION = False
config.MAX_POOL_SIZE = 50
config.DATABASE_URL = 'bolt://neo4j:V@sar!2020@localhost:7687'
