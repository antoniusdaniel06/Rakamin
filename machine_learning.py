from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import pandas as pd
# Pilih fitur yang relevan untuk prediksi
df = pd.read_csv("C:/Users/anton/OneDrive/Desktop/DATA/application_akhir_cleaned.csv")
selected_features = ["AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "CNT_CHILDREN"]
X = df[selected_features]
y = df["TARGET"]

# Menangani nilai yang hilang dengan imputasi (menggunakan median)
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(X)

# Normalisasi fitur numerik
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Split data menjadi training dan testing set
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Menampilkan bentuk dataset setelah preprocessing
X_train.shape, X_test.shape

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Inisialisasi dan pelatihan model Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prediksi pada data uji
y_pred = model.predict(X_test)

# Evaluasi model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(accuracy, report)

