import functions_framework

# import necessary packages
from email.message import EmailMessage
import smtplib


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


@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    data = request.headers
    name = ""

    if data["tipo"] == "Alerta":
        alerta(
            request_json["name"],
            request_json["latitud"],
            request_json["longitud"],
            request_json["descripcion"]
        )
        return "Succes!".format(name)
    elif data["tipo"] == "Noti_Masiva":
        notificacion_masiva(
            request_json["name"],
            request_json["descripcion"]
        )
        return "Succes!".format(name)
    else:
        return "Error!".format(name), 500
