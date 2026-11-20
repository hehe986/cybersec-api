# 23.83.0981 - Muhammad Ardita Hilmi
from flask import Blueprint
from controllers.AuditLogController import get_audit_logs, get_audit_log
auditlog_bp = Blueprint('auditlog_bp', __name__)
auditlog_bp.route('/api/audit-logs',               methods=['GET'])(get_audit_logs)
auditlog_bp.route('/api/audit-logs/<int:log_id>',  methods=['GET'])(get_audit_log)
