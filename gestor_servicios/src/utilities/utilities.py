import os
import json
from google.cloud import pubsub_v1

# Constantes
PATH_TOPIC = os.getenv("PATH_TOPIC")
def formatDateTimeToUTC(dateTime):
    return dateTime.split('.')[0].replace(' ', 'T')

# Funcion para envio de mensaje via pubsub
def publicar_pub_sub(args):
    # Creamos el ciente publihser
    publisher = pubsub_v1.PublisherClient()
    args = json.dumps(args).encode('utf-8')
    messege_published = publisher.publish(PATH_TOPIC, args)
    message_id = messege_published.result()
    print(f"Mensaje publicado con ID: {message_id}")