# 23.83.0981 - Muhammad Ardita Hilmi
from flask import jsonify, request
from models.AssetModel import Asset
from models.AuditLogModel import AuditLog
from config import db

def log_action(action, entity_type, entity_id, desc, performed_by):
    log = AuditLog(action=action, entity_type=entity_type, entity_id=entity_id,
                   description=desc, performed_by=performed_by)
    db.session.add(log)

def get_assets():
    status     = request.args.get('status')
    asset_type = request.args.get('asset_type')
    search     = request.args.get('search')
    sort_by    = request.args.get('sort_by', 'created_at')
    page       = request.args.get('page', 1, type=int)
    per_page   = request.args.get('per_page', 10, type=int)
    query      = Asset.query
    if status:     query = query.filter_by(status=status)
    if asset_type: query = query.filter_by(asset_type=asset_type)
    if search:     query = query.filter(Asset.name.ilike(f'%{search}%'))  # <-- tambahan
    if sort_by == 'name': query = query.order_by(Asset.name)
    else:                 query = query.order_by(Asset.created_at.desc())
    assets = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({'status': 'success', 'data': [a.to_dict() for a in assets.items],
                    'total': assets.total, 'page': page}), 200

def get_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'status': 'error', 'message': 'Asset not found'}), 404
    return jsonify({'status': 'success', 'data': asset.to_dict()}), 200

def create_asset():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Request body required'}), 400
    required = ['name', 'asset_type', 'owner_id']
    for field in required:
        if field not in data:
            return jsonify({'status': 'error', 'message': f'{field} is required'}), 400
    asset = Asset(name=data['name'], ip_address=data.get('ip_address'),
                  asset_type=data['asset_type'], status=data.get('status', 'active'),
                  description=data.get('description'), owner_id=data['owner_id'])
    db.session.add(asset)
    db.session.flush()
    log_action('CREATE', 'asset', asset.id, f"Asset '{asset.name}' created", data['owner_id'])
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Asset created', 'data': asset.to_dict()}), 201

def update_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'status': 'error', 'message': 'Asset not found'}), 404
    data = request.get_json()
    asset.name        = data.get('name',        asset.name)
    asset.ip_address  = data.get('ip_address',  asset.ip_address)
    asset.asset_type  = data.get('asset_type',  asset.asset_type)
    asset.status      = data.get('status',      asset.status)
    asset.description = data.get('description', asset.description)
    log_action('UPDATE', 'asset', asset.id, f"Asset '{asset.name}' updated", asset.owner_id)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Asset updated', 'data': asset.to_dict()}), 200

def delete_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({'status': 'error', 'message': 'Asset not found'}), 404
    log_action('DELETE', 'asset', asset.id, f"Asset '{asset.name}' deleted", asset.owner_id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Asset deleted'}), 200
