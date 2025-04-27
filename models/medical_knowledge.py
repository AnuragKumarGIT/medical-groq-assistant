# Common medical disclaimers to be appended to responses
medical_disclaimers = [
    "DISCLAIMER: This information is for educational purposes only and is not a substitute for professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment of any medical condition.",
    
    "IMPORTANT: This is not a medical diagnosis. Please consult with a healthcare professional for proper evaluation and treatment.",
    
    "NOTE: The information provided here is general in nature. Your specific situation may require different approaches. Always consult with your doctor.",
    
    "MEDICAL NOTICE: In case of emergency, call your local emergency services immediately rather than waiting for online advice."
]

# Common symptom categories and associated information
symptom_categories = {
    "respiratory": [
        "cough", "shortness of breath", "wheezing", "chest pain", "congestion"
    ],
    "digestive": [
        "nausea", "vomiting", "diarrhea", "constipation", "abdominal pain", "bloating"
    ],
    "neurological": [
        "headache", "dizziness", "confusion", "fainting", "seizure", "memory issues"
    ],
    "musculoskeletal": [
        "joint pain", "muscle pain", "stiffness", "swelling", "back pain", "weakness"
    ],
    "dermatological": [
        "rash", "itching", "hives", "redness", "swelling", "sores", "bumps"
    ],
    "cardiovascular": [
        "chest pain", "palpitations", "shortness of breath", "swelling", "fatigue"
    ]
}

# Emergency symptoms that require immediate medical attention
emergency_indicators = [
    "severe chest pain",
    "difficulty breathing",
    "sudden numbness or weakness",
    "sudden severe headache",
    "uncontrolled bleeding",
    "severe abdominal pain",
    "seizure",
    "loss of consciousness",
    "suicidal thoughts",
    "severe allergic reaction",
    "poisoning",
    "head injury",
    "severe burn",
    "stroke symptoms",
    "heart attack symptoms"
]

# Function to check if a user's message contains emergency indicators
def check_for_emergency(message):
    """
    Check if the user's message contains any emergency indicators
    
    Args:
        message: User's text message
        
    Returns:
        is_emergency: Boolean indicating if emergency indicators were found
        matched_terms: List of emergency terms found in the message
    """
    message = message.lower()
    matched_terms = []
    
    for indicator in emergency_indicators:
        if indicator in message:
            matched_terms.append(indicator)
    
    return len(matched_terms) > 0, matched_terms

# Standard emergency response
emergency_response = """
URGENT: The symptoms you've described may require immediate medical attention. 

Please:
1. Call emergency services (911 in the US) or have someone take you to the nearest emergency room
2. Do not wait for symptoms to improve on their own
3. Do not use this platform for emergencies - seek immediate in-person medical care

Your health and safety are the top priority.
"""