import os
import io
import json
import base64
import numpy as np
from flask import Blueprint, request, jsonify

image_predict_bp = Blueprint('image_predict', __name__)

# Pillow is a standard dependency
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ─── Skin disease knowledge base ─────────────────────────────────────────────
SKIN_CONDITIONS = {
    "Melanoma": {
        "description": "A type of skin cancer that develops in melanocytes (pigment-producing cells). Early detection is critical.",
        "visual_clues": ["Dark irregular patches", "Asymmetrical mole", "Multiple colors (black, brown, red)"],
        "causes": ["UV radiation exposure", "Genetics / family history", "Multiple moles", "Fair skin"],
        "precautions": ["Use SPF 30+ sunscreen daily", "Avoid tanning beds", "Wear protective clothing", "Regular skin checks"],
        "basic_treatment": ["Surgical excision", "Immunotherapy", "Targeted therapy", "Radiation therapy"],
        "when_to_see_doctor": "IMMEDIATELY — suspected melanoma is a medical emergency. See a dermatologist or oncologist without delay."
    },
    "Acne Vulgaris": {
        "description": "A common skin condition where hair follicles become plugged with oil and dead skin cells, causing pimples, blackheads, and cysts.",
        "visual_clues": ["Red or pink pimples", "Whiteheads / blackheads", "Oily skin", "Inflammatory papules"],
        "causes": ["Excess sebum production", "Bacteria (C. acnes)", "Hormonal changes", "Stress", "Diet"],
        "precautions": ["Cleanse face twice daily", "Avoid touching face", "Use non-comedogenic products", "Change pillowcases weekly"],
        "basic_treatment": ["Benzoyl peroxide", "Salicylic acid", "Topical retinoids", "Antibiotics (severe cases)"],
        "when_to_see_doctor": "If acne is severe, cystic, or causes scarring — see a dermatologist for prescription treatment."
    },
    "Eczema (Atopic Dermatitis)": {
        "description": "A chronic inflammatory skin condition causing dry, itchy, and inflamed skin. Often flares periodically.",
        "visual_clues": ["Red or brownish-gray patches", "Dry, scaly skin", "Itchy lesions", "Small raised bumps"],
        "causes": ["Genetic predisposition", "Immune system dysfunction", "Environmental triggers", "Dry skin"],
        "precautions": ["Moisturize twice daily", "Avoid harsh soaps and detergents", "Identify and avoid triggers", "Wear soft, cotton clothing"],
        "basic_treatment": ["Topical corticosteroids", "Moisturizers / emollients", "Antihistamines for itch", "Immunosuppressants (severe)"],
        "when_to_see_doctor": "If eczema covers large areas, is infected, doesn't respond to OTC treatments, or severely impacts quality of life."
    },
    "Psoriasis": {
        "description": "A chronic autoimmune condition causing rapid skin cell buildup, resulting in scales and red, itchy patches.",
        "visual_clues": ["Red patches with silvery scales", "Dry, cracked skin", "Thickened nails", "Burning sensation"],
        "causes": ["Autoimmune dysfunction", "Genetics", "Stress", "Infections", "Medications"],
        "precautions": ["Keep skin moisturized", "Avoid stress", "Quit smoking", "Limit alcohol", "Gentle skin care routine"],
        "basic_treatment": ["Topical corticosteroids", "Vitamin D analogues", "Phototherapy", "Biologics (severe cases)"],
        "when_to_see_doctor": "If psoriasis covers more than 10% of body, affects joints, or isn't responding to treatment."
    },
    "Ringworm (Tinea Corporis)": {
        "description": "A fungal infection of the skin that causes a ring-shaped, scaly rash. Highly contagious.",
        "visual_clues": ["Circular, ring-shaped rash", "Red scaly borders", "Clear center", "Itchy"],
        "causes": ["Dermatophyte fungi", "Contact with infected persons/animals", "Warm, moist environments"],
        "precautions": ["Don't share personal items", "Keep skin dry", "Wash hands after touching animals", "Wear breathable clothing"],
        "basic_treatment": ["Topical antifungal creams (clotrimazole, miconazole)", "Oral antifungals if severe", "Keep area clean and dry"],
        "when_to_see_doctor": "If infection spreads rapidly, appears on scalp/nails, or doesn't respond to OTC antifungals after 4 weeks."
    },
    "Hives (Urticaria)": {
        "description": "Raised, itchy welts on the skin that appear suddenly, often as an allergic reaction.",
        "visual_clues": ["Raised, red or skin-colored welts", "Itchy, burning, or stinging", "Swelling", "Welts that change shape/size"],
        "causes": ["Allergic reactions (foods, medications, insect stings)", "Infections", "Stress", "Temperature extremes"],
        "precautions": ["Identify and avoid triggers", "Wear loose clothing", "Avoid hot showers", "Keep an antihistamine handy"],
        "basic_treatment": ["Antihistamines (cetirizine, loratadine)", "Cool compresses", "Corticosteroids for severe cases"],
        "when_to_see_doctor": "If hives are accompanied by throat swelling, difficulty breathing, or dizziness — call emergency services immediately (anaphylaxis)."
    },
    "Rosacea": {
        "description": "A chronic skin condition characterizing facial redness, visible blood vessels, and sometimes acne-like bumps.",
        "visual_clues": ["Persistent facial redness", "Visible blood vessels", "Swollen red bumps", "Eye irritation"],
        "causes": ["Vascular abnormalities", "Immune response", "H. pylori bacteria", "Genetics", "Sun exposure"],
        "precautions": ["Use sunscreen daily", "Avoid triggers (spicy food, alcohol, extremes of temperature)", "Use gentle skin care products"],
        "basic_treatment": ["Topical metronidazole or azelaic acid", "Oral antibiotics", "Laser therapy for blood vessels"],
        "when_to_see_doctor": "See a dermatologist for proper diagnosis and to prevent worsening of symptoms."
    },
    "Contact Dermatitis": {
        "description": "Inflammation caused by direct contact with a substance that irritates the skin or triggers an allergic reaction.",
        "visual_clues": ["Red, itchy rash", "Dry, cracked skin", "Blisters", "Burning sensation", "Swelling"],
        "causes": ["Allergens (nickel, latex, fragrances)", "Irritants (soaps, cleaning products)", "Plants (poison ivy)"],
        "precautions": ["Identify and avoid the trigger substance", "Use gloves when handling chemicals", "Choose fragrance-free products"],
        "basic_treatment": ["Remove the irritant immediately", "Cool compresses", "Hydrocortisone cream", "Antihistamines"],
        "when_to_see_doctor": "If rash covers large areas, involves the face/genitals, or doesn't improve within a few weeks."
    },
}

