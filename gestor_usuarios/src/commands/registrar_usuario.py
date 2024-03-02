# Importación de dependencias
import asyncio
import traceback
from commands.base_command import BaseCommannd
from utilities.utilities import booleano_a_string, obtener_endpoint_entrenamientos, obtener_endpoint_plan_nutricional, agregar_servicio_a_batch, limpiar_batch_de_servicios, ejecucion_batch_en_paralelo, string_a_booleano
from models.models import db, Usuario
from validators.validators import validar_esquema, esquema_registro_usuario
from sqlalchemy.exc import SQLAlchemyError
from errors.errors import ApiError

# Clase que contiene la logica de creción de Alerta
class RegistrarUsuario(BaseCommannd):
    # Constructor
    def __init__(self, data):
        self.validar_request(data)
        self.asignar_datos_usuario(data)

    # Función que valida el request del servicio
    def validar_request(self, json_payload):
        # Validacion del request
        validar_esquema(json_payload, esquema_registro_usuario)

    # Función que valida el request del servicio
    def asignar_datos_usuario(self, json_payload):
        # Asignacion de variables
        self.nombres = json_payload['nombres']
        self.apellidos = json_payload['apellidos']
        self.tipo_identificacion = json_payload['tipo_identificacion']
        self.numero_identificacion = json_payload['numero_identificacion']
        self.sexo = json_payload['sexo']
        self.edad = int(json_payload['edad'])
        self.peso = float(json_payload['peso'])
        self.estatura = float(json_payload['estatura'])
        self.enfermedades_cardiovasculares = bool(json_payload['enfermedades_cardiovasculares'])
        self.proposito = json_payload['proposito']
        self.practica_deporte = bool(json_payload['practica_deporte'])
        self.pais = json_payload['pais']
        self.departamento = json_payload['departamento']
        self.ciudad = json_payload['ciudad']
        
    # Función que valida el request del servicio
    def asignar_ids_servicios_externos(self, resultados):
        # Asignacion id servicios externos
        self.id_entrenamiento = resultados[0]["id"]
        self.id_plan_nutricional = resultados[1]["id"]
        
    # Función que asigna  plan nutricional
    def agregar_plan_nutricional(self, resultados, resultado_legado):
        # Asignacion plan nutricional
        resultados['plan_alimentacion'] = resultado_legado[0]
        return resultados

    # Función que asigna  plan de entrenamientos
    def agregar_plan_de_entrenamiento(self, resultados, resultado_legado):
        # Asignacion  plan de entrenamientos
        resultados['plan_entrenamiento'] = resultado_legado[1]
        return resultados

    # Función que realiza el mapeo de información para el consumo del servicio de Entrenamientos
    def agregar_servicio_entrenamientos(self):
        # Mapeo de información
        headers = {'Content-Type': 'application/json'}
        data = {
            "sexo": self.sexo,
            "edad": self.edad,
            "peso": int(self.peso),
            "estatura": int(self.estatura),
            "tipo_identificacion": self.tipo_identificacion,
            "enfermedades_cardiovasculares": booleano_a_string(self.enfermedades_cardiovasculares),
            "practica_deporte": booleano_a_string(self.practica_deporte),
            "proposito": self.proposito
        }
        agregar_servicio_a_batch((obtener_endpoint_entrenamientos(), 'POST', data, headers))

    # Función que realiza el mapeo de información para el consumo del servicio de plan nutricional
    def agregar_servicio_plan_nutricional(self):
        # Mapeo de información
        headers = {'Content-Type': 'application/json'}
        data = {
            "sexo": self.sexo,
            "edad": self.edad,
            "peso": int(self.peso),
            "estatura": int(self.estatura),
            "tipo_identificacion": self.tipo_identificacion,
            "enfermedades_cardiovasculares": booleano_a_string(self.enfermedades_cardiovasculares),
            "practica_deporte": booleano_a_string(self.practica_deporte),
            "proposito": self.proposito
        }
        agregar_servicio_a_batch((obtener_endpoint_plan_nutricional(), 'POST', data, headers))

    # Función que ejecuta el consumo en paralelo de servicios
    def ejecutar_batch_servicios(self):
        self.agregar_servicio_plan_nutricional()
        self.agregar_servicio_entrenamientos()
        resultados = asyncio.run(ejecucion_batch_en_paralelo())
        limpiar_batch_de_servicios()
        return resultados

        # Función que realiza el registro del usuario en BD
    def registrar_usuario_bd(self):
        # Registrar en BD
        usuario = Usuario(
            nombres=self.nombres,
            apellidos=self.apellidos,
            tipo_identificacion=self.tipo_identificacion,
            numero_identificacion=self.numero_identificacion,
            sexo=self.sexo,
            edad=self.edad,
            peso=self.peso,
            estatura=self.estatura,
            enfermedades_cardiovasculares=self.enfermedades_cardiovasculares,
            pais=self.pais,
            departamento=self.departamento,
            ciudad=self.ciudad
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    # Función que realiza creación de la Alerta
    def execute(self):
        try:
            # Logica de negocio
            resultado = self.ejecutar_batch_servicios()
            # self.asignar_ids_servicios_externos(resultado)
            usuario_registrado = self.registrar_usuario_bd().to_dict()
            usuario_registrado = self.agregar_plan_de_entrenamiento(usuario_registrado, resultado)
            usuario_registrado = self.agregar_plan_nutricional(usuario_registrado, resultado)
            return usuario_registrado
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
        

        