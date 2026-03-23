import json
import joblib
import numpy as np
import os
from flask import Blueprint, request, jsonify

predict_bp = Blueprint('predict', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR = os.path.join(BASE_DIR, 'ml')

# Load model artifacts at startup
try:
    model = joblib.load(os.path.join(ML_DIR, 'model.pkl'))
    label_encoder = joblib.load(os.path.join(ML_DIR, 'label_encoder.pkl'))
    symptom_list = joblib.load(os.path.join(ML_DIR, 'symptom_list.pkl'))
    MODEL_LOADED = True
except Exception as e:
    print(f"[WARN] Could not load ML model: {e}")
    MODEL_LOADED = False


@predict_bp.route('', methods=['POST'])
def predict():
    if not MODEL_LOADED:
        return jsonify({'error': 'ML model not loaded. Run train_model.py first.'}), 503

    data = request.get_json()
    symptoms = data.get('symptoms', [])

    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400

    # Build feature vector
    feature_vector = np.zeros(len(symptom_list))
    for sym in symptoms:
        sym_clean = sym.strip().lower().replace(' ', '_')
        if sym_clean in symptom_list:
            idx = symptom_list.index(sym_clean)
            feature_vector[idx] = 1

    # Predict top 3
    proba = model.predict_proba([feature_vector])[0]
    top3_idx = np.argsort(proba)[::-1][:3]
    results = []
    for idx in top3_idx:
        disease = label_encoder.inverse_transform([idx])[0]
        prob = round(float(proba[idx]) * 100, 1)
        if prob > 0.1:
            results.append({'disease': disease, 'probability': prob})

    return jsonify({'predictions': results}), 200


@predict_bp.route('/symptoms', methods=['GET'])
def get_symptoms():
    """Return the full list of valid symptoms for the frontend selector."""
    if not MODEL_LOADED:
        return jsonify({'symptoms': []}), 200
    display = [s.replace('_', ' ').title() for s in symptom_list]
    return jsonify({'symptoms': display, 'raw': symptom_list}), 200
