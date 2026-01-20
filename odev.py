import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score

# veri okuma
df = pd.read_csv('data.rar')

# boş verileri silme
df.dropna(inplace=True)

# zamanı düzeltme
df['Date'] = pd.to_datetime(df['time'].astype(float), unit='s')
df['Hour'] = df['Date'].dt.hour


#pivot
pivot_tablosu = pd.pivot_table(
    df, 
    index='Hour', 
    values='use [kW]', 
    aggfunc='mean'
)
pivot_tablosu.columns = ['Normal_tuketim']


# 3. MODEL EĞİTİMİ
features = ['Hour', 'temperature', 'humidity', 'pressure']
X = df[features]
y = df['use [kW]']

# Veriyi böldüm.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# RandomForest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_r2 = r2_score(y_test, rf_model.predict(X_test))

# KNN
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn_model = KNeighborsRegressor(n_neighbors=5)
knn_model.fit(X_train_scaled, y_train)
knn_r2 = r2_score(y_test, knn_model.predict(X_test_scaled))

#R2 skor karşılaştırması
print("MODEL BAŞARISI (R2 SCORE)")
print(f"Random Forest R2: {rf_r2:.3f}")
print(f"KNN R2          : {knn_r2:.3f}")




# Örnek veri oluşturdum
senaryo_saat = 20
yeni_senaryo = pd.DataFrame({
    'Hour': [senaryo_saat], 
    'temperature': [10], 
    'humidity': [0.85], 
    'pressure': [1015]
})

#Model tahmini
tahmin = rf_model.predict(yeni_senaryo)[0]

# Pivottan bakıyoz
normal_deger = pivot_tablosu.loc[senaryo_saat, 'Normal_tuketim']

durum = "YÜKSEK (ANORMAL)" if tahmin > (normal_deger * 1.5) else "NORMAL"
print(f"Modelin Tahmini : {tahmin:.4f} kW")
print(f"Normal Değer    : {normal_deger:.4f} kW")
print(f"SONUÇ           : {durum}")