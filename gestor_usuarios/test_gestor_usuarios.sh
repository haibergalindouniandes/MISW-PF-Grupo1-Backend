#!/bin/bash

####################################################################################################################################
echo "<================== [Inicio] Configuración ==================>"
TEST_PATH=tests-results-usuarios
mkdir -p $TEST_PATH
echo "Se realiza la creación del directorio [$TEST_PATH]"
MIN_COVERAGE=80
echo "La cobertura minima establecida para pasar las pruebas es [$MIN_COVERAGE]"
echo "<================== [Fin] Configuración ==================>"
echo "<================== [Inicio] instalacion de dependencias ==================>"
pwd
cd /workspace/gestor_usuarios
pwd
pip install -r requirements.txt
echo "<================== [Fin][Exitoso] instalacion dependencias ==================>"
echo "<================== [Inicio] Ejecucion test ==================>"
#pwd
#cd /workspace/gestor_usuarios
pwd
git pull
git checkout feature_gestor_usuarios
git pull
echo "Se inicia ejecucion de pruebas"
pip install pytest
pip install pytest-cov
pytest --cov-fail-under=80 --cov=src --cov-report=html:cov_report
echo "fin ejecucion de pruebas"
echo "<================== [Fin][Exitoso] Ejecucion test ==================>"