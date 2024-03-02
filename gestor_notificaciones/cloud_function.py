import base64
import json
import sqlalchemy

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
        insert('insert into notificaciones (name,latitud,longitud,descripcion,tipo) values ({a},{b},{c},{d},{e})'.format(a=data_dict["name"],b={data_dict["latitud"]},c=data_dict["longitud"],d=data_dict["descripcion"],e=data_dict["tipo"]))
        print("Succes Alerta!")
    elif data_dict["tipo"] == "Noti_Masiva":
        # notificacion_masiva(
        #     data_dict["name"],
        #     data_dict["descripcion"]
        #     )    
        insert('insert into notificaciones (name,descripcion,tipo) values ({a},{b},{c})'.format(a=data_dict["name"],b=data_dict["descripcion"],c=data_dict["tipo"]))      
        print("Succes Notificacion!")
    else:    
        print("Error!")


    data = event['data']
    print('Se recibe notificacion de usuario')
    return data