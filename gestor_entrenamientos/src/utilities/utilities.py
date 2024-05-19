import os
import json
import requests
import traceback
from google.cloud import pubsub_v1
from errors.errors import CallExternalServiceError
from validators.validators import validar_resultado_consumo_servicio

datos_en_memoria = None

def formatDateTimeToUTC(dateTime):
    return dateTime.split('.')[0].replace(' ', 'T')

# Funcion para envio de mensaje via pubsub
def publicar_pub_sub(args):
    # Creamos el ciente publihser
    publisher = pubsub_v1.PublisherClient()
    args = json.dumps(args).encode('utf-8')
    messege_published = publisher.publish(obtener_topico(), args)
    message_id = messege_published.result()
    print(f"Mensaje publicado con ID: {message_id}")

# Función retorna el enpoint del servicio de usuarios
def obtener_endpoint_usuarios():
    return os.getenv('GESTORUSUARIOS_ADDRESS')

# Función que retorna el topica de mensajes
def obtener_topico():
    return os.getenv("PATH_TOPIC_ALERTA")

# Función que retorna el tipo de notificación
def obtener_tipo_notificacion():
    return os.getenv('TIPO_NOTIFICACION')

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