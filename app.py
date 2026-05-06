import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Animasi Aliran Pompa", page_icon="💧")

st.title("🌊 Simulasi Aliran Pompa Real-Time")
st.markdown("---")

# 2. Sidebar Input
st.sidebar.header("Kontrol Aliran")
debit = st.sidebar.slider("Debit Air (Q)", 0.01, 0.20, 0.05, step=0.01)
head = st.sidebar.number_input("Head (H)", min_value=0.0, value=15.0)
efisiensi = 0.75

# 3. Perhitungan Daya
daya_kw = (1000 * 9.81 * debit * head) / efisiensi / 1000

# 4. Placeholder untuk Animasi
# Kita butuh empty container agar gambar bisa di-update terus menerus
frame_holder = st.empty()

# 5. Logika Animasi Aliran
# Kita buat loop agar titik-titik (partikel air) terlihat bergerak
for frame in range(100):  # Jalankan 100 frame animasi
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Gambar Struktur Tetap (Pompa & Pipa)
    circle = plt.Circle((5, 5), 1.2, color='blue', alpha=0.2, ec='black', lw=2)
    ax.add_patch(circle)
    ax.text(5, 5, "POMPA", ha='center', va='center', fontweight='bold')
    ax.plot([0, 4], [5, 5], color='black', lw=3)   # Pipa Masuk
    ax.plot([5, 5], [6, 10], color='black', lw=3)  # Pipa Keluar

    # Membuat Partikel yang Bergerak
    # Kecepatan aliran dipengaruhi oleh nilai Debit (Q)
    t = (frame * debit * 5) % 10 
    
    # Partikel di Pipa Masuk (Horizontal)
    ax.plot([(t) % 4], [5], 'bo', ms=8)
    ax.plot([(t + 2) % 4], [5], 'bo', ms=8, alpha=0.5)

    # Partikel di Pipa Keluar (Vertikal)
    # Partikel ini muncul setelah partikel masuk "sampai" ke pompa
    y_pos = 6 + ((t) % 4)
    ax.plot([5], [y_pos], 'bo', ms=8)
    ax.plot([5], [y_pos - 1.5], 'bo', ms=8, alpha=0.5)

    # Update tampilan di Streamlit
    frame_holder.pyplot(fig)
    plt.close(fig) # Hapus plot lama agar tidak membebani memori
    
    # Kecepatan refresh frame
    time.sleep(0.05)

# 6. Info Hasil (Muncul di bawah animasi)
st.metric("Estimasi Daya Listrik", f"{daya_kw:.2f} kW")
if daya_kw > 20:
    st.error("Status: Daya Tinggi (Beban Berat)")
else:
    st.success("Status: Daya Normal")
