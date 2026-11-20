# 23.83.0981 - Muhammad Ardita Hilmi
from flask import Blueprint
from controllers.IncidentController import get_incidents, get_incident, create_incident, update_incident, delete_incident
incident_bp = Blueprint('incident_bp', __name__)
incident_bp.route('/api/incidents',                   methods=['GET']   )(get_incidents)
incident_bp.route('/api/incidents/<int:incident_id>', methods=['GET']   )(get_incident)
incident_bp.route('/api/incidents',                   methods=['POST']  )(create_incident)
incident_bp.route('/api/incidents/<int:incident_id>', methods=['PUT']   )(update_incident)
incident_bp.route('/api/incidents/<int:incident_id>', methods=['DELETE'])(delete_incident)
