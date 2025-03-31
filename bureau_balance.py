import pandas as pd

print("Script sedang berjalan...")

file_path  = "C:/Users/anton/OneDrive/Desktop/DATA/bureau_balance.csv" 
df = pd.read_csv(file_path)

#Membersihkan duplicate
df_cleaned = df.drop_duplicates()

#Jika lebih dari 50 perseni ni
# f_cleaned[categorical_cols] = df_cleaned[categorical_cols].apply(lambda x: x.str.lower().str.strip())lai di kolomnya hilang, maka kolom tersebut akan dihapus
df_cleaned = df_cleaned.dropna(thresh=len(df_cleaned)* 0.5,axis=1)

#Mengisi kolom numerik yang kosong dengan median dari kolom tersebut 
kolom_numerik = df_cleaned.select_dtypes(include=['int64','float64']).columns
df_cleaned[kolom_numerik] = df_cleaned[kolom_numerik].fillna(df_cleaned[kolom_numerik].median())

#Mengisi kolom katergorikal dengan modus dari kolom tersebut 
kolom_kategorikal = df_cleaned.select_dtypes(include=['object']).columns
df_cleaned[kolom_kategorikal] = df_cleaned[kolom_kategorikal].fillna(df_cleaned[kolom_kategorikal].mode().iloc[0])
df_cleaned[kolom_kategorikal] = df_cleaned[kolom_kategorikal].apply(lambda x: x.str.lower().str.strip())

#Menangani kolom numerik yang memiliki outlier
Q1 = df_cleaned[kolom_numerik].quantile(0.25)
Q3 = df_cleaned[kolom_numerik].quantile(0.75)
IQR = Q3-Q1

df_cleaned = df_cleaned[~((df_cleaned[kolom_numerik] < (Q1 - 1.5 * IQR)) | 
                           (df_cleaned[kolom_numerik] > (Q3 + 1.5 * IQR))).any(axis=1)]

for col in kolom_kategorikal:
    df_cleaned[col] = df_cleaned[col].astype('category')

cleaned_file_path = "C:/Users/anton/OneDrive/Desktop/DATA/bureau_balance_cleaned.csv"
df_cleaned.to_csv(cleaned_file_path, index=False)


# Load dataset
bureau_balance = pd.read_csv(file_path)

# Agregasi data bureau_balance
bureau_balance_agg = bureau_balance.groupby("SK_ID_BUREAU").agg({
    "MONTHS_BALANCE": "count",  # Jumlah bulan laporan kredit
    "STATUS": lambda x: (x == "1").sum()  # Jumlah bulan dengan status keterlambatan
})

# Rename kolom agar lebih jelas
bureau_balance_agg.rename(columns={
    "MONTHS_BALANCE": "bureau_balance_months",
    "STATUS": "bureau_late_payments"
}, inplace=True)

# Reset index
bureau_balance_agg.reset_index(inplace=True)

# Gabungkan dengan bureau.csv agar bisa digabung ke application_train
file = "C:/Users/anton/OneDrive/Desktop/DATA/bureau.csv"
bureau = pd.read_csv(file)
bureau = bureau.merge(bureau_balance_agg, on="SK_ID_BUREAU", how="left")

# Agregasi ulang berdasarkan SK_ID_CURR
bureau_final_agg = bureau.groupby("SK_ID_CURR").agg({
    "bureau_balance_months": "mean",
    "bureau_late_payments": "sum"
})

# Reset index
bureau_final_agg.reset_index(inplace=True)

# Gabungkan dengan application_train
file_train = "C:/Users/anton/OneDrive/Desktop/DATA/application_train_with_bureau.csv"
application_train = pd.read_csv(file_train)
application_train = application_train.merge(bureau_final_agg, on="SK_ID_CURR", how="left")

# Isi missing value dengan 0
application_train.fillna(0, inplace=True)

# Simpan hasil
application_train.to_csv("application_train_final.csv", index=False)



