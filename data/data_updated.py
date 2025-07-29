import pandas as pd

df = pd.read_csv(
    r"C:\Users\SERDAR\Desktop\updated - Copy\bootcamp-grup177\data\data.csv",
    encoding="latin1",        # veya windows-1254 de olabilir
    sep=";",                  # Eğer CSV dosyası noktalı virgülle ayrılmışsa
    decimal=",",              # Türkçe Excel'den gelen ondalık virgül için
)



# KTAS_expert sınıflarını 1: Kırmızı, 2: Sarı, 3: Yeşil olarak yeniden grupla
# Örnek: 1 kırmızı, 2-3 sarı, 4-5 yeşil gibi gruplanabilir
def map_ktas(value):
    if value == 1:
        return "Kırmızı"
    elif value in [2, 3]:
        return "Sarı"
    elif value in [4, 5]:
        return "Yeşil"
    else:
        return "Bilinmiyor"

df['KTAS_expert'] = df['KTAS_expert'].apply(map_ktas)

# Yeni dağılımı kontrol et
print(df['KTAS_expert'].value_counts())

# Kaydetmek istersen:
df.to_csv(
    r"C:\Users\SERDAR\Desktop\updated - Copy\bootcamp-grup177\data\data_grouped.csv",
    index=False,
    encoding="utf-8-sig",  # Türkçe karakterler bozulmasın
    sep=";",               # Aynı ayraçla kaydet
    decimal=","            # Ondalık ayraç uyumu
)

