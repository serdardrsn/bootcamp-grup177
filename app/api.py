from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import os
from joblib import load

app = FastAPI()

# Model yolları
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "models", "final_rf_pipeline.joblib"))
ENCODER_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "models", "final_label_encoder.joblib"))

# Model ve encoder yükleniyor
model = load(MODEL_PATH)
label_encoder = load(ENCODER_PATH)

# Giriş veri modeli
class PatientData(BaseModel):
    chief_complaint: str
    age: int
    sbp: float
    dbp: float
    hr: float
    rr: float
    bt: float
    mental: str
    sex: str
    arrival_mode: str
    injury: str
    pain: int

# Kural tabanlı kırmızı sınıf tanımı
def is_critical_case(data: PatientData) -> bool:
    return (
        data.sbp < 90 or
        data.hr > 130 or
        data.rr > 30 or
        data.bt > 39.0 or
        data.pain >= 9
    )

# Tahmin endpoint'i
@app.post("/predict")
def predict(data: PatientData):
    # Eğer hasta kritikse doğrudan "Kırmızı"
    if is_critical_case(data):
        final_label = "Kırmızı"
    else:
        # Model için gerekli tüm girişleri hazırla
        default_values = {
            "Group": "Adult",
            "Patients number per hour": 10.0,
            "NRS_pain": data.pain,
            "Saturation": 98.0,
            "KTAS_RN": "Unknown",
            "Diagnosis in ED": "Unknown",
            "Disposition": "Unknown"
        }

        # Tüm özellik sözlüğü
        input_dict = {
            "Chief_complain": data.chief_complaint,
            "Age": data.age,
            "SBP": data.sbp,
            "DBP": data.dbp,
            "HR": data.hr,
            "RR": data.rr,
            "BT": data.bt,
            "Mental": data.mental,
            "Sex": data.sex,
            "Arrival mode": data.arrival_mode,
            "Injury": data.injury,
            "Pain": str(data.pain),  # model eğitiminde string ise
            **default_values
        }

        # Modelin beklediği sıraya göre özellikleri hazırla
        model_columns = model.feature_names_in_
        ordered_data = {col: input_dict.get(col, 0) for col in model_columns}
        df = pd.DataFrame([ordered_data])

        # Model tahmini
        prediction = model.predict(df)
        final_label = label_encoder.inverse_transform(prediction)[0]

    return {
        "final_prediction": final_label,
        "chief_complaint": data.chief_complaint
    }
