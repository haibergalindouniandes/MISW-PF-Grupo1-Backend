import base64
import json
import os
import sqlalchemy
import smtplib
import uuid
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Asignar constantes
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_DRIVER_NAME = 'postgres+pg8000'
DB_CONNECTION_NAME = os.environ.get('DB_CONNECTION_NAME')
NOTIFICATION_EMAIL = os.environ.get('NOTIFICATION_EMAIL')
NOTIFICATION_PASW = os.environ.get('NOTIFICATION_PASW')
CONNECTION_STRING =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(DB_CONNECTION_NAME)})

# Configuración logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Función que permite el registro de la notificación en base de datos
def registrar_notificacion_bd(data_dict):
    db = generar_conexion_bd()
    try:
        with db.connect() as conn:
            query = 'insert into notificaciones (id, name, descripcion, tipo, fecha_creacion, fecha_actualizacion) values (:id, :name, :descripcion, :tipo, :fecha_creacion, :fecha_actualizacion)'
            stmt = sqlalchemy.text(query)
            conn.execute(stmt, data_dict)
            logger.info('Se registro la notificación correctamente')
    except Exception as e:
        logger.error(str(e))    

# Función que permite generar la conexión con base de datos
def generar_conexion_bd():
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=DB_DRIVER_NAME,
        username=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        query=CONNECTION_STRING,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )
    return db

def decodificar_base64(texto_base64):
    cadena_decodificada = base64.b64decode(texto_base64)
    return cadena_decodificada.decode('utf-8')

def enviar_evento(emails,name,descripcion):
    # Estructura del cuerpo del correo
    body = f"""<h1><strong>SportApp Notificación Masiva&nbsp;</strong></h1> 
        <h2><strong>Servicio De Envio De Notificación De Eventos Masivos</strong></h2>  
        <h2><strong>El Proveedor de su Servicio: </strong>{name}</h2>  
        <p>Lo ha contactado ya que se encuentra inscrito en su evento y tiene el siguiente mensaje para usted:</p>  
        <p>{descripcion}</p>  
        <p>Por favor pongase en contacto con el proveedor para mas detalles. </p>
        <p>&nbsp;</p>  
        <p>Equipo Grupo 1 - MISW4501</p>"""
    
    # Envio de email
    msg = MIMEMultipart()
    msg['From'] = NOTIFICATION_EMAIL
    msg['Subject'] = 'SportApp Notificación Masiva De Eventos'
    msg['To'] = ', '.join(emails)
    msg.attach(MIMEText(body, 'html'))
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(NOTIFICATION_EMAIL, decodificar_base64(NOTIFICATION_PASW))
        server.sendmail(NOTIFICATION_EMAIL, emails, msg.as_string())
        logger.info("Email enviado exitosamente a %s:" % (msg["To"]))
        server.quit()

def eventos(event, context):
    """Definición de la función invocada por el servicio Pub/Sub. 
    La función retorna la información recibida en el body
    
    Args:
        event (dic): Objeto con la información de la petición.
        context (dic): Información del evento generado
    Returns:
        Información de la solicitud de notificación masiva
    """
    logger.info('Inicia envio de notificación - Evento masivo')
    logger.info(event['data'])
    message_decoded= base64.b64decode(event['data'])
    logger.info(message_decoded)
    data_dict = json.loads(message_decoded)
    data_dict["id"] = str(uuid.uuid4())
    data_dict["fecha_creacion"] = str(datetime.now())
    data_dict["fecha_actualizacion"] = str(datetime.now())
    if data_dict["tipo"] == "notificacion_masiva_eventos":
        enviar_evento(
            data_dict["emails"],
            data_dict["usuario"],
            data_dict["descripcion"]
            )
        registrar_notificacion_bd(data_dict)
    else:    
        logger.error(f"El tipo [{data_dict['tipo']}] no es valido")
    data = event['data']
    logger.info('Finaliza envio de notificación - Evento masivo')
    return data