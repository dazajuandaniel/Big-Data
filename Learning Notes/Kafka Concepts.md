# Introduction
## [Core Concepts](https://kafka.apache.org/intro)
### Core APIs
* **Producer:** Allows an app to publish to one or more topics.
* **Consumer:** Allows an app to subscribe to one or more topics.
* **Streams:** Allows an app to consume from multiple sources and output to multiple topics.
* **Connector:** Allows building and running reusable producers/consumers.

### Topics
* **Topics:** 
    * Category where messages/records are published.
    * Are always multi-subscriber
* **Producer:**
    * Publishes data to topics
    * Responsible for choosing which record to assign to which partition.
* **Consumers:**
    * Are labeled with a *consumer group* name
    * Each record published to a topic is delivered to one consumer instance within each subscribing consumer group
