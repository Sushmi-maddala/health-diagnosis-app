from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def train_model():
    data = pd.read_csv("sample_data.csv")  # Load your dataset
    X = data["symptoms"]
    y = data["disease"]

    vectorizer = CountVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vec, y)

    return model, vectorizer

def predict_disease(symptom_input, model, vectorizer):
    input_vec = vectorizer.transform([symptom_input])
    prediction = model.predict(input_vec)[0]
    return prediction
