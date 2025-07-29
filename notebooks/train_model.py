import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression

# 📁 Veri yükle
df = pd.read_csv(r"C:\Users\SERDAR\Desktop\updated - Copy\bootcamp-grup177\data\data_grouped.csv", sep=";", encoding="utf-8", engine="python")

# 🎯 Sütunlar
target = "KTAS_expert"
categorical_features = ['Group', 'Sex', 'Arrival mode', 'Injury', 'Chief_complain', 'Mental', 'Pain', 'KTAS_RN', 'Diagnosis in ED', 'Disposition']
numerical_features = ['Age', 'Patients number per hour', 'NRS_pain', 'SBP', 'DBP', 'HR', 'RR', 'BT', 'Saturation']

# 🧹 Eksik değer temizliği
df.replace(['??', '#NA', 'null', '-', 'N/A'], np.nan, inplace=True)
df[numerical_features] = df[numerical_features].apply(pd.to_numeric, errors='coerce')
df[numerical_features] = df[numerical_features].fillna(df[numerical_features].median())
df[categorical_features] = df[categorical_features].fillna("Unknown")

# 🔴 Kural tabanlı kırmızı tespiti
def rule_based_red(row):
    return (
        (row["SBP"] < 90) |
        (row["HR"] > 130) |
        (row["RR"] > 30) |
        (row["BT"] > 39) |
        (row["NRS_pain"] >= 9)
    )

df["is_red"] = df.apply(rule_based_red, axis=1)
df_filtered = df[~df["is_red"]]  # sadece yeşil ve sarı

# 🔄 X ve y
X = df_filtered[categorical_features + numerical_features]
y = df_filtered[target]

# 🎯 Hedef sütunu encode et
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 🔀 Eğitim/test bölmesi
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 🔧 Dönüştürücüler
categorical_transformer = Pipeline([
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])
numerical_transformer = Pipeline([
    ("scaler", StandardScaler())
])
preprocessor = ColumnTransformer([
    ("cat", categorical_transformer, categorical_features),
    ("num", numerical_transformer, numerical_features)
])

# 🔗 Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
])

# 🧠 Modeli eğit
pipeline.fit(X_train, y_train)

# 💾 Kaydet
model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(model_dir, exist_ok=True)
joblib.dump(pipeline, os.path.join(model_dir, "final_rf_pipeline.joblib"))
joblib.dump(label_encoder, os.path.join(model_dir, "final_label_encoder.joblib"))

print("✅ LogisticRegression modeli yalnızca Sarı ve Yeşil sınıflar için eğitildi. Kırmızı sınıf kurallarla yönetilecek.")
