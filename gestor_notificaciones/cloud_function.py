import base64
import json



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

    if data_dict["tipo"] == "Alerta":
        # alerta(
        #     data_dict["name"],
        #     data_dict["latitud"],
        #     data_dict["longitud"],
        #     data_dict["descripcion"]
        #     )
        print("Succes Alerta!")
    elif data_dict["tipo"] == "Noti_Masiva":
        # notificacion_masiva(
        #     data_dict["name"],
        #     data_dict["descripcion"]
        #     )        
        print("Succes Notificacion!")
    else:    
        print("Error!")


    data = event['data']
    print('Se recibe notificacion de usuario')
    return data