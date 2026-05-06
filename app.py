import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Daya Pompa - Mekflu", page_icon="⚙️")

# Identitas Tugas sesuai TOR
st.title("🚜 Aplikasi Estimasi Daya Listrik Pompa")
st.subheader("Tugas Besar Mekanika Fluida - Teknik Fisika")
st.markdown("---")

# Kolom untuk Gambar Skema dan Deskripsi
col_img, col_text = st.columns([1, 1])

with col_img:
    # Menambahkan gambar skema pompa sederhana untuk visualisasi imajinasi sistem
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Centrifugal_Pump.svg/400px-Centrifugal_Pump.svg.png", 
             caption="Skema Kerja Pompa Sentrifugal", use_container_width=True)

with col_text:
    st.info("""
    **Maksud Tugas:**
    Menghitung kebutuhan daya listrik pompa berdasarkan debit, head, dan efisiensi 
    untuk diaplikasikan dalam kasus nyata.
    """)

# Input Parameter di Sidebar
st.sidebar.header("Input Data Pompa")
debit = st.sidebar.number_input("Debit Air (Q) dalam m³/s:", min_value=0.0, value=0.05, format="%.3f")
head = st.sidebar.number_input("Head Pompa (H) dalam meter:", min_value=0.0, value=15.0)
efisiensi_persen = st.sidebar.slider("Efisiensi Pompa (η) dalam %:", 1, 100, 75)

# Konstanta & Perhitungan Akurat (20% Penilaian)[cite: 1]
rho = 1000  # Massa jenis air (kg/m³)
g = 9.81    # Gravitasi (m/s²)
efisiensi = efisiensi_persen / 100

if debit > 0 and head > 0:
    # Rumus Daya Pompa: P = (rho * g * Q * H) / efisiensi
    daya_watt = (rho * g * debit * head) / efisiensi
    daya_kw = daya_watt / 1000

    # Tampilan Hasil
    st.success(f"### ⚡ Daya Listrik yang Dibutuhkan: {daya_kw:.2f} kW")
    
    # Visualisasi Grafik Karakteristik[cite: 1]
    st.markdown("---")
    st.subheader("📊 Grafik Analisis Daya vs Debit")
    
    q_range = np.linspace(0.001, debit * 2, 50)
    p_range = (rho * g * q_range * head) / efisiensi / 1000

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(q_range, p_range, label='Kebutuhan Daya (kW)', color='green', linewidth=2)
    ax.scatter([debit], [daya_kw], color='red', s=100, label='Titik Operasi Sekarang')
    
    ax.set_xlabel('Debit Air (m³/s)')
    ax.set_ylabel('Daya Listrik (kW)')
    ax.set_title(f'Karakteristik Pompa pada Head {head} meter')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    st.pyplot(fig)
else:
    st.warning("Silakan masukkan nilai Debit dan Head untuk memulai perhitungan.")

# Footer
st.markdown("---")
st.caption("Tugas Besar Mekanika Fluida")
