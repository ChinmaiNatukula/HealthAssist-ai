import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Report
from extensions import db

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('', methods=['GET'])
@jwt_required()
def get_reports():
    uid = get_jwt_identity()
    reports = Report.query.filter_by(user_id=uid).order_by(Report.timestamp.desc()).all()
    return jsonify({'reports': [r.to_dict() for r in reports]}), 200


@reports_bp.route('', methods=['POST'])
@jwt_required()
def save_report():
    uid = get_jwt_identity()
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    predictions = data.get('predictions', [])

    report = Report(
        user_id=uid,
        symptoms=json.dumps(symptoms),
        predictions=json.dumps(predictions)
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'report': report.to_dict()}), 201


@reports_bp.route('/<int:report_id>', methods=['DELETE'])
@jwt_required()
def delete_report(report_id):
    uid = get_jwt_identity()
    report = Report.query.filter_by(id=report_id, user_id=uid).first()
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    db.session.delete(report)
    db.session.commit()
    return jsonify({'message': 'Report deleted'}), 200
