import os
import json
from google.cloud import pubsub_v1

# Constantes
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("PATH_PUBSUB_KEY")
PATH_TOPIC = os.getenv("PATH_TOPIC")
def formatDateTimeToUTC(dateTime):
    return dateTime.split('.')[0].replace(' ', 'T')

# Funcion para envio de mensaje via pubsub
def publicar_pub_sub(args):
    # Creamos el ciente publihser
    publisher = pubsub_v1.PublisherClient()
    args = json.dumps(args).encode('utf-8')
    messege_published = publisher.publish(PATH_TOPIC, args)


def dar_clasificacion(sexo, peso, estatura, edad, enfermedades_cardiovasculares, practica_deporte):
    idx_enfermedades = 0
    idx_deporte = 0
    if enfermedades_cardiovasculares == 'SI':
        idx_enfermedades = 1
    if practica_deporte == 'SI':
        idx_deporte = 1
    imc = (peso/(estatura/100)**2)*(1.75**(idx_enfermedades))*(1.25**(1-idx_deporte))

    imc_hombre_optimo = {'18-27 años':14, '28-37 años':17, '38-47 años':21, '48-57 años':23, '58-67 años':25, '68-90 años':25}
    imc_mujer_optimo = {'18-27 años':19, '28-37 años':21, '38-47 años':23, '48-57 años':27, '58-67 años':28, '68-90 años':28}

    idx_imc = int((edad-18)/10)
    if sexo == 'MASCULINO':        
        imc_optimo = [*imc_hombre_optimo.items()][idx_imc][1]
    else:
        imc_optimo = [*imc_mujer_optimo.items()][idx_imc][1]
    
    if imc <= imc_optimo - 1:
        clasificacion = 'PESO BAJO'
    elif imc > imc_optimo - 1 and imc <= imc_optimo + 5:
        clasificacion = 'PESO NORMAL'
    elif imc > imc_optimo + 5 and imc <= imc_optimo + 8:
        clasificacion = 'SOBREPESO'
    else:
        clasificacion = 'OBESIDAD'
    
    return clasificacion    
