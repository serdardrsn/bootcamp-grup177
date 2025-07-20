from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
from joblib import load
import os

# FastAPI app
app = FastAPI()

# Dinamik model yolu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "new_model.joblib")
MODEL_PATH = os.path.normpath(MODEL_PATH)
model = load(MODEL_PATH)

# KTAS etiketleri (5 seviye)
ktas_labels = {
    1: "Kırmızı",
    2: "Turuncu",
    3: "Sarı",
    4: "Yeşil",
    5: "Mavi"
}

# Hasta verisi için şema
class PatientData(BaseModel):
    chief_complaint: str
    age: int
    sbp: int
    dbp: int
    hr: int
    rr: int
    bt: float
    mental: str
    sex: str
    arrival_mode: str
    injury: str
    pain: int

# risk_score hesaplama
def calculate_risk_score(sbp, hr, rr, bt, pain):
    score = 0
    if sbp < 90: score += 2
    if hr > 100: score += 1
    if rr > 30: score += 1
    if bt > 38: score += 1
    if pain >= 8: score += 2
    return score

# Feature hazırlama
def prepare_features(data: PatientData):
    numeric = {
        "Age": data.age,
        "SBP": data.sbp,
        "DBP": data.dbp,
        "HR": data.hr,
        "RR": data.rr,
        "BT": data.bt,
        "Pain": data.pain,
        "risk_score": calculate_risk_score(data.sbp, data.hr, data.rr, data.bt, data.pain)
    }

    categories = {
        "Sex_Female": 1 if data.sex.lower() == "female" else 0,
        "Sex_Male": 1 if data.sex.lower() == "male" else 0,
        "Arrival mode_Ambulance": 1 if "ambulance" in data.arrival_mode.lower() else 0,
        "Arrival mode_Walk-in": 1 if "walk" in data.arrival_mode.lower() else 0,
        "Injury_No": 1 if data.injury.lower() == "no" else 0,
        "Injury_Yes": 1 if data.injury.lower() == "yes" else 0,
        "Mental_Alert": 1 if data.mental.lower() in ["uyanık", "alert"] else 0,
        "Mental_Other": 1 if data.mental.lower() not in ["uyanık", "alert"] else 0
    }

    all_features = {**numeric, **categories}

    feature_order = [
        "Age", "SBP", "DBP", "HR", "RR", "BT", "Pain", "risk_score",
        "Sex_Female", "Sex_Male",
        "Arrival mode_Ambulance", "Arrival mode_Walk-in",
        "Injury_No", "Injury_Yes",
        "Mental_Alert", "Mental_Other",
        # Eksik kolonlar için placeholder
        "missing_feature_1", "missing_feature_2", "missing_feature_3",
        "missing_feature_4", "missing_feature_5", "missing_feature_6", "missing_feature_7"
    ]

    for f in feature_order:
        if f not in all_features:
            all_features[f] = 0

    return np.array([[all_features[f] for f in feature_order]])

# Rule-based KTAS
def ktas_risk_ve_sebep(data: PatientData):
    risk_sebepleri = []

    if data.bt > 38:
        risk_sebepleri.append("Yüksek ateş (>38°C)")
    if data.hr > 100:
        risk_sebepleri.append("Yüksek nabız (>100 bpm)")
    if data.age > 70:
        risk_sebepleri.append("Yaşın 70'in üzerinde olması")
    if data.sbp < 90:
        risk_sebepleri.append("Düşük sistolik kan basıncı (<90 mmHg)")
    if data.dbp < 60:
        risk_sebepleri.append("Düşük diyastolik kan basıncı (<60 mmHg)")
    if data.rr > 30:
        risk_sebepleri.append("Aşırı hızlı solunum (>30/dk)")
    if data.mental.lower() != "uyanık":
        risk_sebepleri.append("Bilinç durumunun uyanık olmaması")
    if data.pain >= 8:
        risk_sebepleri.append("Şiddetli ağrı (8 ve üzeri)")

    if risk_sebepleri:
        return "Kırmızı", "Aşağıdaki sebepler nedeniyle yüksek risk:\n- " + "\n- ".join(risk_sebepleri)

    orta_risk_sebepleri = []
    if 5 <= data.pain < 8:
        orta_risk_sebepleri.append("Orta şiddette ağrı (5-7 arası)")
    if 90 <= data.sbp < 100:
        orta_risk_sebepleri.append("Sistolik kan basıncı sınırda düşük (90-99 mmHg)")
    if 60 <= data.dbp < 70:
        orta_risk_sebepleri.append("Diyastolik basınç sınırda düşük (60-69 mmHg)")
    if 21 <= data.rr <= 30:
        orta_risk_sebepleri.append("Solunum sayısının yüksek olması (21-30/dk)")
    if 37.5 <= data.bt <= 38:
        orta_risk_sebepleri.append("Hafif ateş (37.5-38°C)")

    if orta_risk_sebepleri:
        return "Sarı", "Aşağıdaki sebepler nedeniyle orta risk:\n- " + "\n- ".join(orta_risk_sebepleri)

    return "Yeşil", "Hayati bulgular normal ve ağrı düşük, düşük risk."

# Tahmin endpoint
@app.post("/predict")
def predict(data: PatientData):
    rule_prediction, rule_reason = ktas_risk_ve_sebep(data)

    features = prepare_features(data)
    model_pred = model.predict(features)[0]
    model_prob = round(np.max(model.predict_proba(features)), 2)

    # Burada int() dönüşümü var!
    model_label = ktas_labels.get(int(model_pred), str(model_pred))

    return {
        "model_prediction": model_label,
        "model_probability": model_prob,
        "rule_based_prediction": rule_prediction,
        "rule_based_reason": rule_reason,
        "chief_complaint": data.chief_complaint
    }
