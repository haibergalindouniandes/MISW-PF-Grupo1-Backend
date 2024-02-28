from flask import request, Blueprint
from flask.json import jsonify
from utilities.utilities import formatDateTimeToUTC

entrenamientos_blueprint = Blueprint('entrenamientos', __name__)

# Recurso que expone la funcionalidad healthcheck
@entrenamientos_blueprint.route('/entrenamientos/ping', methods=['GET'])
def health():
    return "pong"