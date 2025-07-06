import streamlit as st
import requests

st.title("Emergency Triage Tahmin Uygulaması")

# Kullanıcıdan tüm feature’ları alıyoruz:
Group = st.number_input("Group", min_value=0, max_value=1000, value=0)
Age = st.number_input("Age", min_value=0.0, max_value=120.0, value=30.0)
Patients_number_per_hour = st.number_input("Patients_number_per_hour", value=10.0)
SBP = st.number_input("SBP", value=120.0)
DBP = st.number_input("DBP", value=80.0)
HR = st.number_input("HR", value=70.0)
RR = st.number_input("RR", value=16.0)
BT = st.number_input("BT", value=36.5)
Disposition = st.number_input("Disposition", min_value=0, max_value=10, value=0)
KTAS_expert = st.number_input("KTAS_expert", min_value=0, max_value=10, value=0)
Error_group = st.number_input("Error_group", min_value=0, max_value=10, value=0)
Length_of_stay_min = st.number_input("Length_of_stay_min", value=30.0)
mistriage = st.number_input("mistriage", min_value=0, max_value=10, value=0)
risk_score = st.number_input("risk_score", value=0.0)

Sex_1 = st.number_input("Sex_1", min_value=0, max_value=1, value=0)
Sex_2 = st.number_input("Sex_2", min_value=0, max_value=1, value=0)

Arrival_mode_1 = st.number_input("Arrival_mode_1", min_value=0, max_value=1, value=0)
Arrival_mode_2 = st.number_input("Arrival_mode_2", min_value=0, max_value=1, value=0)
Arrival_mode_3 = st.number_input("Arrival_mode_3", min_value=0, max_value=1, value=0)
Arrival_mode_4 = st.number_input("Arrival_mode_4", min_value=0, max_value=1, value=0)
Arrival_mode_5 = st.number_input("Arrival_mode_5", min_value=0, max_value=1, value=0)
Arrival_mode_6 = st.number_input("Arrival_mode_6", min_value=0, max_value=1, value=0)
Arrival_mode_7 = st.number_input("Arrival_mode_7", min_value=0, max_value=1, value=0)

Injury_1 = st.number_input("Injury_1", min_value=0, max_value=1, value=0)
Injury_2 = st.number_input("Injury_2", min_value=0, max_value=1, value=0)

Mental_1 = st.number_input("Mental_1", min_value=0, max_value=1, value=0)
Mental_2 = st.number_input("Mental_2", min_value=0, max_value=1, value=0)
Mental_3 = st.number_input("Mental_3", min_value=0, max_value=1, value=0)
Mental_4 = st.number_input("Mental_4", min_value=0, max_value=1, value=0)

Pain_0 = st.number_input("Pain_0", min_value=0, max_value=1, value=0)
Pain_1 = st.number_input("Pain_1", min_value=0, max_value=1, value=0)

NRS_pain_0 = st.number_input("NRS_pain_0", min_value=0, max_value=1, value=0)
NRS_pain_1 = st.number_input("NRS_pain_1", min_value=0, max_value=1, value=0)
NRS_pain_10 = st.number_input("NRS_pain_10", min_value=0, max_value=1, value=0)
NRS_pain_2 = st.number_input("NRS_pain_2", min_value=0, max_value=1, value=0)
NRS_pain_3 = st.number_input("NRS_pain_3", min_value=0, max_value=1, value=0)
NRS_pain_4 = st.number_input("NRS_pain_4", min_value=0, max_value=1, value=0)
NRS_pain_5 = st.number_input("NRS_pain_5", min_value=0, max_value=1, value=0)
NRS_pain_6 = st.number_input("NRS_pain_6", min_value=0, max_value=1, value=0)
NRS_pain_7 = st.number_input("NRS_pain_7", min_value=0, max_value=1, value=0)
NRS_pain_8 = st.number_input("NRS_pain_8", min_value=0, max_value=1, value=0)
NRS_pain_9 = st.number_input("NRS_pain_9", min_value=0, max_value=1, value=0)


if st.button("Tahmin Et"):
    input_data = {
        "Group": Group,
        "Age": Age,
        "Patients_number_per_hour": Patients_number_per_hour,
        "SBP": SBP,
        "DBP": DBP,
        "HR": HR,
        "RR": RR,
        "BT": BT,
        "Disposition": Disposition,
        "KTAS_expert": KTAS_expert,
        "Error_group": Error_group,
        "Length_of_stay_min": Length_of_stay_min,
        "mistriage": mistriage,
        "risk_score": risk_score,
        "Sex_1": Sex_1,
        "Sex_2": Sex_2,
        "Arrival_mode_1": Arrival_mode_1,
        "Arrival_mode_2": Arrival_mode_2,
        "Arrival_mode_3": Arrival_mode_3,
        "Arrival_mode_4": Arrival_mode_4,
        "Arrival_mode_5": Arrival_mode_5,
        "Arrival_mode_6": Arrival_mode_6,
        "Arrival_mode_7": Arrival_mode_7,
        "Injury_1": Injury_1,
        "Injury_2": Injury_2,
        "Mental_1": Mental_1,
        "Mental_2": Mental_2,
        "Mental_3": Mental_3,
        "Mental_4": Mental_4,
        "Pain_0": Pain_0,
        "Pain_1": Pain_1,
        "NRS_pain_0": NRS_pain_0,
        "NRS_pain_1": NRS_pain_1,
        "NRS_pain_10": NRS_pain_10,
        "NRS_pain_2": NRS_pain_2,
        "NRS_pain_3": NRS_pain_3,
        "NRS_pain_4": NRS_pain_4,
        "NRS_pain_5": NRS_pain_5,
        "NRS_pain_6": NRS_pain_6,
        "NRS_pain_7": NRS_pain_7,
        "NRS_pain_8": NRS_pain_8,
        "NRS_pain_9": NRS_pain_9,
    }

    # FastAPI endpoint URL’si
    url = "http://127.0.0.1:8000/predict"
    response = requests.post(url, json=input_data)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Tahmin Sonucu: {result['prediction']}")
    else:
        st.error("Tahmin sırasında hata oluştu!")