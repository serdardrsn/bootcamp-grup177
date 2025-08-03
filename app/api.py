from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import os
from joblib import load
from datetime import datetime

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

# Tahminleri loglamak için
def log_prediction(chief_complaint, age, result):
    log_dir = os.path.normpath(os.path.join(BASE_DIR, "..", "logs"))
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "prediction_log.csv")

    log_entry = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "chief_complaint": chief_complaint,
        "age": age,
        "result": result
    }])

    if os.path.exists(log_path):
        log_entry.to_csv(log_path, mode='a', header=False, index=False)
    else:
        log_entry.to_csv(log_path, mode='w', header=True, index=False)

# Tahmin endpoint'i
@app.post("/predict")
def predict(data: PatientData):
    if is_critical_case(data):
        final_label = "Kırmızı"
    else:
        default_values = {
            "Group": "Adult",
            "Patients number per hour": 10.0,
            "NRS_pain": data.pain,
            "Saturation": 98.0,
            "KTAS_RN": "Unknown",
            "Diagnosis in ED": "Unknown",
            "Disposition": "Unknown"
        }

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
            "Pain": str(data.pain),
            **default_values
        }

        model_columns = model.feature_names_in_
        ordered_data = {col: input_dict.get(col, 0) for col in model_columns}
        df = pd.DataFrame([ordered_data])

        prediction = model.predict(df)
        final_label = label_encoder.inverse_transform(prediction)[0]

    # Tahmini logla
    log_prediction(data.chief_complaint, data.age, final_label)

    return {
        "final_prediction": final_label,
        "chief_complaint": data.chief_complaint
    }
