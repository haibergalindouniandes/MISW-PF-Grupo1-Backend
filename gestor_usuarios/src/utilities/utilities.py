import asyncio
import os
import traceback
import aiohttp
from errors.errors import ApiError, ErrorMetodoNoPermitido
from validators.validators import validar_resultado_consumo_servicio

batch_servicios = []

# Función convierte booleano a string
def booleano_a_string(booleano):
    return 'SI' if booleano else 'NO'

# Función convierte strin a booleano
def string_a_booleano(string):
    return True if string == 'SI' else False

# Función retorna el enpoint del servicio de plan nutricional
def obtener_endpoint_plan_nutricional():
    return os.getenv('GESTOREPLANNUTRICIONAL_ADDRESS')

# Función retorna el enpoint del servicio de entrenamientos
def obtener_endpoint_entrenamientos():
    return os.getenv('GESTORENTRENAMIENTOS_ADDRESS')

# Función que agregar un nuevo  endpoint de la API a llamar
def agregar_servicio_a_batch(servicio):
    batch_servicios.append(servicio)

# Función que limpia el listado de APIs a llamar
def limpiar_batch_de_servicios():
    batch_servicios.clear()

# Función que permite realizar el consumo de un servicio de forma asincrona
async def consumo_servicio_asincrono(url, metodo, data=None, headers=None):
    print('<================ consumo_servicio_asincrono =====================>')
    print(url)
    print(metodo)
    print(data)
    print(data)    
    async with aiohttp.ClientSession() as session:
        if metodo == "POST":
            async with session.post(url, json=data, headers=headers) as resultado:
                validar_resultado_consumo_servicio(resultado)
                return await resultado.json()
        else:
            raise ErrorMetodoNoPermitido 
    
# Función que permite realizar el consumo en paralelo de servicios
async def ejecucion_batch_en_paralelo():
    tareas = [consumo_servicio_asincrono(url, metodo, data, headers) for url, metodo, data, headers in batch_servicios]
    resultados = await asyncio.gather(*tareas)
    return resultados