CONDITION_NAMES = list(SKIN_CONDITIONS.keys())

def extract_image_features(img: "Image.Image") -> dict:
    """Extract color and texture features from a PIL image."""
    img_rgb = img.convert('RGB').resize((128, 128))
    arr = np.array(img_rgb, dtype=np.float32) / 255.0

    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    features = {
        'mean_r': float(np.mean(r)),
        'mean_g': float(np.mean(g)),
        'mean_b': float(np.mean(b)),
        'std_r': float(np.std(r)),
        'std_g': float(np.std(g)),
        'std_b': float(np.std(b)),
        'redness': float(np.mean(r) - (np.mean(g) + np.mean(b)) / 2),  # redness index
        'darkness': float(1.0 - np.mean(arr)),
        'contrast': float(np.std(arr)),
        'saturation': float(np.mean(np.max(arr, axis=2) - np.min(arr, axis=2))),
        # Red pixel density (inflamed skin indicator)
        'red_density': float(np.mean((r > 0.55) & (r > g * 1.2) & (r > b * 1.2))),
        # Dark patch indicator
        'dark_density': float(np.mean(np.mean(arr, axis=2) < 0.3)),
        # Brightness variance (texture)
        'brightness_var': float(np.var(np.mean(arr, axis=2))),
        # Color diversity
        'color_range': float(np.mean(np.max(arr, axis=2) - np.min(arr, axis=2))),
    }
    return features


