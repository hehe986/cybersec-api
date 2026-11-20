# 23.83.0981 - Muhammad Ardita Hilmi
from config import db
from datetime import datetime

class Incident(db.Model):
    __tablename__ = 'incidents'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        nullable=False)
    severity    = db.Column(db.String(20),  nullable=False)
    status      = db.Column(db.String(50),  nullable=False, default='open')
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'),  nullable=False)
    asset_id    = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'description': self.description,
                'severity': self.severity, 'status': self.status,
                'reported_by': self.reported_by, 'asset_id': self.asset_id,
                'created_at': self.created_at.isoformat(), 'updated_at': self.updated_at.isoformat()}
