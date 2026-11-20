# 23.83.0981 - Muhammad Ardita Hilmi
from config import db
from datetime import datetime

class Asset(db.Model):
    __tablename__ = 'assets'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), nullable=False)
    ip_address  = db.Column(db.String(50),  nullable=True)
    asset_type  = db.Column(db.String(100), nullable=False)
    status      = db.Column(db.String(50),  nullable=False, default='active')
    description = db.Column(db.Text,        nullable=True)
    owner_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    incidents       = db.relationship('Incident',      backref='asset', lazy=True)
    vulnerabilities = db.relationship('Vulnerability', backref='asset', lazy=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'ip_address': self.ip_address,
                'asset_type': self.asset_type, 'status': self.status,
                'description': self.description, 'owner_id': self.owner_id,
                'created_at': self.created_at.isoformat()}
