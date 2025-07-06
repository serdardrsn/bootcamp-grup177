from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()


model = joblib.load("model.joblib")
label_encoder = joblib.load("label_encoder.joblib")
feature_columns = joblib.load("feature_columns.joblib")

class InputData(BaseModel):
    Group: int
    Age: float
    Patients_number_per_hour: float
    SBP: float
    DBP: float
    HR: float
    RR: float
    BT: float
    Disposition: int
    KTAS_expert: int
    Error_group: int
    Length_of_stay_min: float
    mistriage: int
    risk_score: float
    Sex_1: int
    Sex_2: int
    Arrival_mode_1: int
    Arrival_mode_2: int
    Arrival_mode_3: int
    Arrival_mode_4: int
    Arrival_mode_5: int
    Arrival_mode_6: int
    Arrival_mode_7: int
    Injury_1: int
    Injury_2: int
    Mental_1: int
    Mental_2: int
    Mental_3: int
    Mental_4: int
    Pain_0: int
    Pain_1: int
    NRS_pain_0: int
    NRS_pain_1: int
    NRS_pain_10: int
    NRS_pain_2: int
    NRS_pain_3: int
    NRS_pain_4: int
    NRS_pain_5: int
    NRS_pain_6: int
    NRS_pain_7: int
    NRS_pain_8: int
    NRS_pain_9: int


@app.post("/predict")
def predict(data: InputData):
    
    input_data = pd.DataFrame([data.dict()], columns=feature_columns)

    
    prediction = model.predict(input_data)[0]
    predicted_label = label_encoder.inverse_transform([prediction])[0]

    return {"prediction": predicted_label}