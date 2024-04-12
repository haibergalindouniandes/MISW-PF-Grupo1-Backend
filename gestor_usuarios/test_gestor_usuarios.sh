#!/bin/bash

####################################################################################################################################
echo "<================== [Inicio] Configuración ==================>"
TEST_PATH=tests-results-usuarios
mkdir -p $TEST_PATH
echo "Se realiza la creación del directorio [$TEST_PATH]"
MIN_COVERAGE=80
echo "La cobertura minima establecida para pasar las pruebas es [$MIN_COVERAGE]"
COVERAGE_FILE=usuarios-coverage-results.txt
echo "El archivo con los resultados de las pruebas de cobertura es [$COVERAGE_FILE]"
echo "<================== [Fin] Configuración ==================>"
echo "<================== [Inicio] instalacion de dependencias ==================>"
pwd
pip install -r gestor_usuarios/requirements.txt
echo "<================== [Fin][Exitoso] instalacion dependencias ==================>"
echo "<================== [Inicio] Ejecucion test ==================>"
pwd
cd /workspace/gestor_usuarios
pytest --cov-fail-under=80 --cov=src --cov-report=html:cov_report --junitxml=${SHORT_SHA}_usuarios_test_log.xml


echo "Se mueve directorio [$COVERAGE_PATH] a [$TEST_PATH/$COVERAGE_PATH]"
echo "<================== [Fin][Exitoso] Ejecucion test ==================>"