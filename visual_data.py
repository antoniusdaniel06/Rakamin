import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_data_visualization(df):
    sns.set_style("whitegrid")
    
    # 1. Distribusi Status Kredit
    plt.figure(figsize=(6, 4))
    sns.countplot(x=df["TARGET"], palette="coolwarm")
    plt.title("Distribusi Status Kredit (TARGET)")
    plt.xlabel("Status Kredit (0 = Disetujui, 1 = Tidak Disetujui)")
    plt.ylabel("Jumlah Aplikasi")
    plt.show()
    
    # 2. Boxplot Pendapatan berdasarkan Status Kredit
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df["TARGET"], y=df["AMT_INCOME_TOTAL"], palette="coolwarm")
    plt.ylim(0, 500000)  # Batasi agar tidak ada outlier ekstrem
    plt.title("Distribusi Pendapatan berdasarkan Status Kredit")
    plt.xlabel("Status Kredit (0 = Disetujui, 1 = Tidak Disetujui)")
    plt.ylabel("Pendapatan Total")
    plt.show()
    
    # 3. Boxplot Jumlah Kredit berdasarkan Status Kredit
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df["TARGET"], y=df["AMT_CREDIT"], palette="coolwarm")
    plt.ylim(0, 2000000)  # Batasi agar tidak ada outlier ekstrem
    plt.title("Distribusi Jumlah Kredit berdasarkan Status Kredit")
    plt.xlabel("Status Kredit (0 = Disetujui, 1 = Tidak Disetujui)")
    plt.ylabel("Jumlah Kredit")
    plt.show()

# Panggil fungsi dengan dataframe
df = pd.read_csv("C:/Users/anton/OneDrive/Desktop/DATA/application_akhir_cleaned.csv")
df_sample = df[["TARGET", "AMT_INCOME_TOTAL", "AMT_CREDIT"]].copy()
plot_data_visualization(df_sample)

plot_data_visualization(df_sample)
