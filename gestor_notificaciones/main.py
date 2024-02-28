import functions_framework

# import necessary packages
from email.message import EmailMessage
import smtplib
from google.cloud import pubsub_v1


subscriber = pubsub_v1.SubscriberClient()
subscription_path = "projects/misw4501/topics/notificaciones_alertas"
timeout = 5.0

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
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
    

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.


@functions_framework.http
def alerta(email,name,latitud,longitud,descripcion):
    # create message object instance
    msg = EmailMessage()
    message = f" <h1><strong>SportApp Alerta&nbsp;</strong></h1> 
        <h2><strong>Servicio de Alerta de Emergencia</strong></h2>  
        <h2><strong>El siguiente Usuario: </strong>{name}</h2>  
        <p>Lo ha contactado ya que se encuentra en un situacion anormal durante su entrenamiento y usted es su contacto de emergencia</p>  
        <p>La ultima ubicacion conocida del usuario fue en Longitud: {longitud} y Latitud: {latitud}</p>  
        <p>La alerta fue creada con el siguiente mensaje: {descripcion}</p>  
        <p>Por favor pongase en contacto con el usuario para mas detalles. </p>
        <p>&nbsp;</p>  
        <p>Equipo Grupo 1 - MISW4501</p>"

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
    message = f" <h1><strong>SportApp Notificacion Masiva&nbsp;</strong></h1> 
        <h2><strong>Servicio de Notificacion de Servicios</strong></h2>  
        <h2><strong>El Proveedor de su Servicio: </strong>{name}</h2>  
        <p>Lo ha contactado ya que se encuentra Inscrito en su evento y tiene el siguiente mensaje para usted:</p>  
        <p>{descripcion}</p>  
        <p>Por favor pongase en contacto con el proveedor para mas detalles. </p>
        <p>&nbsp;</p>  
        <p>Equipo Grupo 1 - MISW4501</p>"
    
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
