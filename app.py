import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# Konfigurasi halaman
st.set_page_config(page_title="Simulasi Pompa Air", page_icon="💧", layout="wide")

st.title("💧 Simulasi Estimasi Daya Pompa Air")
st.write("Masukkan parameter untuk melihat estimasi daya dan proses aliran air")

# Sidebar input
with st.sidebar:
    st.header("⚙️ Input Parameter")
    debit = st.slider("Debit Air (Q) [m³/s]", 0.01, 0.2, 0.05)
    head = st.number_input("Head Pompa (H) [m]", 1.0, 100.0, 15.0)
    efisiensi = st.slider("Efisiensi (%)", 10, 100, 75)

    start = st.button("▶️ Jalankan Simulasi")

# Perhitungan
rho = 1000
g = 9.81
eta = efisiensi / 100

daya = (rho * g * debit * head) / eta / 1000  # kW

col1, col2 = st.columns([2, 1])

# =========================
# VISUALISASI ANIMASI
# =========================
with col1:
    st.subheader("🔄 Visualisasi Aliran Pompa")
    placeholder = st.empty()

    if start:
        for i in range(50):

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')

            # Pompa
            pump = plt.Circle((5, 5), 1.2, color='teal')
            ax.add_patch(pump)
            ax.text(5, 5, "POMPA", ha='center', va='center', color='white')

            # Pipa masuk
            ax.plot([0, 4], [5, 5], linewidth=5)

            # Pipa keluar
            ax.plot([5, 5], [6.2, 10], linewidth=5)

            # Partikel air (lebih banyak & bergerak)
            speed = debit * 20

            for j in range(5):
                t = (i * speed + j * 2) % 10

                # Inlet flow
                if t < 4:
                    ax.plot(t, 5, 'bo')

                # Outlet flow
                if t > 4:
                    ax.plot(5, 6 + (t - 4), 'bo')

            placeholder.pyplot(fig)
            plt.close(fig)

            time.sleep(0.05)

# =========================
# OUTPUT DATA
# =========================
with col2:
    st.subheader("⚡ Output")

    st.metric("Daya Pompa", f"{daya:.2f} kW")

    if daya > 20:
        st.error("⚠️ Daya besar (butuh energi tinggi)")
    else:
        st.success("✅ Daya normal")

    st.write("### Detail Input")
    st.write(f"Debit: {debit} m³/s")
    st.write(f"Head: {head} m")
    st.write(f"Efisiensi: {efisiensi}%")

# =========================
# GRAFIK
# =========================
st.markdown("---")
st.subheader("📊 Grafik Daya vs Debit")

q = np.linspace(0.01, 0.3, 100)
p = (rho * g * q * head) / eta / 1000

fig2, ax2 = plt.subplots()
ax2.plot(q, p)
ax2.scatter(debit, daya)

ax2.set_xlabel("Debit (m³/s)")
ax2.set_ylabel("Daya (kW)")

st.pyplot(fig2)
