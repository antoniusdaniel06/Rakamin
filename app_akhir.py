import pandas as pd

file_path  = "C:/Users/anton/OneDrive/Desktop/DATA/application_train_akhir.csv" 
df = pd.read_csv(file_path)

# Membersihkan duplicate
df_cleaned = df.drop_duplicates()

# Hapus kolom yang lebih dari 50% missing
df_cleaned = df_cleaned.dropna(thresh=len(df_cleaned) * 0.5, axis=1)

# Mengisi kolom numerik yang kosong dengan median dari kolom tersebut 
kolom_numerik = df_cleaned.select_dtypes(include=['int64', 'float64']).columns
df_cleaned[kolom_numerik] = df_cleaned[kolom_numerik].fillna(df_cleaned[kolom_numerik].median())

# Mengisi kolom kategorikal dengan modus dari kolom tersebut 
kolom_kategorikal = df_cleaned.select_dtypes(include=['object']).columns
df_cleaned[kolom_kategorikal] = df_cleaned[kolom_kategorikal].fillna(df_cleaned[kolom_kategorikal].mode().iloc[0])
df_cleaned[kolom_kategorikal] = df_cleaned[kolom_kategorikal].apply(lambda x: x.str.lower().str.strip())

# **PISAHKAN DATA BERDASARKAN TARGET**
df_target_1 = df_cleaned[df_cleaned["TARGET"] == 1]  # Simpan semua data gagal bayar
df_target_0 = df_cleaned[df_cleaned["TARGET"] == 0]  # Data lancar bayar yang akan difilter

# **HITUNG IQR HANYA UNTUK TARGET = 0**
Q1 = df_target_0[kolom_numerik].quantile(0.25)
Q3 = df_target_0[kolom_numerik].quantile(0.75)
IQR = Q3 - Q1

# **BUAT MASK UNTUK FILTERING OUTLIER HANYA UNTUK TARGET = 0**
mask_outlier = (df_target_0[kolom_numerik] >= (Q1 - 1.5 * IQR)) & (df_target_0[kolom_numerik] <= (Q3 + 1.5 * IQR))
df_target_0_cleaned = df_target_0[mask_outlier.all(axis=1)]

# **GABUNGKAN KEMBALI DATA TARGET = 1 & TARGET = 0 YANG TELAH DIFILTER**
df_cleaned = pd.concat([df_target_1, df_target_0_cleaned], ignore_index=True)

# Konversi kategori untuk kolom kategorikal
for col in kolom_kategorikal:
    df_cleaned[col] = df_cleaned[col].astype('category')

# Simpan hasil
cleaned_file_path = "C:/Users/anton/OneDrive/Desktop/DATA/application_akhir_cleaned.csv"
df_cleaned.to_csv(cleaned_file_path, index=False)

print(df_cleaned["TARGET"].value_counts())  # Cek jumlah data per kelas
print(df_cleaned.info())
print(df_cleaned.head())
