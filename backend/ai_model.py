import random
import joblib
import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


MODEL_FILE = "fraud_model.joblib"
ENCODER_FILE = "label_encoder.joblib"


# -------------------------------------------------
# CREATE TRAINING DATA
# -------------------------------------------------

def generate_training_data():

    X = []
    y = []

    diagnoses = [
        "Dengue fever",
        "Fever",
        "Fracture",
        "Heart disease",
        "Cancer",
        "Diabetes",
        "Malaria",
        "Infection"
    ]

    for _ in range(2000):

        claim_amount = random.randint(5000, 1000000)
        diagnosis = random.choice(diagnoses)

        # Create synthetic fraud patterns
        fraud = 0

        # Very high claim amount
        if claim_amount > 500000:
            fraud = 1

        # Random suspicious claims
        if random.random() < 0.10:
            fraud = 1

        # Normal claims
        if claim_amount < 100000 and random.random() < 0.85:
            fraud = 0

        diagnosis_code = diagnoses.index(diagnosis)

        X.append([
            claim_amount,
            diagnosis_code
        ])

        y.append(fraud)

    return X, y


# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------

def train_model():

    X, y = generate_training_data()

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_FILE)

    print("Fraud detection model trained successfully")


# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------

if not os.path.exists(MODEL_FILE):
    train_model()

model = joblib.load(MODEL_FILE)


# -------------------------------------------------
# CLAIM ANALYSIS
# -------------------------------------------------

def analyze_claim(claim_amount, diagnosis):

    diagnoses = [
        "Dengue fever",
        "Fever",
        "Fracture",
        "Heart disease",
        "Cancer",
        "Diabetes",
        "Malaria",
        "Infection"
    ]

    if diagnosis in diagnoses:
        diagnosis_code = diagnoses.index(diagnosis)
    else:
        diagnosis_code = 0

    prediction_data = [[
        claim_amount,
        diagnosis_code
    ]]

    prediction = model.predict(prediction_data)[0]

    probabilities = model.predict_proba(prediction_data)[0]

    fraud_probability = probabilities[1]

    risk_score = round(fraud_probability * 100, 2)

    if risk_score >= 70:
        risk_level = "HIGH"
        decision = "REVIEW"

    elif risk_score >= 40:
        risk_level = "MEDIUM"
        decision = "REVIEW"

    else:
        risk_level = "LOW"
        decision = "APPROVE"

    return {
        "fraud_risk_score": risk_score,
        "fraud_risk_level": risk_level,
        "decision": decision
    }