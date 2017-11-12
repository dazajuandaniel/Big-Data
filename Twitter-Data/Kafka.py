#!/usr/bin/python

#Imports
import app_config, sys
import kafka
from kafka import kafkaProducer, kafkaClient
import json

# Kafka Settings
def kafka_instance():
    try:
        producer = KafkaProducer(bootstrap_servers=app_config.KAFKA_PORT,value_serializer = lambda v: json.dumps(v).encode('utf-8'))
        app_config.custom_logger("Kafka Started")
        return producer
    except Exception as e:
        app_config.custom_logger("Error in Kafka Instance")
        app_config.custom_logger(e)
        return sys.exit()