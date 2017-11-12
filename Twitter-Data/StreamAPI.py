#!/usr/bin/python

#Config
import app_config
import Kafka as kk
from app_config import custom_logger
logger=custom_logger(__name__,'logs/stream.log')

#Other Libraries Required
import json, time
import tweepy as tw
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

#Twitter Configuration
auth = tw.OAuthHandler(app_config.CONSUMER_KEY, app_config.CONSUMER_SECRET)
auth.set_access_token(app_config.ACCESS_TOKEN, app_config.ACCESS_SECRET)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Kafka Setup
topic = b'tweet-stream'
kafka_instance = kk.kafka_instance()



SEARCH_GEO_CODE = [113.03, -39.06, 154.73, -12.28]
class StdOutListener(StreamListener):
    def __init__(self,api):
        self.api = api
        super(StreamListener,self).__init__()
    def on_data(self, data):
        #Use Tweets, we will send to Queue
        tweet = json.loads(data)
        try:
            kafka_instance.send(topic,tweet)
        except Exception as e:
            logger.error("Error sending to Kafka")
            logger.error(e)
            pass

    def on_status(selft,status):
        logger.info(status)

    def on_error(self, status):
        #Log error and keep alive
        logger.error(status)
        if status == 420:
            self.on_timeout()
    
    def on_timeout(self):
        logger.info("Sleeping...")
        time.sleep(600)
        return

    def on_disconnect(self,notice):
        logger.info(notice)
        return

#Start the Stream
listen = StdOutListener(api)
stream = Stream(auth, listen)
alive = True
while alive:
    try:
        stream.filter(locations=SEARCH_GEO_CODE)
        alive = False
        logger.info("Stream Ended")
    except Exception as e:
        logger.error("Error handled..")
        logger.error(e)
        stream.disconnect()
        alive = True
        time.sleep(600)


