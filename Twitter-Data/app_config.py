import logging
import sys

#Database
import pymongo
from pymongo import MongoClient
import secret

#Logging
def setup_custom_logger(name,fileLocation):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(fileLocation, mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    #logging.basicConfig(filename=fileLocation,level=logging.INFO)
    return logger

#Database
def MongoConnection():
    client = MongoClient(secret.HOST)
    db = client.twitter
    collection = db.tweets
    return collection
    
