import os
import json
import traceback
import requests
from errors.errors import CallExternalServiceError
from google.cloud import pubsub_v1
from validators.validators import validar_resultado_consumo_servicio

# Constantes
PATH_TOPIC = os.getenv("PATH_TOPIC_MASIVAS")
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

# Función retorna el enpoint del servicio de usuarios
def obtener_endpoint_usuarios():
    return os.getenv('GESTORUSUARIOS_ADDRESS')

# Función retorna el enpoint del servicio de usuarios
def obtener_headers_usuarios():
    headers = {
        # "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        "X-API-Key": "a033d2c0",
        "Content-Type": "application/json"
    }
    return headers

# Funcion que hace el consumo POST de un servicio externo
def consumir_servicio_usuarios(data):
    try:
        response = requests.post(obtener_endpoint_usuarios(), json=data, headers=obtener_headers_usuarios())
        response.raise_for_status()
        validar_resultado_consumo_servicio(response)
        return response.json()
    except requests.exceptions.HTTPError as e:
        traceback.print_exc()
        raise CallExternalServiceError