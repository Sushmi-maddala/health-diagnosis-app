from flask import Flask, render_template, request
from ml_model import train_model, predict_disease
import sqlite3

app = Flask(__name__)
model, vectorizer = train_model()

# 🥗 Nutrition suggestions by symptom
food_suggestions = {
    "headache": ["almonds", "spinach", "water", "banana", "magnesium-rich foods"],
    "nausea": ["ginger tea", "plain toast", "banana", "crackers", "apple juice"],
    "fever": ["chicken soup", "coconut water", "broth", "oatmeal", "boiled vegetables"],
    "fatigue": ["dates", "eggs", "whole grains", "yogurt", "nuts"],
    "sore throat": ["warm tea", "honey", "soft boiled eggs", "soup", "mashed potatoes"],
    "diarrhea": ["rice", "applesauce", "banana", "toast", "boiled carrots"],
    "constipation": ["oatmeal", "prunes", "flaxseed", "papaya", "spinach"],
    "body aches": ["turmeric milk", "green leafy vegetables", "salmon", "beans", "sweet potatoes"],
    "vomiting": ["ginger", "coconut water", "plain crackers", "apple juice", "rice porridge"],
    "cold": ["garlic", "hot tea", "chicken soup", "citrus fruits", "ginger"],
    "shortness of breath": ["beetroot", "pomegranate", "spinach", "walnuts", "dark chocolate"],
    "dizziness": ["water", "electrolyte drinks", "banana", "dry toast", "orange juice"],
    "indigestion": ["mint tea", "fennel seeds", "yogurt", "banana", "boiled rice"],
    "bloating": ["peppermint tea", "ginger", "cucumber", "papaya", "pineapple"],
    "high blood pressure": ["beetroot", "oats", "dark chocolate", "garlic", "low-fat yogurt"],
    "low blood pressure": ["salted nuts", "coffee", "cheese", "olives", "water"],
    "anemia": ["spinach", "red meat", "lentils", "dates", "pumpkin seeds"],
    "acid reflux": ["oatmeal", "banana", "ginger", "green beans", "grilled chicken"],
    "dehydration": ["coconut water", "watermelon", "cucumber", "oranges", "broth"],
    "menstrual cramps": ["dark chocolate", "banana", "leafy greens", "chamomile tea", "flaxseeds"],
    "insomnia": ["warm milk", "chamomile tea", "almonds", "kiwi", "oats"],
    "stress": ["dark chocolate", "berries", "green tea", "avocado", "nuts"],
    "weakness": ["banana", "dates", "eggs", "sweet potatoes", "protein shake"],
    "dry skin": ["avocado", "walnuts", "olive oil", "cucumber", "sunflower seeds"],
    "joint pain": ["turmeric", "omega-3 rich fish", "berries", "broccoli", "green tea"],
    "eye strain": ["carrots", "sweet potatoes", "spinach", "eggs", "blueberries"],
    "muscle cramps": ["banana", "potassium-rich foods", "coconut water", "spinach", "yogurt"],
    "poor digestion": ["ginger", "papaya", "mint", "fennel", "yogurt"],
    "low immunity": ["citrus fruits", "garlic", "spinach", "yogurt", "almonds"],
    "heatstroke": ["coconut water", "watermelon", "cucumber", "lemonade", "mint"],
    "acidic stomach": ["banana", "cold milk", "oatmeal", "boiled rice", "non-citrus fruits"],
    "heartburn": ["ginger", "low-fat yogurt", "oatmeal", "aloe vera juice", "green beans"],
    "itchiness": ["cucumber", "mint", "turmeric", "sunflower seeds", "water"],
    "bruising": ["pineapple", "citrus fruits", "spinach", "red bell peppers", "broccoli"],
    "weight loss": ["sweet potatoes", "eggs", "avocado", "nuts", "milk"],
    "weight gain": ["peanut butter", "whole grains", "red meat", "cheese", "smoothies"],
    "stomach pain": ["boiled rice", "banana", "ginger", "mint tea", "applesauce"],
    "gastric": ["fennel seeds", "ginger", "mint", "cucumber", "yogurt"],
    "body pains": ["turmeric milk", "spinach", "almonds", "sweet potatoes", "green tea"]
}

def suggest_foods(symptom_text):
    symptoms = symptom_text.lower().split()
    foods = set()
    for s in symptoms:
        if s in food_suggestions:
            foods.update(food_suggestions[s])
    return list(foods) if foods else ["No specific food suggestions found."]

@app.route("/", methods=["GET", "POST"])
def index():
    diagnosis = ""
    diet_plan = ""
    food_list = []

    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])
        weight = float(request.form["weight"])
        allergies = request.form["allergies"]
        symptoms = request.form["symptoms"]

        diagnosis = predict_disease(symptoms, model, vectorizer)
        food_list = suggest_foods(symptoms)

        # Simple diet logic
        if diagnosis == "diabetes":
            diet_plan = "Low sugar diet with whole grains, lean proteins, and fiber-rich vegetables."
        elif diagnosis == "flu":
            diet_plan = "Warm fluids, vitamin C-rich fruits, and plenty of rest."
        elif diagnosis == "migraine":
            diet_plan = "Hydration, magnesium-rich foods, and low stress environment."
        else:
            diet_plan = "Balanced meals with hydration and nutrient-dense options."

        # Save to DB
        conn = sqlite3.connect("health_app.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age, weight, allergies) VALUES (?, ?, ?, ?)",
                       (name, age, weight, allergies))
        conn.commit()
        cursor.execute("SELECT MAX(user_id) FROM users")
        user_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO records (user_id, symptom_list, diagnosis, diet_plan) VALUES (?, ?, ?, ?)",
                       (user_id, symptoms, diagnosis, diet_plan))
        conn.commit()
        conn.close()

        return render_template("index.html", diagnosis=diagnosis, diet_plan=diet_plan, foods=food_list)

    return render_template("index.html", diagnosis=diagnosis)
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)