# 23.83.0981 - Muhammad Ardita Hilmi
from config import hash_password
from config import app, db
from models.UserModel import User
from models.AssetModel import Asset
from models.IncidentModel import Incident
from models.VulnerabilityModel import Vulnerability
from models.AuditLogModel import AuditLog

with app.app_context():
    db.create_all()

    if User.query.count() == 0:
        users = [
            User(username='admin_hilmi',  password=hash_password('admin123'),   email='admin@cybersec.id',   role='admin'),
            User(username='analyst_sari', password=hash_password('analyst123'), email='sari@cybersec.id',     role='analyst'),
            User(username='viewer_budi',  password=hash_password('viewer123'),  email='budi@cybersec.id',     role='viewer'),
        ]
        db.session.add_all(users)
        db.session.commit()

    if Asset.query.count() == 0:
        assets = [
            Asset(name='Web Server Prod',   ip_address='192.168.1.10', asset_type='server',   status='active',      description='Production web server', owner_id=1),
            Asset(name='DB Server',          ip_address='192.168.1.20', asset_type='server',   status='active',      description='MySQL database server', owner_id=1),
            Asset(name='Employee Laptop-01', ip_address='192.168.2.5',  asset_type='endpoint', status='compromised', description='Finance dept laptop',   owner_id=2),
            Asset(name='Core Switch',        ip_address='10.0.0.1',     asset_type='network',  status='active',      description='Core network switch',   owner_id=1),
            Asset(name='HR Portal',          ip_address='192.168.1.30', asset_type='app',      status='active',      description='Internal HR portal',    owner_id=2),
        ]
        db.session.add_all(assets)
        db.session.commit()

    if Incident.query.count() == 0:
        incidents = [
            Incident(title='Phishing Attack Detected',  description='User received phishing email with malicious link', severity='high',     status='investigating', reported_by=2, asset_id=3),
            Incident(title='Unauthorized SSH Access',   description='Failed SSH brute force attempts on web server',    severity='critical', status='open',          reported_by=1, asset_id=1),
            Incident(title='Malware on Endpoint',       description='Ransomware detected on finance laptop',            severity='critical', status='investigating', reported_by=2, asset_id=3),
            Incident(title='Suspicious DB Query',       description='Unusual bulk data export from HR portal DB',       severity='medium',   status='open',          reported_by=2, asset_id=2),
        ]
        db.session.add_all(incidents)
        db.session.commit()

    if Vulnerability.query.count() == 0:
        vulns = [
            Vulnerability(title='Log4Shell RCE',        cve_id='CVE-2021-44228', severity='critical', status='open',      description='Remote code execution via Log4j',     asset_id=1, discovered_by=2),
            Vulnerability(title='SQL Injection in HR',  cve_id='CVE-2024-1234',  severity='high',     status='mitigated', description='SQLi found in HR portal login form',  asset_id=5, discovered_by=2),
            Vulnerability(title='Outdated OpenSSL',     cve_id='CVE-2022-0778',  severity='medium',   status='patched',   description='Outdated OpenSSL on DB server',       asset_id=2, discovered_by=1),
            Vulnerability(title='Default SNMP Password',cve_id=None,             severity='low',      status='open',      description='Core switch uses default SNMP string', asset_id=4, discovered_by=1),
        ]
        db.session.add_all(vulns)
        db.session.commit()

    print("Seed data berhasil dimasukkan!")
    print(f"Users: {User.query.count()}, Assets: {Asset.query.count()}")
    print(f"Incidents: {Incident.query.count()}, Vulnerabilities: {Vulnerability.query.count()}")
