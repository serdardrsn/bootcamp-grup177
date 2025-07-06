import streamlit as st
import json
import requests

st.title("Emergency Triage AI - Veri Girişi Formu")

# Sayısal veriler
age = st.number_input("Yaş", min_value=0, max_value=120, step=1)
sbp = st.number_input("Sistolik Kan Basıncı (SBP)", min_value=0)
dbp = st.number_input("Diyastolik Kan Basıncı (DBP)", min_value=0)
hr = st.number_input("Nabız (HR)", min_value=0)
rr = st.number_input("Solunum Hızı (RR)", min_value=0)
bt = st.number_input("Vücut Isısı (BT)", min_value=30.0, format="%.1f")

# Kategorik veriler
mental = st.selectbox("Bilinç Durumu", ["Uyanık", "Yorgun", "Tepkisiz"])
sex = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
arrival_mode = st.selectbox("Hastanın Geliş Şekli", ["Ambulans", "Yürüyerek", "Sedye ile"])
injury = st.selectbox("Travma Durumu", ["Evet", "Hayır"])
pain = st.slider("Ağrı Puanı (0-10)", 0, 10, step=1)

# Gönder butonu (tek ve benzersiz key ile)
if st.button("Veriyi Gönder"):
    input_data = {
        "age": age,
        "sbp": sbp,
        "dbp": dbp,
        "hr": hr,
        "rr": rr,
        "bt": bt,
        "mental": mental,
        "sex": sex,
        "arrival_mode": arrival_mode,
        "injury": injury,
        "pain": pain
    }

    st.subheader("JSON Formatına Dönüştürülen Veri")
    st.json(input_data)

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        result = response.json()
        st.success(f"Tahmin: {result['ktas_tahmini']}")
    except Exception as e:
        st.error(f"API bağlantısı başarısız: {e}")