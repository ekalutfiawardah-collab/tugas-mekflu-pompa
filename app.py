import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Simulasi Pompa Air", layout="wide")

st.title("💧 Simulasi Daya Pompa Air Interaktif")
st.write("Visualisasi aliran fluida berdasarkan parameter input")

# =========================
# SESSION STATE
# =========================
if "run" not in st.session_state:
    st.session_state.run = False

# =========================
# INPUT
# =========================
with st.sidebar:
    st.header("⚙️ Input Parameter")

    debit = st.slider("Debit (m³/s)", 0.01, 0.2, 0.05)
    head = st.number_input("Head (m)", 1.0, 50.0, 10.0)
    efisiensi = st.slider("Efisiensi (%)", 10, 100, 75)

    if st.button("▶️ Jalankan"):
        st.session_state.run = True

    if st.button("⏹️ Stop"):
        st.session_state.run = False

# =========================
# PERHITUNGAN
# =========================
rho = 1000
g = 9.81
eta = efisiensi / 100

daya = (rho * g * debit * head) / eta / 1000

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([2, 1])

# =========================
# ANIMASI
# =========================
with col1:
    st.subheader("🔄 Visualisasi Aliran Fluida")

    placeholder = st.empty()

    if st.session_state.run:
        for i in range(100):

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')

            # ======================
            # POMPA (LINGKARAN)
            # ======================
            pump = plt.Circle((5, 5), 1.2, color='teal')
            ax.add_patch(pump)

            # ======================
            # IMPELLER (BERPUTAR)
            # ======================
            angle = i * 20
            for k in range(4):
                x = 5 + 0.9 * np.cos(np.radians(angle + k * 90))
                y = 5 + 0.9 * np.sin(np.radians(angle + k * 90))
                ax.plot([5, x], [5, y], linewidth=2, color='white')

            # ======================
            # PIPA
            # ======================
            ax.plot([0, 4], [5, 5], linewidth=6)      # inlet
            ax.plot([5, 5], [6.2, 10], linewidth=6)   # outlet

            # ======================
            # KECEPATAN AIR
            # ======================
            speed_in = debit * 20
            speed_out = debit * 35  # lebih cepat karena head

            # ======================
            # ALIRAN MASUK
            # ======================
            for j in range(15):
                t = (i * speed_in + j) % 4
                ax.plot([t, t + 0.3], [5, 5], linewidth=2, color='blue')

            # ======================
            # ALIRAN KELUAR
            # ======================
            for j in range(15):
                t = (i * speed_out + j) % 4
                ax.plot([5, 5], [6 + t, 6.3 + t], linewidth=2, color='blue')

            # ======================
            # PANAH ARAH
            # ======================
            ax.arrow(2, 5, 1, 0, head_width=0.3)
            ax.arrow(5, 7, 0, 1, head_width=0.3)

            placeholder.pyplot(fig)
            plt.close(fig)

            time.sleep(0.05)

# =========================
# OUTPUT
# =========================
with col2:
    st.subheader("⚡ Output")

    st.metric("Daya Pompa", f"{daya:.2f} kW")

    if daya > 20:
        st.error("⚠️ Daya tinggi")
    else:
        st.success("✅ Daya normal")

    st.write("### Detail:")
    st.write(f"Debit = {debit} m³/s")
    st.write(f"Head = {head} m")
    st.write(f"Efisiensi = {efisiensi}%")

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
