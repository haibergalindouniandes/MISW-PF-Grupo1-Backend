#!/bin/bash

####################################################################################################################################
echo "<================== [Inicio] Configuración ==================>"
TEST_PATH=tests-results-usuarios
mkdir -p $TEST_PATH
echo "Se realiza la creación del directorio [$TEST_PATH]"
MIN_COVERAGE=80
echo "La cobertura minima establecida para pasar las pruebas es [$MIN_COVERAGE]"
echo "<================== [Fin] Configuración ==================>"


echo "<================== [Inicio] Actualizacion de codigo ==================>"
pwd
cd /workspace/gestor_usuarios
pwd
python3 -m pip install --upgrade pip
python3 -m pip --version
python3 -m pip install -r requirements.txt
echo "<================== [Fin][Exitoso] Actualizacion de Codigo ==================>"
pwd
git pull
git checkout feature_gestor_usuarios
git pull
echo "<================== [Inicio] Ejecucion test ==================>"
#pwd
#cd /workspace/gestor_usuarios
pwd
cd /workspace/gestor_usuarios
pwd
python3 -m pip install --upgrade pip
python3 -m pip --version
python3 -m pip install -r requirements.txt
#pip install pytest
#pip install pytest-cov
#pip install pytest-env
#pip install python-dotenv
#pip install flask
#pip install flask_restful
echo "Se inicia ejecucion de pruebas"
pytest --cov-fail-under=80 --cov=src --cov-report=html:cov_report
echo "fin ejecucion de pruebas"
echo "<================== [Fin][Exitoso] Ejecucion test ==================>"