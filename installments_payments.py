import pandas as pd

file_path  = "C:/Users/anton/OneDrive/Desktop/DATA/installments_payments.csv" 
df = pd.read_csv(file_path)

#Membersihkan duplicate
df_cleaned = df.drop_duplicates()

#Jika lebih dari 50 perseni ni
# f_cleaned[categorical_cols] = df_cleaned[categorical_cols].apply(lambda x: x.str.lower().str.strip())lai di kolomnya hilang, maka kolom tersebut akan dihapus
df_cleaned = df_cleaned.dropna(thresh=len(df_cleaned)* 0.5,axis=1)

#Mengisi kolom numerik yang kosong dengan median dari kolom tersebut 
kolom_numerik = df_cleaned.select_dtypes(include=['int64','float64']).columns
df_cleaned[kolom_numerik] = df_cleaned[kolom_numerik].fillna(df_cleaned[kolom_numerik].median())

#

#Menangani kolom numerik yang memiliki outlier
Q1 = df_cleaned[kolom_numerik].quantile(0.25)
Q3 = df_cleaned[kolom_numerik].quantile(0.75)
IQR = Q3-Q1

df_cleaned = df_cleaned[~((df_cleaned[kolom_numerik] < (Q1 - 1.5 * IQR)) | 
                           (df_cleaned[kolom_numerik] > (Q3 + 1.5 * IQR))).any(axis=1)]


installments_payments = df_cleaned
installments_payments_agg = installments_payments.groupby("SK_ID_CURR").agg({
    "DAYS_INSTALMENT": "mean",
    "DAYS_ENTRY_PAYMENT": lambda x: sum(x < 0), 
    "AMT_PAYMENT": "sum"
})
installments_payments_agg.rename(columns={
    "DAYS_INSTALMENT": "avg_days_installment",
    "DAYS_ENTRY_PAYMENT": "late_payments_count",
    "AMT_PAYMENT": "total_paid_installments"
}, inplace=True)

installments_payments_agg.reset_index(inplace=True)
app_train = "C:/Users/anton/OneDrive/Desktop/DATA/application_train_finall.csv"
data = pd.read_csv(app_train)
data = data.merge(installments_payments_agg, on= "SK_ID_CURR", how= "left").fillna(0)
data.to_csv("application_train_finalll.csv", index=False)

print("file baru sudah ada")