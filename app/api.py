from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ✅ Giriş verisini temsil eden sınıf
class InputData(BaseModel):
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

# ✅ Tahmin endpoint’i
@app.post("/predict")
def predict(data: InputData):
    # Şimdilik sadece dummy sınıflandırma (örnek mantık)
    if data.bt > 38 or data.hr > 100 or data.age > 70:
        result = "Kırmızı"
    elif data.pain > 5 or data.sbp < 90:
        result = "Sarı"
    else:
        result = "Yeşil"

    return {"ktas_tahmini": result}
