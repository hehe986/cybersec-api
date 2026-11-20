# 23.83.0981 - Muhammad Ardita Hilmi
from flask import jsonify, request
from models.UserModel import User
from models.AuditLogModel import AuditLog
from config import db, hash_password

def _log(action, entity_id, desc, performed_by):
    db.session.add(AuditLog(
        action=action, entity_type='user',
        entity_id=entity_id, description=desc,
        performed_by=performed_by
    ))

def get_users():
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    role     = request.args.get('role')
    query    = User.query
    if role:
        query = query.filter_by(role=role)
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({'status': 'success', 'data': [u.to_dict() for u in users.items],
                    'total': users.total, 'page': page, 'per_page': per_page}), 200

def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    return jsonify({'status': 'success', 'data': user.to_dict()}), 200

def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Request body required'}), 400
    for field in ['username', 'password', 'email']:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'{field} is required'}), 400
    if len(data['password']) < 6:
        return jsonify({'status': 'error', 'message': 'Password min 6 characters'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'status': 'error', 'message': 'Email already exists'}), 409
    user = User(
        username=data['username'],
        password=hash_password(data['password']),   # hashed
        email=data['email'],
        role=data.get('role', 'analyst')
    )
    db.session.add(user)
    db.session.flush()
    _log('CREATE', user.id, f"User '{user.username}' registered", user.id)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User created', 'data': user.to_dict()}), 201

def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    data = request.get_json()
    user.email     = data.get('email',     user.email)
    user.role      = data.get('role',      user.role)
    user.is_active = data.get('is_active', user.is_active)
    if 'password' in data:
        user.password = hash_password(data['password'])
    _log('UPDATE', user.id, f"User '{user.username}' updated", user.id)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User updated', 'data': user.to_dict()}), 200

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    _log('DELETE', user.id, f"User '{user.username}' deleted", user.id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'User deleted'}), 200