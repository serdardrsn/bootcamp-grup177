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
            "mental": mental.lower(),  # örnek: "uyanık"
            "sex": "female" if sex == "Kadın" else "male",
            "arrival_mode": arrival_mode.lower(),  # örnek: "ambulans"
            "injury": "evet" if injury == "Evet" else "hayır",
            "pain": pain
        }

        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
            response.raise_for_status()
            result = response.json()

            st.subheader("📝 Hasta Şikayeti")
            st.write(result["chief_complaint"])

            predicted_label = result["final_prediction"]
            ana_renk = predicted_label.split(" ")[0]  # ilk kelimeye göre renk sınıfı

            renk_map = {
                "Kırmızı": ("#FF4B4B", "🔴 <b>Kırmızı Alan:</b> Hayati risk, hemen müdahale."),
                "Sarı": ("#FFD700", "🟡 <b>Sarı Alan:</b> Orta risk, 30 dk içinde değerlendirme."),
                "Yeşil": ("#90EE90", "🟢 <b>Yeşil Alan:</b> Stabil, beklemesi uygun.")
            }

            renk, aciklama = renk_map.get(ana_renk, ("#D3D3D3", "⚪ Belirsiz sınıf."))

            st.markdown(
                f"""
                <div style='background-color: {renk}; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h2 style='color: black;'>Tahmin Sonucu: {predicted_label}</h2>
                    <p style='color: black; font-size: 18px;'>{aciklama}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        except requests.exceptions.RequestException as e:
            st.error(f"API bağlantı hatası: {e}")
        except Exception as e:
            st.error(f"İşlem sırasında bir hata oluştu: {e}")

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
