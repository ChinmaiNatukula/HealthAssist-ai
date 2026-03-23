"""
Keyword-based AI chatbot response engine for HealthAssist AI.
Covers medical QA, symptoms, diet, emergency, general health.
"""

import random

RESPONSES = {
    # Greetings
    'hello': ["Hello! 👋 I'm HealthAssist AI. How can I help you today?", "Hi there! Ask me anything about your health. 😊"],
    'hi': ["Hi! Welcome to HealthAssist AI 🏥. What health query do you have?"],
    'hey': ["Hey! I'm here to help with your health questions. 😊"],
    'help': ["I can answer health questions, give diet advice, explain symptoms, and guide you when to see a doctor. Just ask!"],
    'bye': ["Take care! Remember — your health is your greatest wealth. 💙", "Goodbye! Stay healthy! 🌿"],

    # Fever
    'fever': [
        "🌡️ **Fever Management:**\n- Drink plenty of fluids (water, ORS, coconut water)\n- Paracetamol/acetaminophen helps reduce fever safely\n- Rest in a cool room\n- Seek care if fever exceeds 103°F (39.4°C) or persists >3 days\n- Never give aspirin to children with fever"
    ],
    'temperature': ["For high temperature, take paracetamol, drink fluids, and rest. Seek medical help if it persists or rises above 103°F."],

    # Headache
    'headache': [
        "🤕 **Headache Relief Tips:**\n- Stay hydrated — dehydration is a common cause\n- Rest in a quiet, dark room\n- OTC painkillers (ibuprofen/paracetamol)\n- Apply cold/warm compress to forehead\n⚠️ See a doctor if severe, sudden, or with stiff neck/vision changes"
    ],
    'migraine': ["🤯 Migraines need proper management. Triptans are often prescribed. Triggers include stress, bright lights, skipped meals. Keep a migraine diary and consult a neurologist."],

    # Cold & Cough
    'cold': [
        "🤧 **Common Cold:**\n- No cure, but rest and fluids help\n- Saline nasal spray for congestion\n- Honey + ginger tea soothes throat\n- Usually resolves in 7–10 days\n- See a doctor if it lasts >10 days"
    ],
    'cough': [
        "For a cough:\n- Honey + warm water/tea helps soothe\n- Stay hydrated\n- Use a humidifier\n- If dry cough persists >3 weeks, consult a doctor to rule out TB or asthma"
    ],
    'sore throat': ["Gargle with warm salt water, drink warm fluids, and try antiseptic lozenges. If you have pus on tonsils or high fever, see a doctor — you may need antibiotics."],

    # Stomach issues
    'stomach': ["For stomach pain:\n- Avoid spicy/fatty foods\n- Ginger tea helps reduce nausea\n- See a doctor for severe/persistent pain or bloody stools"],
    'diarrhea': ["💧 Stay hydrated with ORS. Eat bland foods (rice, banana, toast). Avoid dairy. Seek care if it lasts >2 days or if you see blood."],
    'nausea': ["For nausea, try ginger tea, small meals, and rest. Avoid strong odors. If vomiting repeatedly, see a doctor to prevent dehydration."],
    'vomiting': ["Stay hydrated with small sips of water/ORS. If vomiting persists >24 hours or you can't keep fluids down, seek medical attention."],
    'constipation': ["🥦 High-fiber diet (fruits, vegetables, whole grains), drink 8+ glasses of water daily, and exercise regularly. Avoid laxatives without medical advice."],
    'acidity': ["🔥 Avoid spicy/oily food, eat smaller meals, don't lie down right after eating. Antacids provide quick relief. Talk to a doctor for recurring GERD."],

    # Diabetes
    'diabetes': [
        "🩸 **Diabetes Management:**\n- Monitor blood glucose regularly\n- Low glycemic diet (whole grains, leafy veggies)\n- Regular exercise (30 min/day)\n- Take prescribed medications consistently\n- Regular HbA1c tests every 3 months"
    ],
    'sugar': ["Reduce simple sugars — choose whole grains, fruits with fiber, and vegetables. Exercise helps cells use glucose better. Consult a diabetologist for personalized advice."],
    'insulin': ["Insulin therapy is crucial for Type 1 and some Type 2 diabetics. Never skip doses. Store insulin properly and rotate injection sites."],

    # Blood pressure
    'blood pressure': [
        "💊 **Hypertension Tips:**\n- Reduce sodium (salt) intake\n- DASH diet: fruits, veggies, low-fat dairy\n- Exercise regularly\n- Limit alcohol and quit smoking\n- Take antihypertensives as prescribed"
    ],
    'hypertension': ["Monitor BP regularly. Keep it below 120/80 mmHg. Stress reduction, diet, and medication if prescribed are key."],
    'bp': ["Normal BP is below 120/80 mmHg. Monitor regularly and consult a cardiologist if it stays elevated."],

    # Heart
    'heart': ["❤️ Heart health: Regular exercise, low saturated fat diet, no smoking, manage stress. Get annual check-ups after 40."],
    'chest pain': ["⚠️ **IMPORTANT:** Chest pain can indicate a heart attack. If accompanied by sweating, arm pain, or breathing difficulty — CALL EMERGENCY SERVICES IMMEDIATELY (102/108)."],

    # Mental health
    'stress': ["🧘 Manage stress with deep breathing, meditation, regular sleep, and exercise. Talk to someone you trust. Professional counseling is very effective."],
    'anxiety': ["For anxiety:\n- Practice mindfulness and deep breathing (4-7-8 technique)\n- Limit caffeine\n- Regular exercise releases endorphins\n- Consider CBT therapy for chronic anxiety"],
    'depression': ["💙 Depression is a real medical condition. Please speak with a mental health professional. You're not alone. Therapy and medication can help significantly."],
    'sleep': ["😴 Sleep Tips:\n- 7–9 hours for adults\n- Fixed sleep/wake schedule\n- No screens 1 hour before bed\n- Cool, dark bedroom\n- Avoid caffeine after 2 PM"],
    'insomnia': ["For insomnia: establish a bedtime routine, avoid naps, limit caffeine/alcohol, and try relaxation techniques. See a doctor if it persists >1 month."],

    # Skin
    'skin': ["🧴 Skin care: Stay hydrated, use sunscreen daily, moisturize, and eat antioxidant-rich foods. See a dermatologist for persistent rashes or changes in moles."],
    'rash': ["For rashes: avoid scratching, apply calamine lotion, take antihistamines for allergic rashes. See a doctor if spreading, painful, or with fever."],
    'acne': ["🫧 Acne: Wash face gently twice daily, avoid touching face, use non-comedogenic products. Salicylic acid or benzoyl peroxide helps. See a dermatologist for severe acne."],

    # Nutrition & Diet
    'diet': [
        "🥗 **Balanced Diet Basics:**\n- 50% plate: vegetables & fruits\n- 25%: whole grains\n- 25%: lean protein (fish, legumes, eggs)\n- Limit processed foods, sugar, and trans fats\n- Drink 8+ glasses of water daily"
    ],
    'nutrition': ["Eat a rainbow of vegetables, lean proteins, whole grains, and healthy fats (nuts, avocado, olive oil). Vitamins and minerals from whole foods are best absorbed."],
    'vitamin': ["Common deficiencies in India: Vitamin D (sunlight + supplementation), Vitamin B12 (especially vegetarians), Iron. Get blood tests to know your levels."],
    'protein': ["Good protein sources: eggs, fish, chicken, lentils (dal), paneer, tofu, Greek yogurt. Aim for 0.8g of protein per kg of body weight daily."],
    'water': ["💧 Drink 8–10 glasses of water daily. More if you exercise or it's hot. Dehydration causes fatigue, headaches, and poor concentration."],

    # Exercise
    'exercise': ["🏃 Aim for 150 minutes of moderate exercise per week. Include cardio (walking, cycling), strength training, and flexibility exercises. Start slow if you're a beginner!"],
    'weight': ["For healthy weight loss: calorie deficit (eat less, move more), strength training, adequate sleep, and stress management. Avoid crash diets."],
    'obesity': ["Obesity management requires lifestyle changes: balanced diet, regular exercise, behavioral changes, and possibly medical supervision. A BMI >30 warrants a doctor consultation."],

    # Emergency
    'emergency': ["🚨 **Medical Emergency?** Call 102 (Ambulance) or 108 immediately. Stay calm, don't eat/drink, and follow dispatcher instructions until help arrives."],
    'ambulance': ["Call 102 or 108 for an ambulance in India. Describe your location and the emergency clearly."],

    # COVID
    'covid': ["😷 COVID-19: Isolate if symptoms appear, get tested, wear N95 mask in public. Get vaccinated and boosted. Seek care if oxygen drops below 94%."],
    'vaccination': ["Vaccines are safe and effective! Stay up to date with COVID, flu, and routine vaccines. Check with your doctor for age-appropriate vaccines."],

    # Generic
    'doctor': ["Always consult a qualified doctor for medical diagnosis and treatment. I can provide general guidance but not replace professional medical advice."],
    'medicine': ["Never self-medicate without a doctor's advice. Prescription medicines should only be taken as directed. Completing the full course of antibiotics is crucial."],
    'hospital': ["For hospital recommendations, check government hospitals in your area or ask your primary care physician for referrals to specialists."],
    'thank': ["You're welcome! 😊 Take good care of yourself. Remember — prevention is better than cure!"],
    'thanks': ["Happy to help! 🌿 Wishing you good health!"],
}

DEFAULT_RESPONSES = [
    "I'm not sure about that specific query. Could you rephrase or ask about a specific symptom, disease, or health topic? 🤔",
    "I don't have specific information on that. I'd recommend consulting a healthcare professional for personalized advice. 🏥",
    "That's outside my current knowledge base. Try asking about symptoms, diet, medications, or general health tips!",
    "For that specific question, please consult a qualified doctor. I can help with general health information and symptoms.",
]


def get_response(message: str) -> str:
    """
    Find the best keyword match in RESPONSES for the user's message.
    """
    message_lower = message.lower().strip()

    # Check for direct keyword matches (longest match first for specificity)
    matched_responses = []
    for keyword, responses in RESPONSES.items():
        if keyword in message_lower:
            matched_responses.append((len(keyword), responses))

    if matched_responses:
        # Use the most specific (longest) keyword match
        matched_responses.sort(key=lambda x: x[0], reverse=True)
        return random.choice(matched_responses[0][1])

    return random.choice(DEFAULT_RESPONSES)
