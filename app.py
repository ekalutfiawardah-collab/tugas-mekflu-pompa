import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# 1. Konfigurasi Halaman & Styling
st.set_page_config(page_title="Simulasi Pompa Mekflu", page_icon="⚙️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f0f4f7; }
    .main-title { color: #d32f2f; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚜 Dashboard Simulasi Pompa Sentrifugal</h1>", unsafe_allow_html=True)

# 2. Sidebar Input
with st.sidebar:
    st.header("⚙️ Parameter Input")
    debit = st.slider("Debit Air (Q) - m³/s", 0.01, 0.20, 0.05, step=0.01)
    head = st.number_input("Head (H) - meter", min_value=0.0, value=15.0)
    efisiensi_persen = st.slider("Efisiensi (η) - %", 1, 100, 75)
    st.markdown("---")
    st.caption("Tugas Besar Mekanika Fluida")

# 3. Perhitungan
rho, g = 1000, 9.81
efisiensi = efisiensi_persen / 100
daya_kw = (rho * g * debit * head) / efisiensi / 1000

# 4. Layout Utama
col_anim, col_data = st.columns([1.5, 1])

with col_anim:
    st.subheader("🖼️ Visualisasi Operasi Sistem")
    placeholder = st.empty()
    
    # Animasi Partikel Aliran
    for i in range(30):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        # --- MENGGAMBAR POMPA (Berdasarkan Gambar Referensi) ---
        # Badan Motor (Merah)
        motor = patches.FancyBboxPatch((2, 2.5), 4, 3, boxstyle="round,pad=0.2", color='#ff5252', ec='black', lw=2)
        ax.add_patch(motor)
        # Garis-garis sirip motor
        for x in [2.8, 3.8, 4.8]:
            ax.plot([x, x], [2.7, 5.3], color='black', lw=2)
        
        # Bagian Depan Pompa (Abu-abu)
        pump_head = patches.Rectangle((6, 3), 1.5, 2, color='#9e9e9e', ec='black', lw=2)
        ax.add_patch(pump_head)
        
        # Pipa Inlet (Kanan Bawah) & Pipa Outlet (Atas)
        ax.plot([7.5, 10, 10], [4, 4, 1.5], color='#333333', lw=6) # Inlet
        ax.plot([6.75, 6.75, 8], [5, 7, 7], color='#333333', lw=6)  # Outlet
        
        # Dasar/Kaki Pompa
        base = patches.Polygon([[2.5, 2.5], [5.5, 2.5], [6, 2], [2, 2]], color='#616161', ec='black')
        ax.add_patch(base)

        # --- ANIMASI ALIRAN (Titik Biru) ---
        t = (i * debit * 12) % 12
        # Aliran Masuk (Inlet)
        if t < 4:
            ax.plot([10], [1.5 + t], 'bo', ms=8)
        # Aliran Keluar (Outlet)
        else:
            ax.plot([6.75 + (t-4)%3], [7], 'bo', ms=8)
            ax.plot([6.75], [5 + (t-4)%2], 'bo', ms=8)

        placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.04)

with col_data:
    st.subheader("⚡ Analisis Daya")
    st.metric(label="Estimasi Daya Listrik", value=f"{daya_kw:.2f} kW")
    
    if daya_kw > 20:
        st.error("⚠️ STATUS: DAYA TINGGI")
    else:
        st.success("✅ STATUS: DAYA NORMAL")
    
    st.write("**Data Perhitungan:**")
    st.info(f"Daya = (ρ · g · Q · H) / η\nDaya = (1000 · 9.81 · {debit} · {head}) / {efisiensi}")

# 5. Grafik Karakteristik
st.markdown("---")
st.subheader("📊 Hubungan Debit vs Daya")
q_axis = np.linspace(0.01, 0.3, 100)
p_axis = (rho * g * q_axis * head) / efisiensi / 1000

fig_gr, ax_gr = plt.subplots(figsize=(10, 3))
ax_gr.plot(q_axis, p_axis, color='#d32f2f', lw=2)
ax_gr.scatter(debit, daya_kw, color='black', s=80, zorder=5)
ax_gr.set_xlabel("Debit (m³/s)")
ax_gr.set_ylabel("Daya (kW)")
ax_gr.grid(True, alpha=0.3)
st.pyplot(fig_gr)
