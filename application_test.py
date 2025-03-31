import pandas as pd

# Load dataset
file_path = "C:/Users/anton/OneDrive/Desktop/DATA/application_test.csv"
df = pd.read_csv(file_path)

# 1. Menghapus Duplikasi Data
df_cleaned = df.drop_duplicates()

# 2. Menangani Missing Values
# - Jika lebih dari 50% nilai di kolom hilang, hapus kolom tersebut
missing_threshold = 0.5
df_cleaned = df_cleaned.dropna(thresh= len(df_cleaned) * missing_threshold, axis=1) #tresh untuk menentukan minimal data valid/atau tidak berisi nan

# - Untuk kolom numerik, isi dengan median
numerical_cols = df_cleaned.select_dtypes(include=['int64', 'float64']).columns
df_cleaned[numerical_cols] = df_cleaned[numerical_cols].fillna(df_cleaned[numerical_cols].median())

# - Untuk kolom kategorikal, isi dengan modus (nilai yang paling sering muncul)
categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
df_cleaned[categorical_cols] = df_cleaned[categorical_cols].fillna(df_cleaned[categorical_cols].mode().iloc[0])

# 3. Menyelaraskan Format Data Kategorikal (lowercase dan trim)
df_cleaned[categorical_cols] = df_cleaned[categorical_cols].apply(lambda x: x.str.lower().str.strip())

# 4. Menangani Outlier menggunakan IQR (Interquartile Range)
Q1 = df_cleaned[numerical_cols].quantile(0.25)
Q3 = df_cleaned[numerical_cols].quantile(0.75)
IQR = Q3 - Q1

df_cleaned = df_cleaned[~((df_cleaned[numerical_cols] < (Q1 - 1.5 * IQR)) | 
                           (df_cleaned[numerical_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

# 5. Mengubah Format Data yang Sesuai
# - Mengubah kategori menjadi tipe kategori untuk efisiensi
for col in categorical_cols:
    df_cleaned[col] = df_cleaned[col].astype('category')

# Simpan file hasil pembersihan
cleaned_file_path = "C:/Users/anton/OneDrive/Desktop/DATA/application_test_cleaned.csv"
df_cleaned.to_csv(cleaned_file_path, index=False)

# Tampilkan ringkasan setelah pembersihan
print(df_cleaned.info())
print(df_cleaned.head())

# File output bisa diunduh
print(f"File cleaned dataset tersedia di: {cleaned_file_path}")
