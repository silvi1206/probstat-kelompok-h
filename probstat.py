import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

# ===============================
# 1️⃣ Baca file CSV
# ===============================
file_path = r"C:\Users\silvi\Downloads\Jumlah Perceraian Menurut Kabupaten_Kota dan Faktor Penyebab Perceraian (perkara) di Provinsi DKI Jakarta, 2024.csv"

# Baca CSV
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()  # hapus spasi ekstra di nama kolom

print("Kolom yang tersedia:", df.columns.tolist())  # cek struktur data

# ===============================
# 2️⃣ Ambil kolom wilayah dan faktor KDRT
# ===============================
# Cari otomatis kolom dengan kata "Kekerasan"
kolom_kdrt = [c for c in df.columns if "Kekerasan" in c]
if not kolom_kdrt:
    raise ValueError("❌ Kolom 'Kekerasan Dalam Rumah Tangga' tidak ditemukan!")

# Ambil hanya kolom kabupaten/kota dan faktor KDRT
data_kdrt = df[["Kabupaten/Kota", kolom_kdrt[0]]].copy()

# ===============================
# 3️⃣ Bersihkan data
# ===============================
data_kdrt = data_kdrt.dropna()

# Hapus baris total "DKI Jakarta" (karena itu jumlah seluruh kota)
data_kdrt = data_kdrt[~data_kdrt["Kabupaten/Kota"].str.fullmatch("DKI Jakarta", case=False)]

# Bersihkan nilai menjadi angka
data_kdrt[kolom_kdrt[0]] = (
    data_kdrt[kolom_kdrt[0]]
    .astype(str)
    .str.replace(r"\D", "", regex=True)
    .replace("", 0)
    .astype(int)
)

# ===============================
# 4️⃣ Hitung statistik deskriptif
# ===============================
x = data_kdrt[kolom_kdrt[0]]
mean_val = x.mean()
median_val = x.median()
mode_val = x.mode()[0]
var_val = x.var()
std_val = x.std()

print("\n📊 Statistik Kekerasan Dalam Rumah Tangga (KDRT) di DKI Jakarta:")
print(f"Mean: {mean_val:.2f}")
print(f"Median: {median_val}")
print(f"Mode: {mode_val}")
print(f"Variance: {var_val:.2f}")
print(f"Standard Deviation: {std_val:.2f}")

# ===============================
# 5️⃣ Buat histogram & kurva KDE
# ===============================
kde = gaussian_kde(x)
x_grid = np.linspace(x.min(), x.max(), 200)
kde_values = kde(x_grid)

plt.figure(figsize=(8,5))
plt.hist(x, bins=10, density=True, alpha=0.4, color="skyblue", edgecolor="black", label="Histogram")
plt.plot(x_grid, kde_values, color="blue", linewidth=2, label="Kurva Kontinu (KDE)")

# Garis Mean, Median, Mode
plt.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val:.2f}')
plt.axvline(median_val, color='green', linestyle='--', label=f'Median: {median_val}')
plt.axvline(mode_val, color='orange', linestyle='--', label=f'Mode: {mode_val}')

plt.title("Distribusi Kasus Perceraian karena Kekerasan Dalam Rumah Tangga (KDRT) di DKI Jakarta, 2024")
plt.xlabel("Jumlah Kasus")
plt.ylabel("Frekuensi Relatif (Density)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
