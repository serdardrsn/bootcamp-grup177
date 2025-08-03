import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Sayfa yapılandırması
st.set_page_config(page_title="Emergency Triage AI", layout="wide")

# Özel CSS stilleri
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            text-align: center;
            margin-bottom: 20px;
            font-weight: bold;
        }
        .logo {
            height: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Üst bar: logo ve başlık
logo_path = "logo.png"
col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo_path, width=150)
with col2:
    st.markdown("<div class='main-title'>🚑 Emergency Triage AI</div>", unsafe_allow_html=True)

# Oturum geçmişi başlat
if "history" not in st.session_state:
    st.session_state.history = []

# Sayfa iki sütuna ayrılıyor
form_col, analysis_col = st.columns([2, 1])

# FORM ALANI
with form_col:
    st.subheader("📋 Hasta Bilgileri Girişi")
    with st.form("triage_form"):
        chief_complaint = st.text_input("Hasta Şikayeti")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Yaş", min_value=0, max_value=120, step=1)
            sbp = st.number_input("Sistolik Kan Basıncı (SBP)", min_value=0)
            dbp = st.number_input("Diyastolik Kan Basıncı (DBP)", min_value=0)
            hr = st.number_input("Nabız (HR)", min_value=0)
            rr = st.number_input("Solunum Sayısı (RR)", min_value=0)
        with col2:
            bt = st.number_input("Vücut Isısı (BT)", min_value=30.0, max_value=45.0, step=0.1)
            mental = st.selectbox("Bilinç Durumu", ["Uyanık", "Yorgun", "Tepkisiz"])
            sex = st.selectbox("Cinsiyet", ["Erkek", "Kadın"])
            arrival_mode = st.selectbox("Geliş Şekli", ["Ambulans", "Yürüyerek", "Sedye ile"])
            injury = st.selectbox("Travma Durumu", ["Evet", "Hayır"])
            pain = st.slider("Ağrı Puanı (0-10)", 0, 10, step=1)

        submit_button = st.form_submit_button("📥 Kayıt Gir")

        if submit_button:
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
                    "mental": mental.lower(),
                    "sex": "female" if sex == "Kadın" else "male",
                    "arrival_mode": arrival_mode.lower(),
                    "injury": "evet" if injury == "Evet" else "hayır",
                    "pain": pain
                }

                try:
                    response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
                    response.raise_for_status()
                    result = response.json()
                    predicted_label = result["final_prediction"]

                    # Oturum geçmişine kaydet
                    st.session_state.history.append({
                        "Tarih/Saat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Şikayet": chief_complaint,
                        "Yaş": age,
                        "SBP": sbp,
                        "DBP": dbp,
                        "HR": hr,
                        "RR": rr,
                        "BT": bt,
                        "Mental": mental,
                        "Cinsiyet": sex,
                        "Geliş Şekli": arrival_mode,
                        "Travma": injury,
                        "Ağrı": pain,
                        "Müdahale Derecesi": predicted_label
                    })

                    # Tahmin kartı renkli kutu ile göster
                    renk_map = {
                        "Kırmızı": ("#FF4B4B", "🔴 <b>Kırmızı Alan:</b> Hayati risk, hemen müdahale."),
                        "Sarı": ("#FFD700", "🟡 <b>Sarı Alan:</b> Orta risk, 30 dk içinde değerlendirme."),
                        "Yeşil": ("#90EE90", "🟢 <b>Yeşil Alan:</b> Stabil, beklemesi uygun.")
                    }

                    ana_renk = predicted_label.split(" ")[0]
                    renk, aciklama = renk_map.get(ana_renk, ("#D3D3D3", "⚪ Belirsiz sınıf."))

                    st.markdown(
                        f"""
                        <div style='background-color: {renk}; padding: 20px; border-radius: 10px; text-align: center; margin-top: 10px;'>
                            <h3 style='color: black;'>Tahmin Sonucu: {predicted_label}</h3>
                            <p style='color: black; font-size: 16px;'>{aciklama}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")

# ANALİZ ALANI
with analysis_col:
    st.subheader("📑 Kayıt Geçmişi")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            label="📥 Verileri Dışa Aktar (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="triage_kayitlari.csv",
            mime="text/csv"
        )
    else:
        st.info("Henüz kayıt yok.")

# Etik bilgilendirme
st.markdown(
    """
    <hr>
    <p style='font-size: 12px; color: gray; text-align: center;'>
        <b>Etik Bilgilendirme:</b> Bu uygulama yalnızca akademik araştırma ve eğitim amaçlı geliştirilmiştir.
        Yapay zekâ destekli çıktılar, klinik kararların yerini almaz. Nihai karar yetkili sağlık personelindedir.
    </p>
    """,
    unsafe_allow_html=True
)
