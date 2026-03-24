"""
ML Model Training Script for HealthAssist AI
Uses a built-in symptom-disease dataset (no external files required).
Run: python ml/train_model.py
"""
import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# ─── Symptom–Disease Dataset ─────────────────────────────────────────────────
# Format: (disease, [list of symptoms])
DATASET = [
    ("Fungal infection", ["itching","skin_rash","nodal_skin_eruptions","dischromic_patches"]),
    ("Fungal infection", ["itching","skin_rash","nodal_skin_eruptions"]),
    ("Allergy", ["continuous_sneezing","shivering","chills","watering_from_eyes"]),
    ("Allergy", ["continuous_sneezing","shivering","chills","watering_from_eyes","fatigue"]),
    ("GERD", ["stomach_pain","acidity","ulcers_on_tongue","vomiting","cough","chest_pain"]),
    ("GERD", ["stomach_pain","acidity","ulcers_on_tongue","vomiting"]),
    ("Chronic cholestasis", ["itching","vomiting","yellowish_skin","nausea","loss_of_appetite","abdominal_pain","yellowing_of_eyes"]),
    ("Drug Reaction", ["itching","skin_rash","stomach_pain","burning_micturition","spotting_urination"]),
    ("Peptic ulcer disease", ["vomiting","indigestion","loss_of_appetite","abdominal_pain","passage_of_gases","internal_itching"]),
    ("AIDS", ["muscle_wasting","patches_in_throat","high_fever","extra_marital_contacts"]),
    ("Diabetes", ["fatigue","weight_loss","restlessness","lethargy","irregular_sugar_level","blurred_and_distorted_vision","obesity","excessive_hunger","increased_appetite","polyuria"]),
    ("Diabetes", ["fatigue","weight_loss","restlessness","lethargy","irregular_sugar_level","blurred_and_distorted_vision","polyuria"]),
    ("Gastroenteritis", ["vomiting","sunken_eyes","dehydration","diarrhoea"]),
    ("Bronchial Asthma", ["fatigue","cough","high_fever","breathlessness","family_history","mucoid_sputum"]),
    ("Bronchial Asthma", ["fatigue","cough","breathlessness","mucoid_sputum"]),
    ("Hypertension", ["headache","chest_pain","dizziness","loss_of_balance","lack_of_concentration"]),
    ("Hypertension", ["headache","chest_pain","dizziness"]),
    ("Migraine", ["acidity","indigestion","headache","blurred_and_distorted_vision","excessive_hunger","stiff_neck","depression","irritability","visual_disturbances"]),
    ("Migraine", ["headache","blurred_and_distorted_vision","stiff_neck","depression","irritability"]),
    ("Cervical spondylosis", ["back_pain","weakness_in_limbs","neck_pain","dizziness","loss_of_balance"]),
    ("Paralysis (brain hemorrhage)", ["vomiting","headache","weakness_in_limbs","altered_sensorium"]),
    ("Jaundice", ["itching","vomiting","fatigue","weight_loss","high_fever","yellowish_skin","dark_urine","abdominal_pain"]),
    ("Jaundice", ["itching","vomiting","fatigue","weight_loss","yellowish_skin","dark_urine"]),
    ("Malaria", ["chills","vomiting","high_fever","sweating","headache","nausea","diarrhoea","muscle_pain"]),
    ("Malaria", ["chills","vomiting","high_fever","sweating","headache","nausea"]),
    ("Chicken pox", ["itching","skin_rash","fatigue","lethargy","high_fever","headache","loss_of_appetite","mild_fever","swelled_lymph_nodes","malaise","red_spots_over_body"]),
    ("Dengue", ["skin_rash","chills","joint_pain","vomiting","fatigue","high_fever","headache","nausea","loss_of_appetite","pain_behind_the_eyes","back_pain","malaise","muscle_pain","red_spots_over_body"]),
    ("Dengue", ["skin_rash","chills","joint_pain","vomiting","fatigue","high_fever","headache","nausea"]),
    ("Typhoid", ["chills","vomiting","fatigue","high_fever","headache","nausea","constipation","abdominal_pain","diarrhoea","toxic_look_(typhos)","belly_pain"]),
    ("Typhoid", ["chills","vomiting","fatigue","high_fever","headache","nausea","constipation"]),
    ("hepatitis A", ["joint_pain","vomiting","yellowish_skin","dark_urine","nausea","loss_of_appetite","abdominal_pain","diarrhoea","mild_fever","yellowing_of_eyes","muscle_pain"]),
    ("hepatitis A", ["joint_pain","vomiting","yellowish_skin","dark_urine","nausea","loss_of_appetite"]),
    ("Hepatitis B", ["itching","fatigue","lethargy","yellowish_skin","dark_urine","nausea","loss_of_appetite","abdominal_pain","yellow_urine","yellowing_of_eyes","malaise","receiving_blood_transfusion","receiving_unsterile_injections"]),
    ("Hepatitis C", ["fatigue","yellowish_skin","nausea","loss_of_appetite","family_history","yellowing_of_eyes"]),
    ("Hepatitis D", ["joint_pain","vomiting","fatigue","yellowish_skin","dark_urine","nausea","loss_of_appetite","abdominal_pain","yellowing_of_eyes"]),
    ("Hepatitis E", ["joint_pain","vomiting","fatigue","high_fever","yellowish_skin","dark_urine","nausea","loss_of_appetite","abdominal_pain","yellowing_of_eyes","acute_liver_failure","coma","stomach_bleeding"]),
    ("Alcoholic hepatitis", ["vomiting","yellowish_skin","abdominal_pain","swelling_of_stomach","history_of_alcohol_consumption","fluid_overload","fatigue"]),
    ("Tuberculosis", ["chills","vomiting","fatigue","weight_loss","cough","high_fever","breathlessness","sweating","loss_of_appetite","mild_fever","yellowing_of_eyes","swelled_lymph_nodes","malaise","phlegm","blood_in_sputum","chest_pain"]),
    ("Tuberculosis", ["chills","fatigue","weight_loss","cough","high_fever","breathlessness","sweating","loss_of_appetite"]),
    ("Common Cold", ["continuous_sneezing","chills","fatigue","cough","high_fever","headache","swelled_lymph_nodes","malaise","phlegm","runny_nose","congestion","chest_pain","loss_of_smell","throat_irritation","redness_of_eyes","sinus_pressure","fast_heart_rate"]),
    ("Common Cold", ["continuous_sneezing","chills","fatigue","cough","headache","malaise","runny_nose","congestion","throat_irritation"]),
    ("Pneumonia", ["chills","fatigue","cough","high_fever","breathlessness","sweating","malaise","phlegm","blood_in_sputum","rusty_sputum"]),
    ("Pneumonia", ["chills","fatigue","cough","high_fever","breathlessness","sweating"]),
    ("Dimorphic hemmorhoids(piles)", ["constipation","pain_during_bowel_movements","pain_in_anal_region","bloody_stool","irritation_in_anus"]),
    ("Heart attack", ["vomiting","breathlessness","sweating","chest_pain"]),
    ("Varicose veins", ["fatigue","cramps","bruising","obesity","swollen_legs","swollen_blood_vessels","prominent_veins_on_calf"]),
    ("Hypothyroidism", ["fatigue","weight_gain","cold_hands_and_feets","mood_swings","lethargy","dizziness","puffy_face_and_eyes","enlarged_thyroid","brittle_nails","swollen_extremeties","depression","irritability","abnormal_menstruation"]),
    ("Hyperthyroidism", ["fatigue","mood_swings","weight_loss","restlessness","sweating","diarrhoea","fast_heart_rate","excessive_hunger","muscle_weakness","irritability","abnormal_menstruation"]),
    ("Hypoglycemia", ["fatigue","vomiting","anxiety","sweating","headache","nausea","blurred_and_distorted_vision","excessive_hunger","drying_and_tingling_lips","slurred_speech","irritability","palpitations"]),
    ("Osteoarthritis", ["joint_pain","neck_pain","knee_pain","hip_joint_pain","swelling_joints","painful_walking"]),
    ("Arthritis", ["muscle_weakness","stiff_neck","swelling_joints","movement_stiffness","painful_walking"]),
    ("(vertigo) Paroymsal Positional Vertigo", ["vomiting","headache","nausea","spinning_movements","loss_of_balance","unsteadiness"]),
    ("Acne", ["skin_rash","pus_filled_pimples","blackheads","scurring"]),
    ("Urinary tract infection", ["burning_micturition","bladder_discomfort","foul_smell_of_urine","continuous_feel_of_urine"]),
    ("Psoriasis", ["skin_rash","joint_pain","skin_peeling","silver_like_dusting","small_dents_in_nails","inflammatory_nails"]),
    ("Impetigo", ["skin_rash","high_fever","blister","red_sores_around_nose","yellow_crust_ooze"]),
]

# All unique symptoms
ALL_SYMPTOMS = sorted(set(s for _, syms in DATASET for s in syms))

def build_features(symptom_list, all_symptoms):
    vec = np.zeros(len(all_symptoms))
    for s in symptom_list:
        if s in all_symptoms:
            vec[all_symptoms.index(s)] = 1
    return vec

def train():
    print("Building dataset...")
    X, y = [], []
    for disease, symptoms in DATASET:
        X.append(build_features(symptoms, ALL_SYMPTOMS))
        y.append(disease)

    X = np.array(X)
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)

    print("Training Random Forest classifier...")
    clf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    clf.fit(X_train, y_train)

    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"[OK] Model trained. Test Accuracy: {acc*100:.1f}%")

    # Save artifacts
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    out_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(clf, os.path.join(out_dir, 'model.pkl'))
    joblib.dump(le, os.path.join(out_dir, 'label_encoder.pkl'))
    joblib.dump(ALL_SYMPTOMS, os.path.join(out_dir, 'symptom_list.pkl'))
    print(f"[OK] Saved model.pkl, label_encoder.pkl, symptom_list.pkl to {out_dir}")
    return acc

if __name__ == '__main__':
    train()
