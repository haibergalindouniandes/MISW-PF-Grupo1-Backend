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

cat $TEST_PATH/$COVERAGE_FILE
COVERAGE=$(grep -oP 'Statements\s+:\s+\K\d+\.\d+' $TEST_PATH/$COVERAGE_FILE)
echo "La cobertura total de las pruebas fue [$COVERAGE]"
decimal=$(awk "BEGIN {print $COVERAGE}")
if (( $(echo "$decimal < $MIN_COVERAGE" | bc -l) )); then
  echo "Error: La cobertura obtenida [$COVERAGE] es MENOR que la cobertura minima [$MIN_COVERAGE] requerida para pasar las pruebas"
  echo "<================== [Fin][Error] Ejecución de pruebas unitarias y cobertura ==================>"
  exit 1
fi
echo "La cobertura obtenida [$COVERAGE] CUMPLE con los criterios para pasar las pruebas"
mv $COVERAGE_PATH $TEST_PATH/
echo "Se mueve directorio [$COVERAGE_PATH] a [$TEST_PATH/$COVERAGE_PATH]"
echo "<================== [Fin][Exitoso] Ejecucion test ==================>"