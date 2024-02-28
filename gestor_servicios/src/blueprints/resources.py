from flask import request, Blueprint
from flask.json import jsonify
from utilities.utilities import formatDateTimeToUTC

servicios_blueprint = Blueprint('servicios', __name__)

# Recurso que expone la funcionalidad healthcheck
@servicios_blueprint.route('/servicios/ping', methods=['GET'])
def health():
    return "pong"