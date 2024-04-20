import random
from faker import Faker
import requests
from src.main import app

class TestResources:
    # Declaración constantes
    dataFactory = Faker()    
    data = {}
    headers = {}
    response_healthcheck = {}
    response_token = {}
    response_creacion_plan_entrenamiento = {}
    response_consulta_plan_entrenamiento_por_usuario = {}
    
    # Función que genera data inicial
    def set_up(self):
        data_login = {"email": "usuario2024@uniandes.edu.co", "password": "Usuario2*24"}   
        lista_entrenamientos = [ "Ciclismo", "Carreras" ]    
        id_usuario = "6da46c66-f5ee-11ee-a0c6-c9ae58811c0e"
        self.ejecucion_generar_token(data_login) 
        
        self.data = {
            "entrenamiento": f"{random.choice(lista_entrenamientos)}",
            "numero_semanas": random.randint(1, 10),
            "id_usuario": f"{id_usuario}",
            "plan_entrenamiento": {
                "lunes": f"{random.randint(1, 10)}",
                "martes": f"{random.randint(1, 10)}",
                "miercoles": f"{random.randint(1, 10)}",
                "jueves": f"{random.randint(1, 10)}",
                "viernes": f"{random.randint(1, 10)}",
                "sabado": f"{random.randint(1, 10)}",
                "domingo": f"{random.randint(1, 10)}"
            }
        }
        
        self.headers["Authorization"] = f"Bearer {self.response_token['token']}"
    
    # Función consume el API de generación del token
    def ejecucion_generar_token(self, data):
        url = "https://misw-pf-grupo1-backend-gestor-usuarios-klme3r4qta-uc.a.run.app/usuarios/login"             
        response = requests.post(url, json=data)
        self.response_token  = response.json()

    # Función consume el API de generación de healthcheck de entrenamientos
    def ejecucion_healthcheck(self):
        with app.test_client() as test_client:
            self.response_healthcheck = test_client.get(
                '/entrenamientos/ping'
            )
    
    # Función consume el API de creación de plan de entrenamientos
    def ejecucion_crear_plan_entrenamiento(self, data, headers):
        with app.test_client() as test_client:
            self.response_creacion_plan_entrenamiento = test_client.post(
                '/entrenamientos/plan-entrenamiento', json=data, headers=headers
            )    

    # Función consume el API de consulta de plan de entrenamiento por usuario
    def ejecucion_consultar_plan_entrenamiento_por_usuario(self, headers):
        with app.test_client() as test_client:
            self.response_consulta_plan_entrenamiento_por_usuario = test_client.get(
                f"/entrenamientos/plan-entrenamiento/usuario/{self.data['id_usuario']}", headers=headers
            )    
    
    # Función que valida el healthcheck
    def test_validar_healthcheck(self):
        self.ejecucion_healthcheck()
        assert self.response_healthcheck.status_code == 200
        
    # Función que valida la creación exitosa de un plan de entrenamiento
    def test_validar_creacion_plan_entrenamiento(self):
        self.set_up()
        self.ejecucion_crear_plan_entrenamiento(self.data, self.headers)
        assert self.response_creacion_plan_entrenamiento.status_code == 200
        
    # Función que valida la creación exitosa de un plan de entrenamiento
    def test_validar_consulta_plan_entrenamiento_por_usuario(self):
        self.set_up()
        self.ejecucion_consultar_plan_entrenamiento_por_usuario(self.headers)
        assert self.response_consulta_plan_entrenamiento_por_usuario.status_code == 200        