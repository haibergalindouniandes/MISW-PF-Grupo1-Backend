import random
import requests
from datetime import datetime
from faker import Faker
from src.main import app

class TestResources:
    # Declaración constantes
    dataFactory = Faker()    
    data = {}
    alimentacion = {}
    plan_alimentacion = {}
    headers = {}
    response_healthcheck = {}
    response_token = {}
    response_resultados_alimentacion = {}
    response_consulta_resultados_alimentacion_id_usuario = {}
    response_consulta_resultados_alimentacion_fechas = {}
    response_crear_plan_alimentacion = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}     
        id_usuario = "d0d85122-eafd-11ee-a951-0242ac120002"
        fecha_actual = self.obtener_fecha_actual()
        self.ejecucion_generar_token(data_login) 
        
        self.data = {
            "calorias_1": f"{random.randint(300, 400)}",
            "calorias_2": f"{random.randint(300, 400)}",
            "calorias_3": f"{random.randint(300, 400)}",
            "ml_agua": f"{random.randint(300, 400)}",
            "fecha": f"{fecha_actual }",
            "id_usuario": f"{id_usuario}"
        }


        self.plan_alimentacion = {    
            "plan_alimentacion":{
                "lunes": f"{random.randint(100, 2000)}",
                "martes": f"{random.randint(100, 2000)}",
                "miercoles": f"{random.randint(100, 2000)}",
                "jueves": f"{random.randint(100, 2000)}",
                "viernes": f"{random.randint(100, 2000)}",
                "sabado": f"{random.randint(100, 2000)}",
                "domingo": f"{random.randint(100, 2000)}"
            }     
        }
        self.alimentacion = {
            "id_usuario": f"{id_usuario}",
            "numero_semanas": {random.randint(1, 10)},
            "plan_alimentacion":f"{self.plan_alimentacion}"
      
        }
        
        self.headers["Authorization"] = f"Bearer {self.response_token['token']}"

    # Función que permite generar una fecha futura
    def obtener_fecha_actual(self):
        fecha_actual = datetime.now()
        return fecha_actual.strftime('%Y-%m-%d')
    
    # Función consume el API de generación del token
    def ejecucion_generar_token(self, data):
        url = "https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/login"             
        response = requests.post(url, json=data)
        self.response_token  = response.json()

    # Función consume el API de generación de healthcheck de entrenamientos
    def ejecucion_healthcheck(self):
        with app.test_client() as test_client:
            self.response_healthcheck = test_client.get(
                '/nutricion/ping'
            )
    
    # Función consume el API de registro de resultados de alimentacion de un usuario
    def ejecucion_registrar_resultados_alimentacion(self, data, headers):
        with app.test_client() as test_client:
            self.response_resultados_alimentacion = test_client.post(
                '/nutricion/resultados-alimentacion', json=data, headers=headers
            )    

    # Función consume el API de consulta de resultados de alimentacion por usuario
    def ejecucion_consultar_resultados_alimentacion_id_usuario(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_resultados_alimentacion_id_usuario = test_client.get(
                f"/nutricion/resultados-alimentacion/{self.data['id_usuario']}", headers=headers
            )    

    # Función consume el API de consulta de resultados de alimentacion por usuario y rango de fechas
    def ejecucion_consultar_resultados_alimentacion_fechas(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_resultados_alimentacion_fechas = test_client.get(
                f"/nutricion/resultados-alimentacion/{self.data['id_usuario']}/{self.data['fecha']}/{self.data['fecha']}", headers=headers
            ) 
    
    # Función consume el API de ccreacion plan de alimentacion
    def ejecucion_creacion_plan_alimentacion(self, alimentacion, headers):
        with app.test_client() as test_client:
            self.response_crear_plan_alimentacion = test_client.post(
                '/nutricion/plan-nutricional', json=alimentacion, headers=headers
            )            
    
    # Función que valida el healthcheck
    def test_validar_healthcheck(self):
        self.ejecucion_healthcheck()
        assert self.response_healthcheck.status_code == 200
        
    # Función que valida el reistro exitoso de resultados de alimentacion de un usuario
    def test_validar_registro_resultados_alimentacion(self):
        self.set_up()
        self.ejecucion_registrar_resultados_alimentacion(self.data, self.headers)
        assert self.response_resultados_alimentacion.status_code == 200
        
    # Función que valida la conusulta de los resultados de alimentacion de un usuario
    def test_validar_consulta_resultados_alimentacion_usuario(self):
        self.set_up()
        self.ejecucion_consultar_resultados_alimentacion_id_usuario(self.headers)
        assert self.response_consulta_resultados_alimentacion_id_usuario.status_code == 200        
        
    # Función que valida la conusulta de los resultados de alimentacion de un usuario y rango de fechas
    def test_validar_consulta_resultados_alimentacion_fechas(self):
        self.set_up()
        self.ejecucion_consultar_resultados_alimentacion_fechas(self.headers)
        assert self.response_consulta_resultados_alimentacion_fechas.status_code == 200      


    # Función que valida la creacion de un plan de alimentacion
    def test_validar_creacion_plan_alimentacion(self):
        self.set_up()
        self.ejecucion_creacion_plan_alimentacion(self.alimentacion, self.headers)
        print("=======CrearPlanAlimentacion========")
        print(self.alimentacion)
        print(self.response_crear_plan_alimentacion)
        assert self.response_crear_plan_alimentacion.status_code == 200                           