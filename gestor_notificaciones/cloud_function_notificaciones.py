import base64
import json
import sqlalchemy
from email.message import EmailMessage
import smtplib
from security_utilies import cargar_clave_desde_archivo, descifrar_texto

# Uncomment and set the following variables depending on your specific instance and database:
connection_name = "proyecto1-experimentos:us-central1:postgres"
#table_name = ""
#table_field = ""
#table_field_value = ""
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"
# If your database is PostgreSQL, uncomment the following two lines:
driver_name = 'postgres+pg8000'
query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})


def insert(query):
    print(query)    
    stmt = sqlalchemy.text(query)

    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt)
    except Exception as e:
        return 'Error: {}'.format(str(e))
    return 'ok'

def notificacion_masiva(email,name,descripcion):
    # create message object instance
    msg = EmailMessage()
    body = f"""<h1><strong>SportApp Notificacion Masiva&nbsp;</strong></h1> 
        <h2><strong>Servicio de Notificacion de Servicios</strong></h2>  
        <h2><strong>El Proveedor de su Servicio: </strong>{name}</h2>  
        <p>Lo ha contactado ya que se encuentra Inscrito en su evento y tiene el siguiente mensaje para usted:</p>  
        <p>{descripcion}</p>  
        <p>Por favor pongase en contacto con el proveedor para mas detalles. </p>
        <p>&nbsp;</p>  
        <p>Equipo Grupo 1 - MISW4501</p>"""
    
    # setup the parameters of the message
    # password = "1d761200a0fd75"
    # msg["From"] = "miswexp1pro1grupo1@gmail.com"
    # msg["To"] = email
    # msg["Subject"] = "SportApp Notificacion Masiva"
    # # add in the message body
    # msg.add_header("Content-Type", "text/html")
    # msg.set_payload(message)
    # # create server
    # server = smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525)
    # server.starttls()
    # # Login Credentials for sending the mail
    # server.login("28ae9d3cad356a", password)
    # # send the message via the server.
    # server.sendmail(msg["From"], msg["To"], msg.as_string())
    # server.quit()
    # print("successfully sent email to %s:" % (msg["To"]))
    
    clave_cargada = cargar_clave_desde_archivo()
    texto_cifrado = b'gAAAAABl4-WSBGPYs_zRFNAGLm2N0d6ooQAkC73ZxeDJgeY5p87NWi2uDzeZ8PzOui77RuQ9ajjqDmSZe-hS2FipsVKrm9HUT4pmh5dGNPvmWYM53Vu5OALGE8GdHp4qgDSSCOeRT7Tq9-RjRGQ8g8WVNCk46xZVGsBMSWkTFcawgl0nESrEFRY='
    texto_descifrado = descifrar_texto(texto_cifrado, clave_cargada)

    password = texto_descifrado
    msg["From"] = "miswexp1pro1grupo1@gmail.com"
    msg["To"] = email
    msg["Subject"] = "SportApp Notificacion Masiva"
    # add in the message body
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(body)
    # create server
    server = smtplib.SMTP("smtp.sendgrid.net", 587)
    server.starttls()
    # Login Credentials for sending the mail
    server.login("apikey", password)
    # send the message via the server.
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
    print("successfully sent email to %s:" % (msg["To"]))

def notificaciones(event, context):
    """Definición de la función invocada por el servicio Pub/Sub. 
    La función retorna la información recibida en el body
    
    Args:
        event (dic): Objeto con la información de la petición.
        context (dic): Información del evento generado
    Returns:
        Información de la solicitud de auxilio
    """
    print('Inicia gestor de notificaciones')
    print(event['data'])

    message_decoded= base64.b64decode(event['data'])
    print(message_decoded)
    data_dict = json.loads(message_decoded)
    print(data_dict["name"])

    if data_dict["tipo"] == "Noti_Masiva":
        notificacion_masiva(
            data_dict["email"],
            data_dict["name"],
            data_dict["descripcion"]
            )    
        insert('insert into notificaciones (name,descripcion,tipo) values ({a},{b},{c})'.format(a=data_dict["name"],b=data_dict["descripcion"],c=data_dict["tipo"]))      
        print("Succes Notificacion!")
    else:    
        print("Error!")

    data = event['data']
    print('Se recibe notificacion de usuario')
    return data