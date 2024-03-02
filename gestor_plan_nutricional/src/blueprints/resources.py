from flask import request, Blueprint
from commands.plan_nutricional import DarPlanNutricional
from flask.json import jsonify

planes_nutricionales_blueprint = Blueprint(name='nutricion', import_name=__name__, url_prefix='/nutricion')

# Recurso que expone la funcionalidad healthcheck
@planes_nutricionales_blueprint.route('/ping', methods=['GET'])
def health():
    return "pong"

@planes_nutricionales_blueprint.route('/plan-nutricional', methods=['POST'])
def dar_plan_nutricional():
    data = request.get_json()
    return DarPlanNutricional(data).execute()
