# 23.83.0981 - Muhammad Ardita Hilmi
from config import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(100), nullable=False, unique=True)
    password   = db.Column(db.String(255), nullable=False)
    email      = db.Column(db.String(150), nullable=False, unique=True)
    role       = db.Column(db.String(50),  nullable=False, default='analyst')
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    incidents       = db.relationship('Incident',      backref='reporter',   lazy=True, foreign_keys='Incident.reported_by')
    assets          = db.relationship('Asset',         backref='owner',      lazy=True, foreign_keys='Asset.owner_id')
    vulnerabilities = db.relationship('Vulnerability', backref='discoverer', lazy=True, foreign_keys='Vulnerability.discovered_by')
    audit_logs      = db.relationship('AuditLog',      backref='actor',      lazy=True, foreign_keys='AuditLog.performed_by')

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email,
                'role': self.role, 'is_active': self.is_active, 'created_at': self.created_at.isoformat()}
