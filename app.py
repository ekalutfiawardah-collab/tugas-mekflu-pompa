import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Mekanika Fluida - Telkom University", page_icon="💧")

# Header Aplikasi sesuai TOR
st.title("🌊 Aplikasi Estimasi Daya Pompa & Turbin")
st.write("Tugas Besar Mekanika Fluida - Program Studi Teknik Fisika")
st.write("---")

# Sidebar untuk Input Parameter
st.sidebar.header("Konfigurasi Input")
pilihan_soal = st.sidebar.radio("Pilih Jenis Sistem:", ["Pompa (Soal 2)", "Turbin (Soal 1)"])

# Input User berdasarkan kebutuhan soal
debit = st.sidebar.number_input("Masukkan Debit Air (Q) dalam m³/s:", min_value=0.0, value=0.1, format="%.3f")
head = st.sidebar.number_input("Masukkan Head (H) dalam meter:", min_value=0.0, value=10.0)
efisiensi_persen = st.sidebar.slider("Efisiensi (η) dalam %:", 1, 100, 80)

# Konstanta Fisika
rho = 1000  # Massa jenis air (kg/m³)
g = 9.81    # Percepatan gravitasi (m/s²)
efisiensi = efisiensi_persen / 100

# Logika Perhitungan Berdasarkan Jenis Sistem[cite: 1]
if pilihan_soal == "Pompa (Soal 2)":
    # Rumus Daya Pompa: P = (rho * g * Q * H) / efisiensi
    daya_watt = (rho * g * debit * head) / efisiensi
    label_hasil = "Estimasi Daya Listrik yang DIBUTUHKAN Pompa"
    warna_metric = "inverse"
else:
    # Rumus Daya Turbin: P = rho * g * Q * H * efisiensi
    daya_watt = rho * g * debit * head * efisiensi
    label_hasil = "Estimasi Daya Listrik yang DIHASILKAN Turbin"
    warna_metric = "normal"

daya_kw = daya_watt / 1000

# Menampilkan Hasil Utama[cite: 1]
st.subheader("Hasil Perhitungan")
st.metric(label=label_hasil, value=f"{daya_kw:.2f} kW")

# Visualisasi Sederhana (Grafik Hubungan Debit vs Daya)[cite: 1]
st.write("---")
st.subheader("📊 Visualisasi Sistem (Imajinasi Operasi)")
st.info("Grafik di bawah menunjukkan bagaimana perubahan debit air memengaruhi daya pada sistem Anda.")

# Data untuk Grafik
q_range = np.linspace(0.01, (debit * 2) if debit > 0 else 1.0, 50)
if pilihan_soal == "Pompa (Soal 2)":
    p_range = (rho * g * q_range * head) / efisiensi / 1000
else:
    p_range = (rho * g * q_range * head * efisiensi) / 1000

# Plotting menggunakan Matplotlib
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(q_range, p_range, label='Kurva Karakteristik Daya', color='blue', linewidth=2)
ax.scatter([debit], [daya_kw], color='red', s=100, label='Titik Operasi Saat Ini', zorder=5)
ax.set_xlabel('Debit (m³/s)')
ax.set_ylabel('Daya (kW)')
ax.set_title(f'Hubungan Debit vs Daya pada Head {head}m')
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()

st.pyplot(fig)

# Footer Identitas
st.write("---")
st.caption("Dibuat untuk memenuhi Tugas Besar Mekanika Fluida Semester Genap 2024/2025[cite: 1]")
