import pandas as pd

file_path  = "C:/Users/anton/OneDrive/Desktop/DATA/bureau.csv" 
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

cleaned_file_path = "C:/Users/anton/OneDrive/Desktop/DATA/bureau_cleaned.csv"
df_cleaned.to_csv(cleaned_file_path, index=False)

# Load dataset
bureau = pd.read_csv(file_path)

# Periksa nama kolom
print("Kolom dalam bureau.csv:", bureau.columns)

# Pastikan SK_ID_CURR ada
if "SK_ID_CURR" not in bureau.columns:
    raise KeyError("Kolom 'SK_ID_CURR' tidak ditemukan dalam bureau.csv")

# Pastikan CREDIT_ACTIVE berupa string
bureau["CREDIT_ACTIVE"] = bureau["CREDIT_ACTIVE"].astype(str)

# Agregasi data bureau
bureau_agg = bureau.groupby("SK_ID_CURR").agg({
    "SK_ID_BUREAU": "count",
    "AMT_CREDIT_SUM": "sum",
    "AMT_CREDIT_SUM_DEBT": "sum",
    "DAYS_CREDIT": "mean",
    "CREDIT_ACTIVE": lambda x: (x == "Active").sum()
}).reset_index()

# Load application_train.csv
application_train = pd.read_csv("application_train.csv")

# Gabungkan dengan application_train
application_train = application_train.merge(bureau_agg, on="SK_ID_CURR", how="left")

# Isi missing value dengan 0
application_train.fillna(0, inplace=True)

# Simpan hasil
application_train.to_csv("application_train_with_bureau.csv", index=False)

print("Gabungan selesai, file disimpan sebagai application_train_with_bureau.csv")