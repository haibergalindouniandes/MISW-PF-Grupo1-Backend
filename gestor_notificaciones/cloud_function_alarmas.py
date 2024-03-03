import base64
import json
import sqlalchemy
from email.message import EmailMessage
import smtplib

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

def alerta(email,name,latitud,longitud,descripcion):
    # create message object instance
    msg = EmailMessage()
    body = f""" <h1><strong>SportApp Alerta&nbsp;</strong></h1> 
        <h2><strong>Servicio de Alerta de Emergencia</strong></h2>  
        <h2><strong>El siguiente Usuario: </strong>{name}</h2>  
        <p>Lo ha contactado ya que se encuentra en un situacion anormal durante su entrenamiento y usted es su contacto de emergencia</p>  
        <p>La ultima ubicacion conocida del usuario fue en Longitud: {longitud} y Latitud: {latitud}</p>  
        <p>La alerta fue creada con el siguiente mensaje: {descripcion}</p>  
        <p>Por favor pongase en contacto con el usuario para mas detalles. </p>
        <p>&nbsp;</p>  
        <p>Equipo Grupo 1 - MISW4501</p>"""

    # setup the parameters of the message
    # password = "1d761200a0fd75"
    # msg["From"] = "miswexp1pro1grupo1@gmail.com"
    # msg["To"] = email
    # msg["Subject"] = "SportApp Alerta de Emergencia"
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

    password = "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"
    msg["From"] = "miswexp1pro1grupo1@gmail.com"
    msg["To"] = email
    msg["Subject"] = "SportApp Notificacion de Alerta"
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

def alarmas(event, context):
    """Definición de la función invocada por el servicio Pub/Sub. 
    La función retorna la información recibida en el body
    
    Args:
        event (dic): Objeto con la información de la petición.
        context (dic): Información del evento generado
    Returns:
        Información de la solicitud de auxilio
    """
    print('Inicia gestor de Alarmas')
    print(event['data'])

    message_decoded= base64.b64decode(event['data'])
    print(message_decoded)
    data_dict = json.loads(message_decoded)
    print(data_dict["name"])

    if data_dict["tipo"] == "Alerta":
        alerta(
            data_dict["email"],
            data_dict["name"],
            data_dict["latitud"],
            data_dict["longitud"],
            data_dict["descripcion"]
            )
        insert('insert into notificaciones (name,latitud,longitud,descripcion,tipo) values ({a},{b},{c},{d},{e})'.format(a=data_dict["name"],b={data_dict["latitud"]},c=data_dict["longitud"],d=data_dict["descripcion"],e=data_dict["tipo"]))
        print("Succes Alerta!")
    else:    
        print("Error!")


    data = event['data']
    print('Se recibe Alarma de usuario')
    return data