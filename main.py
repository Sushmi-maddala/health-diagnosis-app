from ml_model import train_model, predict_disease
from database import init_db  # Connects to your database setup

# Run this once to create the database and tables
init_db()

print("✅ Database is ready!")
import sqlite3  # Add this at the top if not already there

print("\n🧑‍⚕️ Welcome to the Health Diagnosis App!\nPlease enter your details:")

# Step 1: Take user input
name = input("Name: ")
age = int(input("Age: "))
weight = float(input("Weight (kg): "))
allergies = input("Any allergies? (or type 'None'): ")

# Step 2: Save user info to database
conn = sqlite3.connect("health_app.db")
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO users (name, age, weight, allergies)
    VALUES (?, ?, ?, ?)
""", (name, age, weight, allergies))

conn.commit()
conn.close()

print("\n✅ Your information has been saved successfully!")
# Train the ML model using your dataset
model, vectorizer = train_model()

# Ask user for symptoms
symptoms = input("\nEnter your symptoms (space-separated): ")

# Predict the disease
diagnosis = predict_disease(symptoms, model, vectorizer)
print(f"\n🩺 Based on your symptoms, the predicted disease is: {diagnosis}")

# Basic diet recommendations (you can customize these later)
diet_plan = ""
if diagnosis == "diabetes":
    diet_plan = "Low sugar diet with whole grains, lean proteins, and fiber-rich vegetables."
elif diagnosis == "flu":
    diet_plan = "Warm fluids, vitamin C-rich fruits, and lots of rest."
elif diagnosis == "migraine":
    diet_plan = "Hydration, magnesium-rich foods, and avoid processed snacks."
else:
    diet_plan = "Balanced meals with hydration and nutrient-dense options."

print(f"\n🍱 Recommended Diet Plan: {diet_plan}")
# Save diagnosis and diet plan into the records table
conn = sqlite3.connect("health_app.db")
cursor = conn.cursor()

# Get the latest user_id (who just entered their info)
cursor.execute("SELECT MAX(user_id) FROM users")
user_id = cursor.fetchone()[0]

cursor.execute("""
    INSERT INTO records (user_id, symptom_list, diagnosis, diet_plan)
    VALUES (?, ?, ?, ?)
""", (user_id, symptoms, diagnosis, diet_plan))

conn.commit()
conn.close()

print("\n✅ Diagnosis and diet plan saved successfully!")
input("\nPress Enter to close...")