def score_conditions(features: dict) -> list:
    """
    Heuristic scoring of skin conditions based on image color/texture features.
    Returns list of (condition_name, score) sorted descending.
    """
    r = features['mean_r']
    g = features['mean_g']
    b = features['mean_b']
    redness = features['redness']
    darkness = features['darkness']
    red_density = features['red_density']
    dark_density = features['dark_density']
    saturation = features['saturation']
    contrast = features['contrast']
    brightness_var = features['brightness_var']

    scores = {}

    # Melanoma: dark, irregular, varying colors
    scores['Melanoma'] = (
        dark_density * 3.0
        + darkness * 2.0
        + brightness_var * 5.0
        + saturation * 1.5
        + (1 - features['std_r']) * 0.5  # irregular coloring
    )

    # Acne Vulgaris: reddish spots on lighter background
    scores['Acne Vulgaris'] = (
        red_density * 4.0
        + redness * 3.0
        + (r - 0.5) * 2.0 if r > 0.5 else 0
        + contrast * 1.0
    )
    if scores['Acne Vulgaris'] < 0: scores['Acne Vulgaris'] = 0

    # Eczema: red + dry/scaly = high contrast + reddish tones
    scores['Eczema (Atopic Dermatitis)'] = (
        red_density * 2.5
        + contrast * 3.5
        + brightness_var * 2.0
        + redness * 2.0
    )

    # Psoriasis: silvery-red, high saturation, thick patches
    scores['Psoriasis'] = (
        saturation * 3.0
        + red_density * 2.0
        + brightness_var * 1.5
        + (r + g - b * 2) * 1.0 if (r + g - b * 2) > 0 else 0
    )
    if scores['Psoriasis'] < 0: scores['Psoriasis'] = 0

    # Ringworm: circular pattern, mild redness
    scores['Ringworm (Tinea Corporis)'] = (
        redness * 2.0
        + saturation * 2.0
        + (1 - dark_density) * 1.5
        + red_density * 1.5
    )

    # Hives: raised red welts, high redness
    scores['Hives (Urticaria)'] = (
        red_density * 3.5
        + redness * 3.0
        + (1 - darkness) * 1.5
    )

    # Rosacea: diffuse facial redness
    scores['Rosacea'] = (
        redness * 4.0
        + red_density * 2.5
        + (1 - contrast) * 1.5
        + (1 - dark_density) * 1.0
    )

    # Contact Dermatitis: redness + contrast (acute inflammation)
    scores['Contact Dermatitis'] = (
        redness * 3.0
        + red_density * 2.0
        + contrast * 2.5
    )

    # Add feature-based noise to avoid ties
    np.random.seed(int(sum(features.values()) * 1000) % 10000)
    for k in scores:
        scores[k] += np.random.uniform(0.01, 0.15)

    # Normalise to probabilities
    total = sum(max(v, 0.01) for v in scores.values())
    probs = {k: max(v, 0.01) / total for k, v in scores.items()}

    sorted_conditions = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    return sorted_conditions


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}


@image_predict_bp.route('', methods=['POST'])
def predict_from_image():
    if not PIL_AVAILABLE:
        return jsonify({'error': 'Pillow library not installed. Run: pip install Pillow'}), 503

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload JPG, PNG, or GIF.'}), 400

    try:
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        # Get image thumbnail (base64) for response
        thumb = img.copy()
        thumb.thumbnail((200, 200))
        buf = io.BytesIO()
        thumb.save(buf, format='JPEG', quality=85)
        thumb_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        features = extract_image_features(img)
        sorted_conditions = score_conditions(features)

        # Top 3 predictions
        top3 = sorted_conditions[:3]
        total_top3 = sum(s for _, s in top3)
        results = []
        for name, score in top3:
            pct = round((score / total_top3) * 100, 1)
            info = SKIN_CONDITIONS.get(name, {})
            results.append({
                'condition': name,
                'probability': pct,
                'description': info.get('description', ''),
                'visual_clues': info.get('visual_clues', []),
                'causes': info.get('causes', []),
                'precautions': info.get('precautions', []),
                'basic_treatment': info.get('basic_treatment', []),
                'when_to_see_doctor': info.get('when_to_see_doctor', ''),
            })

        return jsonify({
            'predictions': results,
            'thumbnail': f'data:image/jpeg;base64,{thumb_b64}',
            'image_size': list(img.size),
            'features_summary': {
                'redness_level': 'High' if features['red_density'] > 0.2 else ('Moderate' if features['red_density'] > 0.08 else 'Low'),
                'darkness_level': 'High' if features['dark_density'] > 0.3 else ('Moderate' if features['dark_density'] > 0.1 else 'Low'),
                'contrast': 'High' if features['contrast'] > 0.2 else ('Moderate' if features['contrast'] > 0.1 else 'Low'),
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500
