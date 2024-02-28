import os
import json
from google.cloud import pubsub_v1

# Constantes
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("PATH_PUBSUB_KEY")
PATH_TOPIC = os.getenv("PATH_TOPIC")
def formatDateTimeToUTC(dateTime):
    return dateTime.split('.')[0].replace(' ', 'T')

# Funcion para envio de mensaje via pubsub
def publicar_pub_sub(args):
    # Creamos el ciente publihser
    publisher = pubsub_v1.PublisherClient()
    args = json.dumps(args).encode('utf-8')
    messege_published = publisher.publish(PATH_TOPIC, args)