import pandas as pd

# Load dataset yang sudah dibersihkan
file_path = "application_akhir_cleaned.csv"
df = pd.read_csv(file_path)

# Cek distribusi nilai TARGET
print(df["TARGET"].value_counts(normalize=True))  # Persentase
print(df["TARGET"].value_counts())  # Jumlah absolut


df_raw = pd.read_csv("application_train.csv")

# Cek distribusi nilai TARGET sebelum cleaning
print(df_raw["TARGET"].value_counts(normalize=True))
print(df_raw["TARGET"].value_counts())

df_target1 = df_raw[df_raw["TARGET"] == 1]

# Cek apakah baris dengan TARGET = 1 masih ada di dataset yang sudah dibersihkan
df_target1_after = df[df["TARGET"] == 1]

# Bandingkan jumlahnya
print(f"Jumlah TARGET = 1 sebelum cleaning: {len(df_target1)}")
print(f"Jumlah TARGET = 1 setelah cleaning: {len(df_target1_after)}")


