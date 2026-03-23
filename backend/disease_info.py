import json
import os
from flask import Blueprint, jsonify

disease_info_bp = Blueprint('disease_info', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'ml', 'disease_data.json')

_data_cache = None

def _load_data():
    global _data_cache
    if _data_cache is None:
        with open(DATA_FILE, 'r') as f:
            _data_cache = json.load(f)
    return _data_cache

@disease_info_bp.route('/<string:name>', methods=['GET'])
def get_disease_info(name):
    data = _load_data()
    key = name.strip().lower().replace(' ', '_').replace('-', '_')
    # Try exact match first, then partial
    info = data.get(key)
    if not info:
        for k, v in data.items():
            if key in k or k in key:
                info = v
                break
    if not info:
        return jsonify({'error': f'No information found for: {name}'}), 404
    return jsonify(info), 200


@disease_info_bp.route('', methods=['GET'])
def list_diseases():
    data = _load_data()
    return jsonify({'diseases': list(data.keys())}), 200
