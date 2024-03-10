import json

datos_en_memoria = None

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

# Función que permite realizar el cargue inicial de plan nutricional
def cargue_inicial():
    # Cargar plan nutricional desde json file
    with open('utilities/planNutricional.json') as archivo_json:
        global datos_en_memoria
        datos_en_memoria = json.load(archivo_json)

# Función que permite realizar el cargue inicial de plan nutricional
def recomendacion_planes_nutricionales():
    global datos_en_memoria
    return datos_en_memoria

# Función que permite realizar el cargue inicial de plan nutricional
def cargue_inicial_plan_nutricional(db, PlanNutricional):
    # Consultar la tabla en BD
    registros = db.session.query(PlanNutricional).all()
    # Validar si ya existen registros
    if len(registros) == 0:
        # Cargar plan nutricional desde json file
        with open('utilities/planNutricional.json') as archivo_json:
            planes_nutricionales = json.load(archivo_json)
        # Registrar plan nutricional
        for plan_nutricional, info in planes_nutricionales.items():
            registro = []
            registro.append(plan_nutricional)
            for dato, valor in info.items():
                registro.append(valor)
            print(registro)
            nuevo_plan_nutricional = PlanNutricional(plan_nutricional=registro[0],
                                                menus=registro[1],                                                
                                                proposito=registro[2],
                                                clasificacion=registro[3]
                                            )
            db.session.add(nuevo_plan_nutricional)
            db.session.commit()
        db.session.close()