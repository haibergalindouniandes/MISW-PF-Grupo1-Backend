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
pip install -r gestor_usuarios/requirements.txt
echo "<================== [Fin][Exitoso] instalacion dependencias ==================>"
echo "<================== [Inicio] Ejecucion test ==================>"
pwd
cd /workspace/gestor_usuarios
git pull
git checkout feature_gestor_usuarios
git pull
pytest --cov-fail-under=80 --cov=src --cov-report=html:cov_report
echo "<================== [Fin][Exitoso] Ejecucion test ==================>"