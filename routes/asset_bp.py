# 23.83.0981 - Muhammad Ardita Hilmi
from flask import Blueprint
from controllers.AssetController import get_assets, get_asset, create_asset, update_asset, delete_asset
asset_bp = Blueprint('asset_bp', __name__)
asset_bp.route('/api/assets',               methods=['GET']   )(get_assets)
asset_bp.route('/api/assets/<int:asset_id>', methods=['GET']   )(get_asset)
asset_bp.route('/api/assets',               methods=['POST']  )(create_asset)
asset_bp.route('/api/assets/<int:asset_id>', methods=['PUT']   )(update_asset)
asset_bp.route('/api/assets/<int:asset_id>', methods=['DELETE'])(delete_asset)
