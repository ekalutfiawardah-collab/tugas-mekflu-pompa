import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Konfigurasi Halaman (Harus diletakkan paling atas)
st.set_page_config(page_title="Tubes Mekflu - Kelompok Pompa", page_icon="💧", layout="wide")

# 2. Styling Background & Warna (Perbaikan Error)
st.markdown("""
    <style>
    .stApp {
        background-color: #e0f2f1;
    }
    .main-title {
        color: #00796b;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🚜 Dashboard Simulasi Pompa Air</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Tugas Besar Mekanika Fluida - Teknik Fisika</p>", unsafe_allow_html=True)

# 3. Sidebar Input Parameter
with st.sidebar:
    st.header("⚙️ Konfigurasi Sistem")
    debit = st.slider("Debit Air (Q) - m³/s", 0.01, 0.20, 0.05, step=0.01)
    head = st.number_input("Head (H) - meter", min_value=0.0, value=15.0)
    efisiensi_persen = st.slider("Efisiensi (η) - %", 1, 100, 75)
    st.markdown("---")
    st.info("Atur parameter untuk melihat perubahan daya.")

# 4. Perhitungan Logika
rho = 1000  # kg/m3
g = 9.81    # m/s2
efisiensi = efisiensi_persen / 100
daya_kw = (rho * g * debit * head) / efisiensi / 1000

# 5. Layout Utama
col_anim, col_data = st.columns([1.5, 1])

with col_anim:
    st.subheader("🖼️ Visualisasi Aliran")
    placeholder = st.empty()
    
    # Loop Animasi Sederhana
    for i in range(30): # Dikurangi jumlah frame agar lebih ringan
        fig_anim, ax_anim = plt.subplots(figsize=(6, 4))
        ax_anim.set_xlim(0, 10)
        ax_anim.set_ylim(0, 10)
        ax_anim.axis('off')
        
        # Gambar Badan Pompa
        pump = plt.Circle((5, 5), 1.3, color='#009688', alpha=0.8, ec='black', lw=2)
        ax_anim.add_patch(pump)
        ax_anim.text(5, 5, "POMPA", ha='center', va='center', color='white', fontweight='bold')
        
        # Pipa
        ax_anim.plot([0, 3.8], [5, 5], color='#333333', lw=5) # Inlet
        ax_anim.plot([5, 5], [6.3, 10], color='#333333', lw=5) # Outlet
        
        # Partikel Air
        t = (i * debit * 10) % 10
        ax_anim.plot([(t) % 4], [5], 'bo', ms=10, alpha=0.7) # Masuk
        ax_anim.plot([5], [6 + (t % 4)], 'bo', ms=10, alpha=0.7) # Keluar
        
        placeholder.pyplot(fig_anim)
        plt.close(fig_anim)
        time.sleep(0.05)

with col_data:
    st.subheader("⚡ Output Analisis")
    st.metric(label="Estimasi Daya Listrik", value=f"{daya_kw:.2f} kW")
    
    # Status Daya
    if daya_kw > 20:
        st.error("⚠️ STATUS: DAYA TINGGI")
    else:
        st.success("✅ STATUS: DAYA NORMAL")
    
    st.write(f"**Ringkasan Input:**")
    st.write(f"- Debit: {debit} m³/s")
    st.write(f"- Head: {head} m")
    st.write(f"- Efisiensi: {efisiensi_persen}%")

# 6. Grafik Karakteristik
st.markdown("---")
st.subheader("📊 Grafik Karakteristik Daya vs Debit")
q_range = np.linspace(0.01, 0.3, 100)
p_range = (rho * g * q_range * head) / efisiensi / 1000

fig_graph, ax_graph = plt.subplots(figsize=(10, 3.5))
ax_graph.plot(q_range, p_range, color='#00796b', lw=2, label='Kurva Daya')
ax_graph.scatter(debit, daya_kw, color='red', s=100, label='Titik Operasi', zorder=5)
ax_graph.set_xlabel("Debit (m³/s)")
ax_graph.set_ylabel("Daya (kW)")
ax_graph.legend()
st.pyplot(fig_graph)

st.caption("Tugas Besar Mekanika Fluida - Pekan 14")
