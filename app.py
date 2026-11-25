# 23.83.0981 - Muhammad Ardita Hilmi
# UTS Pemrograman Web Lanjut - Cybersecurity Incident Management API
from config import app, db
from routes.user_bp import user_bp
from routes.asset_bp import asset_bp
from routes.incident_bp import incident_bp
from routes.vulnerability_bp import vulnerability_bp
from routes.auditlog_bp import auditlog_bp

app.register_blueprint(user_bp)
app.register_blueprint(asset_bp)
app.register_blueprint(incident_bp)
app.register_blueprint(vulnerability_bp)
app.register_blueprint(auditlog_bp)

with app.app_context():
    db.create_all()

@app.errorhandler(404)
def not_found(e):
    from flask import jsonify
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    from flask import jsonify
    return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(debug=True)
