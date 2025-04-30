from flask import Blueprint, render_template
from ..api.autenticacion import autenticacion

api = Blueprint('api', __name__)

api.register_blueprint(autenticacion)