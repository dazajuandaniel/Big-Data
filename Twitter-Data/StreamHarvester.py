#!/usr/bin/python

#Logging
from app_config import setup_custom_logger
logger=setup_custom_logger(__name__,'log/StreamHarvester_uni.log')

#Config Files
import secret

#Other Libraries Required
import sys, json
import tweepy as tw
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import TwitterSentiment as ts

#Twitter Configuration
auth = tw.OAuthHandler(secret.CONSUMER_KEY, secret.CONSUMER_SECRET)
auth.set_access_token(secret.ACCESS_TOKEN, secret.ACCESS_SECRET)
api = tw.API(auth)

#Database Config
collection = app_config.MongoClient()

class StdOutListener(StreamListener):
    def on_data(self, data):
        
        tweet = json.loads(data)
        #Clean Tweet
        clean_tweet_text=ts.processTweet(tweet['text'])
        tweet['clean_text']=clean_tweet_text
        #Avoid Duplicates bu Changind "_id" parameter in DB
        tweet['_id']=tweet['id_str']
        #Include Sentiment Based on TextBlob
        tweet['sentiment']=ts.getSentiment(clean_tweet_text)
        #Store Tweet in MongoDB
        try:
            collection.insert_one(tweet)
            logger.info('Wrote Tweet Succesfully')
        except Exception as e:
            logger.error('Error Ocurred Database Write')
            logger.error(e)

    def on_error(self, status):
        logger.error(status)


if __name__ == '__main__':
    l = StdOutListener()
    stream = Stream(auth, l)

    #Australia Area
    stream.filter(locations=[113.1,-43.7,155.3,-11.7])
    # http://boundingbox.klokantech.com/

