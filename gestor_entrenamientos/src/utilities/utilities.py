import os
import json
import requests
import traceback
from google.cloud import pubsub_v1
from errors.errors import CallExternalServiceError
from validators.validators import validar_resultado_consumo_servicio

datos_en_memoria = None

# Constantes
PATH_TOPIC = os.getenv("PATH_TOPIC_ALERTA")
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

# Funcion que hace el consumo GET de gestor de usuarios
def consumir_servicio_usuarios(headers):
    try:
        headers_servicio_usuario = {
            "Authorization": headers['Authorization']
        }
        response = requests.get(url=obtener_endpoint_usuarios(), headers=headers_servicio_usuario)
        validar_resultado_consumo_servicio(response)
        return response.json()
    except requests.exceptions.HTTPError as e: # pragma: no cover
        traceback.print_exc()
        raise CallExternalServiceError      