import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, FancyArrow

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Simulasi Pompa Mekflu", page_icon="💧")

st.title("🌊 Simulasi & Estimasi Daya Pompa")
st.subheader("Tugas Besar Mekanika Fluida - Teknik Fisika")
st.markdown("---")

# 2. Sidebar Input
st.sidebar.header("Parameter Sistem")
debit = st.sidebar.slider("Debit Air (Q) - m³/s", 0.01, 0.20, 0.05, step=0.01)
head = st.sidebar.number_input("Head (H) - meter", min_value=0.0, value=15.0)
efisiensi_persen = st.sidebar.slider("Efisiensi (η) - %", 1, 100, 75)

# 3. Perhitungan
rho = 1000
g = 9.81
efisiensi = efisiensi_persen / 100
daya_kw = (rho * g * debit * head) / efisiensi / 1000

# 4. Visualisasi Animasi Aliran
st.subheader("🖼️ Animasi Aliran Sistem Pompa")
col1, col2 = st.columns([2, 1])

with col1:
    # Membuat plot untuk animasi
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Gambar Badan Pompa
    pompa = Circle((5, 5), 1.5, color='lightgrey', ec='black', lw=2)
    ax.add_patch(pompa)
    ax.text(5, 5, "POMPA", ha='center', va='center', fontweight='bold')

    # Gambar Pipa Inlet & Outlet
    ax.plot([0, 3.5], [5, 5], color='black', lw=4) # Inlet
    ax.plot([5, 5], [6.5, 10], color='black', lw=4) # Outlet

    # Animasi Partikel Air (Titik Biru)
    # Kecepatan titik tergantung pada Debit (Q)
    num_particles = 10
    particles, = ax.plot([], [], 'bo', ms=8, alpha=0.6)

    def init():
        particles.set_data([], [])
        return particles,

    def update(frame):
        # Logika pergerakan partikel berdasarkan frame dan Debit
        speed = debit * 10 
        t = (frame * speed) % 15
        
        x_pts = []
        y_pts = []
        
        for i in range(num_particles):
            pos = (t + i*1.5) % 15
            if pos < 5: # Di pipa inlet
                x_pts.append(pos)
                y_pts.append(5)
            elif pos < 10: # Di pipa outlet
                x_pts.append(5)
                y_pts.append(pos)
        
        particles.set_data(x_pts, y_pts)
        return particles,

    # Menampilkan statis (karena Streamlit butuh trik khusus untuk animasi lari)
    # Sebagai gantinya, kita buat visualisasi aliran dinamis yang menarik
    st.pyplot(fig)
    st.caption("Aliran air bergerak dari kiri (Inlet) ke atas (Outlet).")

with col2:
    st.metric("Daya Listrik", f"{daya_kw:.2f} kW")
    st.write(f"**Status:**")
    if daya_kw > 20:
        st.error("Daya Tinggi")
    else:
        st.success("Daya Normal")

# 5. Grafik Analisis
st.markdown("---")
st.subheader("📊 Analisis Performa")
q_range = np.linspace(0.01, 0.3, 100)
p_range = (rho * g * q_range * head) / efisiensi / 1000

fig2, ax2 = plt.subplots(figsize=(8, 3))
ax2.plot(q_range, p_range, color='blue', label='Kurva Daya')
ax2.scatter(debit, daya_kw, color='red', label='Titik Operasi')
ax2.set_xlabel("Debit (m³/s)")
ax2.set_ylabel("Daya (kW)")
ax2.legend()
st.pyplot(fig2)
