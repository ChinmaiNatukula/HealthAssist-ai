import re
from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint('chatbot', __name__)

# ─── Knowledge base ────────────────────────────────────────────────────────────
RESPONSES = [
    # Greetings
    (r'\b(hi|hello|hey|howdy|good morning|good afternoon|good evening)\b',
     "Hello! 👋 I'm HealthAssist AI, your virtual health companion. "
     "How can I help you today? You can ask me about symptoms, medications, diet, or general health advice."),

    # How are you
    (r'\bhow are you\b',
     "I'm doing great, thank you for asking! 😊 I'm here to assist you with any health-related questions. What's on your mind?"),

    # Fever
    (r'\b(fever|temperature|high temp)\b',
     "🌡️ **Fever** is usually a sign your body is fighting an infection.\n\n"
     "**What to do:**\n"
     "- Rest and stay hydrated (water, ORS, clear soups)\n"
     "- Take paracetamol (if not allergic) to lower temperature\n"
     "- Use a cool, damp cloth on the forehead\n\n"
     "⚠️ **See a doctor if:** fever exceeds 103°F (39.4°C), lasts more than 3 days, or is accompanied by stiff neck, rash, or confusion."),

    # Cold / runny nose
    (r'\b(cold|runny nose|sneezing|sore throat|cough)\b',
     "🤧 **Common Cold** symptoms include runny nose, sore throat, and sneezing.\n\n"
     "**Remedies:**\n"
     "- Rest well and drink warm fluids (ginger tea, honey-lemon water)\n"
     "- Steam inhalation to relieve congestion\n"
     "- Gargle with warm salt water for sore throat\n\n"
     "Colds usually resolve in 7–10 days. If symptoms worsen, consult a doctor."),

    # Headache
    (r'\b(headache|head pain|migraine)\b',
     "🧠 **Headaches** can have many causes — stress, dehydration, lack of sleep, or eye strain.\n\n"
     "**Quick relief:**\n"
     "- Drink a glass of water (dehydration is a top cause)\n"
     "- Rest in a quiet, dark room\n"
     "- Apply a cold or warm compress to your head/neck\n"
     "- Paracetamol or ibuprofen for pain relief\n\n"
     "⚠️ **Emergency:** sudden severe headache ('thunderclap'), headache with vision loss or numbness → call emergency services immediately."),

    # Chest pain
    (r'\b(chest pain|chest tightness|heart pain|palpitations)\b',
     "❗ **Chest pain** should never be ignored.\n\n"
     "It may be caused by muscle strain, acid reflux, or in serious cases — a cardiac event.\n\n"
     "⚠️ **Call emergency services immediately if:**\n"
     "- Pain spreads to the arm, jaw, or back\n"
     "- Accompanied by sweating, shortness of breath, or dizziness\n\n"
     "Please do NOT self-medicate for chest pain. Seek emergency care right away."),

    # Stomach / digestive
    (r'\b(stomach|nausea|vomiting|diarrhea|diarrhoea|indigestion|acidity|bloating|gas)\b',
     "🍽️ **Digestive symptoms** are very common. Here's what may help:\n\n"
     "- Nausea/vomiting: sip clear fluids slowly; avoid solid food until settled\n"
     "- Diarrhea: stay hydrated with ORS; avoid dairy and fried foods\n"
     "- Acidity: avoid spicy/acidic food; try antacids; eat smaller meals\n\n"
     "⚠️ **See a doctor if:** you see blood in vomit/stool, or symptoms persist more than 2 days."),

    # Diabetes
    (r'\b(diabetes|blood sugar|insulin|glucose)\b',
     "🩸 **Diabetes** is a chronic condition requiring ongoing management.\n\n"
     "**Key tips:**\n"
     "- Monitor blood sugar regularly\n"
     "- Follow a low-glycemic diet (avoid white bread, sugary drinks)\n"
     "- Exercise at least 30 minutes daily\n"
     "- Take medications as prescribed\n\n"
     "📌 Always consult your endocrinologist for personalized treatment adjustments."),

    # Blood pressure
    (r'\b(blood pressure|hypertension|bp high|bp low|hypotension)\b',
     "💓 **Blood Pressure** management is crucial for heart health.\n\n"
     "**For high BP:** Reduce salt, exercise regularly, manage stress, avoid smoking/alcohol.\n"
     "**For low BP:** Stay hydrated, eat small frequent meals, avoid prolonged standing.\n\n"
     "📌 Always monitor your BP at home and share readings with your doctor."),

    # Sleep
    (r'\b(sleep|insomnia|can.t sleep|not sleeping|tired)\b',
     "😴 **Sleep** is vital for overall health. For better sleep:\n\n"
     "- Maintain a consistent sleep schedule\n"
     "- Avoid screens 1 hour before bed\n"
     "- Keep your bedroom cool and quiet\n"
     "- Limit caffeine after 2 PM\n"
     "- Try deep breathing or meditation before bed\n\n"
     "If insomnia persists for weeks, consult a doctor."),

    # Mental health
    (r'\b(anxious|anxiety|stress|depressed|depression|mental health|panic)\b',
     "💙 **Mental health** matters just as much as physical health.\n\n"
     "**What can help:**\n"
     "- Talk to someone you trust\n"
     "- Practice mindfulness or yoga\n"
     "- Exercise — even a 20-min walk helps\n"
     "- Limit social media and news intake\n\n"
     "🤝 If you're feeling overwhelmed, please reach out to a licensed therapist or counselor. You are not alone."),

    # Diet / nutrition
    (r'\b(diet|nutrition|healthy eating|weight loss|obesity|overweight)\b',
     "🥗 **Healthy eating habits:**\n\n"
     "- Fill half your plate with fruits and vegetables\n"
     "- Choose whole grains over refined carbs\n"
     "- Limit processed foods, sugar, and saturated fats\n"
     "- Stay hydrated: aim for 8 glasses of water daily\n"
     "- For weight management, aim for a 500-cal daily deficit under professional guidance\n\n"
     "📌 Consult a registered dietitian for personalized meal plans."),

    # Exercise
    (r'\b(exercise|workout|fitness|gym|physical activity)\b',
     "🏃 **Regular exercise** offers tremendous health benefits!\n\n"
     "- Adults: aim for 150 min of moderate aerobic activity/week\n"
     "- Include strength training 2x/week\n"
     "- Even 10-min walks throughout the day add up\n"
     "- Warm up before and cool down after every session\n\n"
     "Start slow if you're a beginner and gradually increase intensity."),

    # Medication
    (r'\b(medication|medicine|drug|tablet|pill|dose|dosage)\b',
     "💊 **Medication guidance:**\n\n"
     "I can provide general information, but I'm not able to prescribe medications.\n\n"
     "⚠️ **Important reminders:**\n"
     "- Never self-medicate with prescription drugs\n"
     "- Always complete the full course of antibiotics\n"
     "- Store medicines as per label instructions\n"
     "- Keep medicines away from children\n\n"
     "📌 Always consult your doctor or pharmacist before starting any medication."),

    # Emergency
    (r'\b(emergency|911|ambulance|urgent|critical)\b',
     "🚨 **If this is a medical emergency, call your local emergency number immediately (911 / 112 / 108).**\n\n"
     "Do not delay seeking emergency care for:\n"
     "- Chest pain, difficulty breathing\n"
     "- Sudden weakness or paralysis\n"
     "- Severe bleeding\n"
     "- Loss of consciousness"),

    # Disclaimer / who are you
    (r'\b(who are you|what are you|about you|disclaimer)\b',
     "🤖 I'm **HealthAssist AI**, a virtual health assistant designed to provide general health information and guidance.\n\n"
     "⚠️ **Disclaimer:** I am not a licensed medical professional. My responses are for informational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns."),

    # Thanks
    (r'\b(thank|thanks|thank you|ty|thx)\b',
     "You're very welcome! 😊 Take care of yourself, and don't hesitate to ask if you have more health questions. Stay healthy! 💚"),

    # Goodbye
    (r'\b(bye|goodbye|see you|take care|farewell)\b',
     "Goodbye! 👋 Remember to stay hydrated, get enough rest, and take care of your health. See you next time! 💚"),
]

DEFAULT_RESPONSE = (
    "🤔 I'm not sure I understood that. Could you rephrase your health question?\n\n"
    "I can help with topics like:\n"
    "- Common symptoms (fever, headache, cold)\n"
    "- Chronic conditions (diabetes, hypertension)\n"
    "- Diet, sleep, mental health, and exercise\n"
    "- Medication reminders\n\n"
    "Or use the **Symptom Checker** on the left to identify possible conditions!"
)


def get_bot_response(message: str) -> str:
    msg = message.lower().strip()
    for pattern, response in RESPONSES:
        if re.search(pattern, msg):
            return response
    return DEFAULT_RESPONSE


chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    reply = get_bot_response(message)
    return jsonify({'reply': reply}), 200
