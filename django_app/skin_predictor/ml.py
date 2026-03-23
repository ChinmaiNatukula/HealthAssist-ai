"""
Skin Disease Prediction engine.
Uses image metadata and a deterministic mapping to return realistic results.
"""

import hashlib

SKIN_DISEASES = [
    {
        'name': 'Acne Vulgaris',
        'confidence_base': 85,
        'description': 'A common skin condition where hair follicles become plugged with oil and dead skin cells, causing pimples and blackheads.',
        'precautions': [
            'Wash face gently twice daily with a mild cleanser',
            'Avoid touching or popping pimples',
            'Use non-comedogenic (oil-free) skincare products',
            'Apply benzoyl peroxide or salicylic acid topically',
            'See a dermatologist for severe cases',
        ],
        'severity': 'mild',
        'icon': '🔴',
    },
    {
        'name': 'Eczema (Atopic Dermatitis)',
        'confidence_base': 78,
        'description': 'A condition that causes red, itchy, and inflamed patches of skin. Often related to allergens or immune dysfunction.',
        'precautions': [
            'Moisturize skin at least twice daily',
            'Avoid triggers like harsh soaps, pet dander, and certain fabrics',
            'Use fragrance-free, gentle skin products',
            'Apply prescribed corticosteroid creams during flare-ups',
            'Keep fingernails short to minimize damage from scratching',
        ],
        'severity': 'moderate',
        'icon': '🍊',
    },
    {
        'name': 'Psoriasis',
        'confidence_base': 72,
        'description': 'A chronic autoimmune condition causing rapid skin cell buildup, resulting in scaling, redness, and itchy patches.',
        'precautions': [
            'Keep skin moisturized to reduce scaling',
            'Avoid skin injuries, infections, and stress',
            'Get safe sun exposure (10–15 min/day) to slow cell growth',
            'Follow prescribed topical or systemic treatments',
            'Join a support group for coping strategies',
        ],
        'severity': 'moderate',
        'icon': '🧡',
    },
    {
        'name': 'Ringworm (Tinea Corporis)',
        'confidence_base': 88,
        'description': 'A fungal infection causing a circular, ring-shaped rash. Despite the name, it is not caused by a worm.',
        'precautions': [
            'Apply antifungal cream (clotrimazole/miconazole) twice daily',
            'Keep the infected area clean and dry',
            'Avoid sharing towels, clothing, or bedding',
            'Wash hands thoroughly after touching the affected area',
            'Complete the full course of treatment even if it looks healed',
        ],
        'severity': 'mild',
        'icon': '🟡',
    },
    {
        'name': 'Melanoma (Suspected)',
        'confidence_base': 65,
        'description': 'A serious form of skin cancer. Early detection is critical. Look for asymmetry, irregular borders, multiple colors in a mole.',
        'precautions': [
            '⚠️ SEEK IMMEDIATE DERMATOLOGIST REVIEW',
            'Avoid sun exposure without SPF 50+ sunscreen',
            'Do not use tanning beds',
            'Perform monthly self-skin examinations (ABCDE rule)',
            'Schedule a professional skin cancer screening urgently',
        ],
        'severity': 'critical',
        'icon': '⚫',
    },
    {
        'name': 'Vitiligo',
        'confidence_base': 80,
        'description': 'A condition causing loss of skin color in patches due to destruction of melanin-producing cells. Not contagious.',
        'precautions': [
            'Apply sunscreen SPF 30+ on depigmented areas daily',
            'Consider cosmetic camouflage creams for visible areas',
            'Consult a dermatologist for phototherapy or topical treatments',
            'Protect affected skin from sunburn',
            'Talk to a counselor if it affects your self-confidence',
        ],
        'severity': 'mild',
        'icon': '⬜',
    },
]


def predict_skin_disease(image_file):
    """
    Predict a skin disease from an uploaded image.
    Uses a deterministic hash of the file content for consistent demo results.
    Returns disease info with a confidence score.
    """
    # Read file and compute hash for deterministic results
    content = image_file.read()
    file_hash = hashlib.md5(content).hexdigest()
    index = int(file_hash[:8], 16) % len(SKIN_DISEASES)
    
    disease = SKIN_DISEASES[index]
    # Vary confidence slightly based on hash
    confidence_variation = (int(file_hash[8:10], 16) % 10) - 5  # -5 to +4
    confidence = min(97, max(60, disease['confidence_base'] + confidence_variation))
    
    # Also return second and third guesses
    second_index = (index + 1) % len(SKIN_DISEASES)
    third_index = (index + 2) % len(SKIN_DISEASES)
    
    return {
        'primary': {**disease, 'confidence': confidence},
        'alternatives': [
            {**SKIN_DISEASES[second_index], 'confidence': max(20, confidence - 25)},
            {**SKIN_DISEASES[third_index], 'confidence': max(10, confidence - 40)},
        ]
    }
