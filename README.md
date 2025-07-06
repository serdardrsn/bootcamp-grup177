# Emergency Triage AI 

## 1. Takım Bilgileri
**Takım Adı:** Takım 177

**Takım Üyeleri ve Rolleri:**
- Andaç Bilgili – Project Owner  
- Serdar Dursun – Scrum Master  
- Mustafa Günhan – Developer  
- Tuğçe Önder – Developer  
- Eren Eroğlu – Developer

## 2. Proje ve Ürün Tanımı
**Emergency Triage AI**, acil servislerde hasta önceliklendirme (triage) sürecini dijitalleştirmeye ve sağlık profesyonellerine karar destek sunmaya yönelik geliştirilmiş, veri temelli ve yapay zeka destekli bir sistemdir. Projenin temel amacı, hasta kabul anında girilen hayati bulgular ve semptomlara dayalı olarak, hastanın klinik aciliyet düzeyini hızlı ve güvenilir bir şekilde tahmin etmektir.

Bu sistemde referans alınan sınıflandırma protokolü, **Korean Triage and Acuity Scale (KTAS)** olup, hastaları “Kırmızı (çok acil)”, “Sarı (acil)” ve “Yeşil (daha az acil)” olmak üzere üç ana kategoriye ayırmayı amaçlar. KTAS, hastanın klinik durumuna dayalı aciliyet skorlarını standartlaştırarak, sağlık kaynaklarının etkili kullanılmasını destekleyen yaygın bir triyaj ölçeğidir.

Geleneksel KTAS uygulamaları sağlık personelinin bireysel değerlendirmelerine dayanırken, **Emergency Triage AI** bu süreci otomatikleştirerek:
- Yanlılık ve tutarsızlığı azaltmayı,
- Zaman kazandırmayı,
- Ön değerlendirme süreçlerini standardize etmeyi hedeflemektedir.

## 3. Sprint Yönetimi ve Trello
Sprint takibi Trello üzerinden yapılmıştır. Sprint 1 panosuna ait bağlantı:  
🔗 https://trello.com/invite/b/68665405dede83130f458f73/ATTIc0d28ec31b5a2e3f11f642a9e7280ed023B5F3A6/bootcamp-sprint-1

## 4. Sprint 1 Görev Özeti ve Durumu

Sprint 1 toplam **100 puan** olarak hedeflenmiştir ve bu hedef başarıyla gerçekleştirilmiştir. Projenin veri hazırlığı, kullanıcı arayüzü ve temel API altyapısı bu sprintte tamamlanmış ve sistem uçtan uca çalışır hâle getirilmiştir.

### ✅ Tamamlanan Görevler

- Kaggle veri setinin indirilmesi ve dokümantasyonu  
- Eksik/uyumsuz değerlerin analizi  
- KTAS sınıf dönüşümü  
- Özellik mühendisliği  
- Feature açıklama dokümantasyonu  
- Form mimarisi + input tipi belirleme  
- Giriş inputlarının entegresi  
- Dropdown alanlarının kodlanması  
- Veri transfer formatı belirleme  
- FastAPI kurulumu  
- Tahmin endpoint'inin oluşturulması  
- Streamlit → API bağlantısı  
- GitHub repo oluşturma ve branch yapısı  
- Ekran görüntüsü ve kullanıcı dökümantasyonu  
- Sprint 1 özet raporu hazırlanması  
- API dummy veri testleri  
- UI input testleri  
- Geliştirici API dokümantasyonu  
- Uygulama mimarisi şeması  

---

## 5. Kullanıcı Arayüzü (Streamlit Form)
![Streamlit Formu](Screenshot%202025-07-06%20184850.png)

## 6. Sprint Board Görüntüsü (Trello)
![Trello Board](Screenshot%202025-07-06%20200715.png)

## 7. API Dökümantasyonu (Geliştirici)

**Endpoint:** `POST /predict`

**Giriş (JSON):**
```json
{
  "age": 76,
  "sbp": 100,
  "dbp": 70,
  "hr": 120,
  "rr": 20,
  "bt": 39.2,
  "mental": "Tepkisiz",
  "sex": "Kadın",
  "arrival_mode": "Ambulans",
  "injury": "Evet",
  "pain": 7
}
```

**Dönüş:**
```json
{
  "ktas_tahmini": "Kırmızı"
}
```

> Tahmin mantığı: Ateş > 38, Nabız > 100 veya Yaş > 70 → Kırmızı

## 8. Uygulama Mimarisi (Akış)

```
Kullanıcı
   ↓
Streamlit Form
   ↓
JSON Veri
   ↓
FastAPI /predict Endpoint
   ↓
Model ile Tahmin
   ↓
Tahmin Sonucu
```

> Bu yapı yerel çalışmaya ve modüler entegrasyona uygundur.
