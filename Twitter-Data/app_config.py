import logging
import sys

#Constants
CONSUMER_KEY = 'Urze1T1ByqrVoBWwCS1luYRn0'
CONSUMER_SECRET = 'BTHSgsjhcQM6051rQKywSqyypVb2PPssocSKEqErX6x3BeDtyF'
ACCESS_TOKEN = '140966719-9hjuMlsm5YetkZiKZZdbsCT6smsanfTuI1gkdPN5'
ACCESS_SECRET = 'N3M816Qv8vme09zW5e8Ttr5Fy3IhR7cI0wciwOSWog9NS'

CONSUMER_KEY_UNI = 'PBsXp8rZd59wj9UlHfhskr13a'
CONSUMER_SECRET_UNI = 'I3SX0m3UAXCK91LVIHj3NpZlLXfukYybZXYSZhrPEG5zuoOPw8'
ACCESS_TOKEN_UNI = '877752456838381573-0hMJuQTKZ1yCA0TfoU78HF8vDDxoE8I'
ACCESS_SECRET_UNI = 'HhuZ6dEtsvilSgIxeEYU1TtVjLMs178CpgvuVcdU3umfi'

# Keyword List
WORDS = ['australia','melbourne','colombia']

# Kafka
KAFKA_PORT = 'localhost:9092'

#Logging
def custom_logger(name,fileLocation):
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
    return logger