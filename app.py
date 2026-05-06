import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Daya Pompa - Mekflu", page_icon="⚙️")

# Identitas Tugas sesuai TOR
st.title("🚜 Aplikasi Estimasi Daya Listrik Pompa")
st.subheader("Tugas Besar Mekanika Fluida - Teknik Fisika")
st.markdown("---")

# Input Parameter di Sidebar
st.sidebar.header("Input Data Pompa")
debit = st.sidebar.number_input("Debit Air (Q) dalam m³/s:", min_value=0.0, value=0.05, format="%.3f")
head = st.sidebar.number_input("Head Pompa (H) dalam meter:", min_value=0.0, value=15.0)
efisiensi_persen = st.sidebar.slider("Efisiensi Pompa (η) dalam %:", 1, 100, 75)

# Konstanta & Perhitungan
rho = 1000  # kg/m³
g = 9.81    # m/s²
efisiensi = efisiensi_persen / 100

# Bagian Visualisasi Utama (Imajinasi Sistem)[cite: 1]
st.subheader("🖼️ Visualisasi Sistem Pompa")
col1, col2 = st.columns([1, 1])

with col1:
    # Membuat diagram sederhana menggunakan Matplotlib agar pasti muncul
    fig_diag, ax_diag = plt.subplots(figsize=(4, 3))
    ax_diag.add_patch(plt.Circle((0.5, 0.5), 0.2, color='blue', alpha=0.3)) # Simbol Pompa
    ax_diag.annotate('POMPA', xy=(0.5, 0.5), ha='center', va='center', fontweight='bold')
    ax_diag.arrow(0.1, 0.5, 0.2, 0, head_width=0.05, head_length=0.05, fc='k', ec='k') # Inlet
    ax_diag.arrow(0.7, 0.5, 0, 0.3, head_width=0.05, head_length=0.05, fc='k', ec='k') # Outlet
    ax_diag.text(0.1, 0.4, f"Q: {debit} m³/s")
    ax_diag.text(0.75, 0.7, f"H: {head} m")
    ax_diag.set_xlim(0, 1)
    ax_diag.set_ylim(0, 1)
    ax_diag.axis('off')
    st.pyplot(fig_diag)

with col2:
    if debit > 0 and head > 0:
        daya_watt = (rho * g * debit * head) / efisiensi
        daya_kw = daya_watt / 1000
        st.metric(label="Estimasi Daya Listrik", value=f"{daya_kw:.2f} kW")
        st.write(f"Efisiensi: {efisiensi_persen}%")
    else:
        st.warning("Masukkan nilai Q dan H")

# Grafik Analisis[cite: 1]
st.markdown("---")
st.subheader("📊 Grafik Analisis Daya vs Debit")
q_range = np.linspace(0.001, (debit * 2) if debit > 0 else 1, 50)
p_range = (rho * g * q_range * head) / efisiensi / 1000

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(q_range, p_range, label='Kebutuhan Daya (kW)', color='green', linewidth=2)
if debit > 0:
    ax.scatter([debit], [daya_kw], color='red', s=100, label='Titik Operasi Anda', zorder=5)

ax.set_xlabel('Debit Air (m³/s)')
ax.set_ylabel('Daya Listrik (kW)')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()
st.pyplot(fig)

st.caption("Tugas Besar Mekanika Fluida[cite: 1]")
