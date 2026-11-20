# 23.83.0981 - Muhammad Ardita Hilmi
# Automated Test - Cybersecurity Incident Management API
import pytest
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import dari app.py biar semua blueprint ke-register
from app import app
from config import db
from models.UserModel import User
from models.AssetModel import Asset
from models.IncidentModel import Incident
from models.VulnerabilityModel import Vulnerability
from models.AuditLogModel import AuditLog

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_cybersec.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            if User.query.count() == 0:
                db.session.add(User(username='test_admin', password='admin123',
                                    email='admin@test.id', role='admin'))
                db.session.commit()
            if Asset.query.count() == 0:
                db.session.add(Asset(name='Test Server', ip_address='10.0.0.1',
                                     asset_type='server', owner_id=1))
                db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

# ---- USER TESTS ----
def test_get_users_success(client):
    res = client.get('/api/users')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)

def test_create_user_success(client):
    payload = {'username': 'new_analyst', 'password': 'pass123',
               'email': 'analyst@test.id', 'role': 'analyst'}
    res = client.post('/api/users', json=payload)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['status'] == 'success'
    assert data['data']['username'] == 'new_analyst'

def test_create_user_missing_field(client):
    payload = {'username': 'incomplete_user'}
    res = client.post('/api/users', json=payload)
    assert res.status_code == 400
    data = json.loads(res.data)
    assert data['status'] == 'error'

def test_get_user_not_found(client):
    res = client.get('/api/users/9999')
    assert res.status_code == 404
    data = json.loads(res.data)
    assert data['status'] == 'error'

# ---- INCIDENT TESTS ----
def test_create_incident_success(client):
    payload = {'title': 'Test Incident', 'description': 'Test desc',
               'severity': 'high', 'reported_by': 1, 'asset_id': 1}
    res = client.post('/api/incidents', json=payload)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['data']['severity'] == 'high'

def test_create_incident_invalid_severity(client):
    payload = {'title': 'Bad Incident', 'description': 'Test',
               'severity': 'extreme', 'reported_by': 1}
    res = client.post('/api/incidents', json=payload)
    assert res.status_code == 400

def test_get_incidents_filter_severity(client):
    client.post('/api/incidents', json={'title': 'T1', 'description': 'D',
                'severity': 'critical', 'reported_by': 1})
    res = client.get('/api/incidents?severity=critical')
    assert res.status_code == 200
    data = json.loads(res.data)
    for item in data['data']:
        assert item['severity'] == 'critical'

def test_delete_incident_not_found(client):
    res = client.delete('/api/incidents/9999')
    assert res.status_code == 404

# ---- VULNERABILITY TESTS ----
def test_create_vulnerability_success(client):
    payload = {'title': 'Test SQLi', 'severity': 'high', 'asset_id': 1,
               'discovered_by': 1, 'description': 'SQL injection in login',
               'cve_id': 'CVE-2024-9999'}
    res = client.post('/api/vulnerabilities', json=payload)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['status'] == 'success'
    assert data['data']['cve_id'] == 'CVE-2024-9999'

def test_create_vulnerability_missing_field(client):
    payload = {'title': 'Incomplete Vuln', 'severity': 'low'}
    res = client.post('/api/vulnerabilities', json=payload)
    assert res.status_code == 400
    data = json.loads(res.data)
    assert data['status'] == 'error'

def test_get_vulnerability_not_found(client):
    res = client.get('/api/vulnerabilities/9999')
    assert res.status_code == 404

# ---- ASSET TESTS ----
def test_create_asset_success(client):
    payload = {'name': 'New Router', 'asset_type': 'network', 'owner_id': 1,
               'ip_address': '10.0.0.254', 'status': 'active'}
    res = client.post('/api/assets', json=payload)
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data['status'] == 'success'

def test_get_assets_success(client):
    res = client.get('/api/assets')
    assert res.status_code == 200

def test_create_asset_missing_owner(client):
    payload = {'name': 'No Owner Asset', 'asset_type': 'server'}
    res = client.post('/api/assets', json=payload)
    assert res.status_code == 400

# ---- AUDIT LOG TESTS ----
def test_get_audit_logs_success(client):
    client.post('/api/incidents', json={
        'title': 'Audit Test', 'description': 'D',
        'severity': 'low', 'reported_by': 1
    })
    res = client.get('/api/audit-logs')
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data['status'] == 'success'

def test_create_user_duplicate_username(client):
    client.post('/api/users', json={
        'username': 'dup_user', 'password': 'pass123', 'email': 'dup@test.id'
    })
    res = client.post('/api/users', json={
        'username': 'dup_user', 'password': 'other123', 'email': 'other@test.id'
    })
    assert res.status_code == 409

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
