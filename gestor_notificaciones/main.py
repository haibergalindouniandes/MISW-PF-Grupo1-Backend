import functions_framework

# import necessary packages
from email.message import EmailMessage
import smtplib
import os
from google.cloud import pubsub_v1

PATH_PUBSUB_KEY = os.getenv("PATH_PUBSUB_KEY", default="proyecto1-experimentos-b53d3e709d98.json")
PATH_SUBSCRIBER = os.getenv("SUBSCRIPTION_TOPIC", default="projects/proyecto1-experimentos/subscriptions/notifications-sub")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH_PUBSUB_KEY

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    try:
        print(f"Received {message}.")
        name = ""
        if message.attributes.get("tipo") == "Alerta":
            alerta(
                message.attributes.get("name"),
                message.attributes.get("latitud"),
                message.attributes.get("longitud"),
                message.attributes.get("descripcion")
            )
            message.ack()
            return "Succes!".format(name)
        elif message.attributes.get("tipo") == "Noti_Masiva":
            notificacion_masiva(
                message.attributes.get("name"),
                message.attributes.get("descripcion")
            )
            message.ack()
            return "Succes!".format(name)
        else:
            message.ack()
            return "Error!".format(name), 500
    except Exception as e:
        print("ERROR", f"==> {str(e)}")
    finally:
        print(
            "INFO", f"<=================== Fin del procesamiento de la tarea ===================>")



@functions_framework.http
def alerta(email,name,latitud,longitud,descripcion):
    # create message object instance
    msg = EmailMessage()
    message = f""" <h1><strong>SportApp Alerta&nbsp;</strong></h1> 
        <h2><strong>Servicio de Alerta de Emergencia</strong></h2>  
        <h2><strong>El siguiente Usuario: </strong>{name}</h2>  
        <p>Lo ha contactado ya que se encuentra en un situacion anormal durante su entrenamiento y usted es su contacto de emergencia</p>  
        <p>La ultima ubicacion conocida del usuario fue en Longitud: {longitud} y Latitud: {latitud}</p>  
        <p>La alerta fue creada con el siguiente mensaje: {descripcion}</p>  
        <p>Por favor pongase en contacto con el usuario para mas detalles. </p>
        <p>&nbsp;</p>  
        <p>Equipo Grupo 1 - MISW4501</p>"""

     # setup the parameters of the message
    password = "jmek wgba shnf msdr"
    msg["From"] = "SportApp_G1_Pruebas@gmail.com"
    msg["To"] = email
    msg["Subject"] = "SportApp Alerta de Emergencia"
    # add in the message body
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(message)
    # create server
    server = smtplib.SMTP("smtp.gmail.com: 587")
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg["From"], password)
    # send the message via the server.
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
    print("successfully sent email to %s:" % (msg["To"]))


@functions_framework.http
def notificacion_masiva(email,name,descripcion):
    # create message object instance
    msg = EmailMessage()
    message = f"""<h1><strong>SportApp Notificacion Masiva&nbsp;</strong></h1> 
        <h2><strong>Servicio de Notificacion de Servicios</strong></h2>  
        <h2><strong>El Proveedor de su Servicio: </strong>{name}</h2>  
        <p>Lo ha contactado ya que se encuentra Inscrito en su evento y tiene el siguiente mensaje para usted:</p>  
        <p>{descripcion}</p>  
        <p>Por favor pongase en contacto con el proveedor para mas detalles. </p>
        <p>&nbsp;</p>  
        <p>Equipo Grupo 1 - MISW4501</p>"""
    
    # setup the parameters of the message
    password = "jmek wgba shnf msdr"
    msg["From"] = "SportApp_G1_Pruebas@gmail.com"
    msg["To"] = email
    msg["Subject"] = "SportApp Notificacion Masiva"
    # add in the message body
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(message)
    # create server
    server = smtplib.SMTP("smtp.gmail.com: 587")
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg["From"], password)
    # send the message via the server.
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()
    print("successfully sent email to %s:" % (msg["To"]))

# Configuracion subscriber
subscriber = pubsub_v1.SubscriberClient()
streaming_pull_future = subscriber.subscribe(PATH_SUBSCRIBER, callback=callback)
timeout = 5.0
print(f"Escuchando mensajes desde [{PATH_SUBSCRIBER}]")

with subscriber:
    try:
        streaming_pull_future.result(timeout=timeout)
    except:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
