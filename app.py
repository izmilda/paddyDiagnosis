from flask import Flask, render_template, request

app = Flask(__name__)

# --- 1. KNOWLEDGE BASE (The Rules) ---
# Same logic as before, but in Python dictionaries
KNOWLEDGE_BASE = [
    {
        "id": "rice_blast",
        "name": "Rice Blast",
        "type": "Fungal Disease",
        "severity": "High",
        "symptoms": ["leaf_diamond_lesions", "leaf_gray_center", "panicle_neck_rot"],
        "management": "Use Tricyclazole. Maintain water level."
    },
    {
        "id": "bacterial_leaf_blight",
        "name": "Bacterial Leaf Blight",
        "type": "Bacterial Disease",
        "severity": "High",
        "symptoms": ["leaf_water_soaked_streaks", "leaf_yellow_margins", "leaf_ooze"],
        "management": "Drain field. Avoid Nitrogen. Use Copper fungicides."
    },
    {
        "id": "nitrogen_deficiency",
        "name": "Nitrogen Deficiency",
        "type": "Nutrient Deficiency",
        "severity": "Low",
        "symptoms": ["leaf_general_yellowing", "plant_stunted_growth"],
        "management": "Apply Urea. Use Leaf Color Chart."
    }
]

# --- 2. SYMPTOM CATALOG ---
SYMPTOMS = [
    {"id": "leaf_diamond_lesions", "label": "Diamond/Eye-shaped lesions"},
    {"id": "leaf_gray_center", "label": "Gray/White centers in spots"},
    {"id": "panicle_neck_rot", "label": "Rot at base of panicle"},
    {"id": "leaf_water_soaked_streaks", "label": "Water-soaked streaks"},
    {"id": "leaf_yellow_margins", "label": "Yellow wavy margins"},
    {"id": "leaf_ooze", "label": "Milky ooze droplets"},
    {"id": "leaf_general_yellowing", "label": "General yellowing (Chlorosis)"},
    {"id": "plant_stunted_growth", "label": "Stunted growth"}
]

# --- 3. ROUTES (Connecting to the Web) ---

@app.route('/', methods=['GET', 'POST'])
def home():
    diagnosis = None
    selected_symptoms = []

    if request.method == 'POST':
        # Get list of checked checkboxes from HTML
        selected_symptoms = request.form.getlist('symptoms')
        
        # --- INFERENCE ENGINE LOGIC ---
        scores = []
        for disease in KNOWLEDGE_BASE:
            # Find intersection (matches)
            matches = [s for s in disease['symptoms'] if s in selected_symptoms]
            match_count = len(matches)
            
            # Calculate Confidence %
            total_symptoms = len(disease['symptoms'])
            confidence = (match_count / total_symptoms) * 100 if total_symptoms > 0 else 0
            
            if confidence > 0:
                scores.append({
                    "name": disease['name'],
                    "type": disease['type'],
                    "severity": disease['severity'],
                    "management": disease['management'],
                    "confidence": round(confidence, 1)
                })
        
        # Sort by highest confidence
        scores.sort(key=lambda x: x['confidence'], reverse=True)
        diagnosis = scores

    # Render the HTML, passing the variables (symptoms list and results) to it
    return render_template('index.html', symptoms_list=SYMPTOMS, diagnosis=diagnosis)

if __name__ == '__main__':
    app.run(debug=True)