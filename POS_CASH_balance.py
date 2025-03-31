import pandas as pd

file_path  = "C:/Users/anton/OneDrive/Desktop/DATA/POS_CASH_balance.csv" 
df = pd.read_csv(file_path)

#Membersihkan duplicate
df_cleaned = df.drop_duplicates()

#Jika lebih dari 50 perseni ni
# f_cleaned[categorical_cols] = df_cleaned[categorical_cols].apply(lambda x: x.str.lower().str.strip())lai di kolomnya hilang, maka kolom tersebut akan dihapus
df_cleaned = df_cleaned.dropna(thresh=len(df_cleaned)* 0.5,axis=1)

#Mengisi kolom numerik yang kosong dengan median dari kolom tersebut 
kolom_numerik = df_cleaned.select_dtypes(include=['int64','float64']).columns
df_cleaned[kolom_numerik] = df_cleaned[kolom_numerik].fillna(df_cleaned[kolom_numerik].median())


#Menangani kolom numerik yang memiliki outlier
Q1 = df_cleaned[kolom_numerik].quantile(0.25)
Q3 = df_cleaned[kolom_numerik].quantile(0.75)
IQR = Q3-Q1

df_cleaned = df_cleaned[~((df_cleaned[kolom_numerik] < (Q1 - 1.5 * IQR)) | 
                           (df_cleaned[kolom_numerik] > (Q3 + 1.5 * IQR))).any(axis=1)]

POS_CASH_agg = df_cleaned.groupby("SK_ID_CURR").agg({
    "SK_ID_PREV" : "count",
    "CNT_INSTALMENT_FUTURE" : "sum"
})
POS_CASH_agg.rename(columns={
    "SK_ID_PREV" : "pos_total_loans",
    "CNT_INSTALMENT_FUTURE" : "pos_remaining_installments"
}, inplace=True)

POS_CASH_agg.reset_index(inplace=True)

credit_cart = pd.read_csv("C:/Users/anton/OneDrive/Desktop/DATA/credit_card_balance.csv")

cd_cleaned = credit_cart.drop_duplicates()

#Jika lebih dari 50 perseni ni
# f_cleaned[categorical_cols] = df_cleaned[categorical_cols].apply(lambda x: x.str.lower().str.strip())lai di kolomnya hilang, maka kolom tersebut akan dihapus
cd_cleaned = cd_cleaned.dropna(thresh=len(cd_cleaned)* 0.5,axis=1)

#Mengisi kolom numerik yang kosong dengan median dari kolom tersebut 
kolom_numerik = cd_cleaned.select_dtypes(include=['int64','float64']).columns
cd_cleaned[kolom_numerik] = cd_cleaned[kolom_numerik].fillna(cd_cleaned[kolom_numerik].median())


#Menangani kolom numerik yang memiliki outlier
Q1 = cd_cleaned[kolom_numerik].quantile(0.25)
Q3 = cd_cleaned[kolom_numerik].quantile(0.75)
IQR = Q3-Q1

cd_cleaned = cd_cleaned[~((cd_cleaned[kolom_numerik] < (Q1 - 1.5 * IQR)) | 
                           (cd_cleaned[kolom_numerik] > (Q3 + 1.5 * IQR))).any(axis=1)]

credit_cart_agg = cd_cleaned.groupby("SK_ID_CURR").agg({
    "AMT_CREDIT_LIMIT_ACTUAL": "sum",
    "AMT_BALANCE": "sum"
})

credit_cart_agg.rename(columns={
    "AMT_CREDIT_LIMIT_ACTUAL": "credit_card_total_limit",
    "AMT_BALANCE": "credit_card_total_balance"
}, inplace=True)

credit_cart_agg.reset_index(inplace=True)

app_train = pd.read_csv("C:/Users/anton/OneDrive/Desktop/DATA/application_train_finalll.csv")
application_train = app_train.merge(POS_CASH_agg, on="SK_ID_CURR", how="left").fillna(0)
application_train = app_train.merge(credit_cart_agg, on="SK_ID_CURR", how="left").fillna(0)

application_train.to_csv("application_train_akhir.csv", index= False)
print("file akhir sudah ada")