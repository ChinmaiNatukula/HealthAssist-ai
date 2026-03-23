"""
Symptom-to-Disease rule-based prediction engine.
Maps sets of symptoms to most likely conditions.
"""

SYMPTOM_DB = {
    frozenset(['fever', 'cough', 'fatigue', 'headache']): {
        'disease': 'Influenza (Flu)',
        'description': 'A common viral respiratory infection causing fever, body aches, cough, and fatigue. Usually resolves in 1–2 weeks.',
        'next_steps': ['Rest at home and drink plenty of fluids', 'Take OTC fever reducers (paracetamol/ibuprofen)', 'Consult a doctor if fever persists beyond 3 days'],
        'severity': 'moderate',
        'icon': '🤧',
    },
    frozenset(['fever', 'cough', 'shortness of breath', 'loss of taste']): {
        'disease': 'COVID-19 (Suspected)',
        'description': 'Symptoms strongly indicate a possible COVID-19 infection. Loss of taste/smell is a hallmark symptom. Seek medical attention.',
        'next_steps': ['Isolate immediately and get tested', 'Monitor oxygen saturation with pulse oximeter', 'Seek emergency care if breathing becomes difficult'],
        'severity': 'high',
        'icon': '🦠',
    },
    frozenset(['headache', 'nausea', 'vomiting', 'fever', 'stiff neck']): {
        'disease': 'Meningitis (Suspected)',
        'description': 'Stiff neck combined with fever and headache may indicate meningitis. This is a medical emergency.',
        'next_steps': ['Seek emergency medical care immediately', 'Do not delay — this can be life-threatening', 'Call emergency services if symptoms worsen rapidly'],
        'severity': 'critical',
        'icon': '🚨',
    },
    frozenset(['chest pain', 'shortness of breath', 'sweating']): {
        'disease': 'Cardiac Event (Suspected)',
        'description': 'These symptoms may indicate a heart attack or serious cardiac event. Requires immediate medical attention.',
        'next_steps': ['Call emergency services immediately (102/108)', 'Sit or lie down calmly', 'Chew an aspirin if available and not allergic'],
        'severity': 'critical',
        'icon': '❤️‍🔥',
    },
    frozenset(['sore throat', 'fever', 'swollen glands']): {
        'disease': 'Strep Throat / Tonsillitis',
        'description': 'Bacterial throat infection causing pain, fever, and swollen lymph nodes. Antibiotics may be needed.',
        'next_steps': ['Visit a doctor for a throat swab test', 'Gargle with warm salt water for relief', 'Avoid sharing utensils to prevent spread'],
        'severity': 'mild',
        'icon': '🔴',
    },
    frozenset(['abdominal pain', 'diarrhea', 'nausea', 'vomiting']): {
        'disease': 'Gastroenteritis',
        'description': 'Common stomach bug causing digestive upset. Usually caused by viral or bacterial infection from contaminated food/water.',
        'next_steps': ['Stay hydrated with ORS (oral rehydration solution)', 'Avoid solid food for a few hours', 'Seek care if symptoms persist beyond 48 hours'],
        'severity': 'mild',
        'icon': '🤢',
    },
    frozenset(['joint pain', 'fever', 'rash', 'muscle pain']): {
        'disease': 'Dengue Fever',
        'description': 'A mosquito-borne viral disease. Warning signs include severe abdominal pain and sudden drop in fever.',
        'next_steps': ['Get a platelet count blood test done urgently', 'Stay hydrated with fluids and rest', 'Avoid aspirin/ibuprofen — use paracetamol only'],
        'severity': 'high',
        'icon': '🦟',
    },
    frozenset(['frequent urination', 'thirst', 'fatigue', 'blurred vision']): {
        'disease': 'Diabetes (Suspected)',
        'description': 'These symptoms are classic signs of uncontrolled blood sugar. A fasting blood glucose test is essential.',
        'next_steps': ['Get a fasting blood sugar test done', 'Consult an endocrinologist', 'Reduce sugar/carbohydrate intake immediately'],
        'severity': 'moderate',
        'icon': '🍭',
    },
    frozenset(['skin rash', 'itching', 'redness']): {
        'disease': 'Allergic Reaction / Dermatitis',
        'description': 'Skin inflammation caused by allergens, chemicals, or contact irritants. May require antihistamines.',
        'next_steps': ['Identify and avoid the allergen', 'Apply soothing lotion (calamine)', 'Take antihistamines for relief; see a dermatologist if severe'],
        'severity': 'mild',
        'icon': '🔴',
    },
    frozenset(['back pain', 'fever', 'painful urination']): {
        'disease': 'Urinary Tract Infection (UTI) / Kidney Infection',
        'description': 'Bacterial infection in the urinary tract that may have spread to the kidneys. Antibiotics are needed.',
        'next_steps': ['See a doctor for urine culture test', 'Drink at least 2–3 liters of water daily', 'Avoid caffeine and alcohol until fully recovered'],
        'severity': 'moderate',
        'icon': '🫘',
    },
}

GENERAL_SYMPTOM_RESPONSE = {
    'disease': 'General Illness',
    'description': 'Based on the symptoms you provided, a specific diagnosis could not be determined. Please consult a qualified medical professional for an accurate diagnosis.',
    'next_steps': ['Schedule an appointment with your doctor', 'Keep track of symptom onset, duration, and severity', 'Stay hydrated and get adequate rest'],
    'severity': 'unknown',
    'icon': '🩺',
}


def predict_disease(symptoms_list):
    """
    Given a list of symptom strings, find the best matching disease.
    Returns the disease info dict and a confidence percentage.
    """
    if not symptoms_list:
        return GENERAL_SYMPTOM_RESPONSE, 0

    symptoms_set = set(s.lower().strip() for s in symptoms_list)
    best_match = None
    best_score = 0

    for disease_symptoms, disease_info in SYMPTOM_DB.items():
        overlap = len(symptoms_set & disease_symptoms)
        total = len(disease_symptoms | symptoms_set)
        score = overlap / total if total > 0 else 0
        if score > best_score:
            best_score = score
            best_match = disease_info

    confidence = round(best_score * 100)

    if confidence < 20:
        return GENERAL_SYMPTOM_RESPONSE, confidence

    return best_match, confidence


# List of all known symptoms for the front-end autocomplete
ALL_SYMPTOMS = sorted(set(
    symptom
    for symptom_set in SYMPTOM_DB.keys()
    for symptom in symptom_set
))
