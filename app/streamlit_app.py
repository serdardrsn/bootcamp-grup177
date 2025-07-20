import streamlit as st
import requests

# Sayfa ayarları
st.set_page_config(page_title="Emergency Triage AI", layout="centered")
st.title("🚑 Emergency Triage AI")
st.markdown("Acil servise başvuran hastaların önceliklendirilmesini sağlayan yapay zeka destekli sistem.")

st.header("📋 Hasta Bilgilerini Girin")

# Kullanıcı girişleri
chief_complaint = st.text_input("Hasta Şikayeti (Chief Complaint)")
age = st.number_input("Yaş", min_value=0, max_value=120, step=1)
sbp = st.number_input("Sistolik Kan Basıncı (SBP)", min_value=0)
dbp = st.number_input("Diyastolik Kan Basıncı (DBP)", min_value=0)
hr = st.number_input("Nabız (HR)", min_value=0)
rr = st.number_input("Solunum Sayısı (RR)", min_value=0)
bt = st.number_input("Vücut Isısı (BT)", min_value=30.0, max_value=45.0, step=0.1)
mental = st.selectbox("Bilinç Durumu", ["Uyanık", "Yorgun", "Tepkisiz"])
sex = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
arrival_mode = st.selectbox("Hastanın Geliş Şekli", ["Ambulans", "Yürüyerek", "Sedye ile"])
injury = st.selectbox("Travma Durumu", ["Evet", "Hayır"])
pain = st.slider("Ağrı Puanı (0-10)", 0, 10, step=1)

# Tahmin butonu
if st.button("🚨 Tahmin Yap"):
    if not chief_complaint:
        st.error("Lütfen hasta şikayetini girin.")
    else:
        input_data = {
            "chief_complaint": chief_complaint,
            "age": age,
            "sbp": sbp,
            "dbp": dbp,
            "hr": hr,
            "rr": rr,
            "bt": float(bt),
            "mental": mental,
            "sex": sex,
            "arrival_mode": arrival_mode,
            "injury": injury,
            "pain": pain
        }

        try:
            # API isteği
            response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
            response.raise_for_status()
            result = response.json()

            st.subheader("📝 Hasta Şikayeti")
            st.write(result["chief_complaint"])

            # Model tahmini renkli kutu ile göster
            renk_map = {
                "Kırmızı": ("#FF4B4B", "🔴 <b>Kırmızı Alan:</b> Hayati risk, hemen müdahale."),
                "Turuncu": ("#FF8C00", "🟠 <b>Turuncu Alan:</b> Yüksek risk, acil müdahale."),
                "Sarı": ("#FFD700", "🟡 <b>Sarı Alan:</b> Orta risk, 30 dk içinde değerlendirme."),
                "Yeşil": ("#90EE90", "🟢 <b>Yeşil Alan:</b> Stabil, beklemesi uygun."),
                "Mavi": ("#87CEEB", "🔵 <b>Mavi Alan:</b> Çok düşük risk, yönlendirme yapılabilir.")
            }

            renk, aciklama = renk_map.get(result["model_prediction"], ("#D3D3D3", "⚪ Belirsiz sınıf."))

            st.markdown(
                f"""
                <div style='background-color: {renk}; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h2 style='color: black;'>Model Tahmini: {result['model_prediction']}</h2>
                    <p style='color: black; font-size: 18px;'>{aciklama}</p>
                    <p><b>Tahmin Güveni:</b> {result['model_probability']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Rule-based tahmin
            st.subheader("📌 Rule-Based Tahmin")
            st.info(f"{result['rule_based_prediction']} - {result['rule_based_reason']}")

        except Exception as e:
            st.error(f"API bağlantı hatası: {e}")


