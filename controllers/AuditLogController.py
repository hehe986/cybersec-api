# 23.83.0981 - Muhammad Ardita Hilmi
from flask import jsonify, request
from models.AuditLogModel import AuditLog
from config import db

def get_audit_logs():
    entity_type  = request.args.get('entity_type')
    action       = request.args.get('action')
    performed_by = request.args.get('performed_by', type=int)
    page         = request.args.get('page', 1, type=int)
    per_page     = request.args.get('per_page', 20, type=int)
    query        = AuditLog.query
    if entity_type:  query = query.filter_by(entity_type=entity_type)
    if action:       query = query.filter_by(action=action)
    if performed_by: query = query.filter_by(performed_by=performed_by)
    logs = query.order_by(AuditLog.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({'status': 'success', 'data': [l.to_dict() for l in logs.items],
                    'total': logs.total, 'page': page}), 200

def get_audit_log(log_id):
    log = AuditLog.query.get(log_id)
    if not log:
        return jsonify({'status': 'error', 'message': 'Log not found'}), 404
    return jsonify({'status': 'success', 'data': log.to_dict()}), 200
