# 23.83.0981 - Muhammad Ardita Hilmi
from flask import jsonify, request
from models.IncidentModel import Incident
from models.AuditLogModel import AuditLog
from config import db

VALID_SEVERITY = ['low', 'medium', 'high', 'critical']
VALID_STATUS   = ['open', 'investigating', 'resolved', 'closed']

def log_action(action, entity_id, desc, performed_by):
    log = AuditLog(action=action, entity_type='incident', entity_id=entity_id,
                   description=desc, performed_by=performed_by)
    db.session.add(log)

def get_incidents():
    severity = request.args.get('severity')
    status   = request.args.get('status')
    search   = request.args.get('search')
    sort_by  = request.args.get('sort_by', 'created_at')
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query    = Incident.query
    if severity: query = query.filter_by(severity=severity)
    if status:   query = query.filter_by(status=status)
    if search:   query = query.filter(Incident.title.ilike(f'%{search}%'))
    if sort_by == 'severity': query = query.order_by(Incident.severity)
    else:                     query = query.order_by(Incident.created_at.desc())
    incidents = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({'status': 'success', 'data': [i.to_dict() for i in incidents.items],
                    'total': incidents.total, 'page': page}), 200

def get_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({'status': 'error', 'message': 'Incident not found'}), 404
    return jsonify({'status': 'success', 'data': incident.to_dict()}), 200

def create_incident():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Request body required'}), 400
    required = ['title', 'description', 'severity', 'reported_by']
    for field in required:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'{field} is required'}), 400
    if data['severity'] not in VALID_SEVERITY:
        return jsonify({'status': 'error', 'message': f'severity must be one of {VALID_SEVERITY}'}), 400
    incident = Incident(title=data['title'], description=data['description'],
                        severity=data['severity'], status=data.get('status', 'open'),
                        reported_by=data['reported_by'], asset_id=data.get('asset_id'))
    db.session.add(incident)
    db.session.flush()
    log_action('CREATE', incident.id, f"Incident '{incident.title}' reported", data['reported_by'])
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Incident created', 'data': incident.to_dict()}), 201

def update_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({'status': 'error', 'message': 'Incident not found'}), 404
    data = request.get_json()
    if 'severity' in data and data['severity'] not in VALID_SEVERITY:
        return jsonify({'status': 'error', 'message': f'severity must be one of {VALID_SEVERITY}'}), 400
    if 'status' in data and data['status'] not in VALID_STATUS:
        return jsonify({'status': 'error', 'message': f'status must be one of {VALID_STATUS}'}), 400
    incident.title       = data.get('title',       incident.title)
    incident.description = data.get('description', incident.description)
    incident.severity    = data.get('severity',    incident.severity)
    incident.status      = data.get('status',      incident.status)
    incident.asset_id    = data.get('asset_id',    incident.asset_id)
    log_action('UPDATE', incident.id, f"Incident '{incident.title}' updated", incident.reported_by)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Incident updated', 'data': incident.to_dict()}), 200

def delete_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({'status': 'error', 'message': 'Incident not found'}), 404
    log_action('DELETE', incident.id, f"Incident '{incident.title}' deleted", incident.reported_by)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Incident deleted'}), 200
