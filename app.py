import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# =========================
# CONFIG & THEME
# =========================
st.set_page_config(page_title="Simulasi Pompa Air Pro", layout="wide")

# Custom CSS untuk mempercantik UI, Card, dan Input Box
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    .stNumberInput div[data-baseweb="input"] { border-radius: 8px; }
    
    /* Style untuk kotak hasil analisis yang mewah */
    .analysis-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .parameter-text {
        font-size: 0.95rem;
        color: #4a5568;
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Simulasi Daya Pompa Air Interaktif")
st.write("Visualisasi aliran fluida dinamis dengan modul analisis parameter lengkap")

# =========================
# SESSION STATE
# =========================
if "run" not in st.session_state:
    st.session_state.run = False

# =========================
# LAYOUT UTAMA (2 KOLOM BALANS)
# =========================
col_control, col_display = st.columns([1.2, 1.8])

# =========================
# KOLOM KIRI: INPUT & HASIL ANALISIS (UPGRADED)
# =========================
with col_control:
    st.subheader("⚙️ Parameter Sistem")
    
    debit = st.number_input(
        "Debit Aliran (Q) dalam m³/s", 
        min_value=0.001, max_value=1.000, value=0.050, step=0.005, format="%.3f",
        help="Volume fluida yang dialirkan per satuan waktu."
    )
    head = st.number_input(
        "Total Head Pompa (H) dalam meter", 
        min_value=0.1, max_value=100.0, value=10.0, step=0.5, format="%.1f",
        help="Tinggi tekan/dorong hidrolis efektif pompa."
    )
    efisiensi = st.number_input(
        "Efisiensi Pompa (η) dalam %", 
        min_value=5, max_value=100, value=75, step=1,
        help="Rasio daya hidrolis output dibanding daya mekanis input."
    )
    
    st.markdown("---")
    st.subheader("⚡ Hasil Analisis")
    
    # -------------------------
    # LOGIKA PERHITUNGAN TEKNIS
    # -------------------------
    rho = 1000  # Massa jenis air (kg/m³)
    g = 9.81    # Percepatan gravitasi (m/s²)
    eta = efisiensi / 100
    
    # 1. Daya Hidrolis (Daya air murni tanpa rugi-rugi)
    daya_hidrolis = (rho * g * debit * head) / 1000  # kW
    # 2. Daya Poros / Aktual (Daya motor listrik yang dibutuhkan)
    daya_aktual = daya_hidrolis / eta  # kW
    
    # -------------------------
    # TAMPILAN KARTU HASIL (CARD VIEW)
    # -------------------------
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    
    # Tampilan Utama: Metrik Daya Aktual
    st.metric(
        label="🔋 Kebutuhan Daya Aktual (P_input)", 
        value=f"{daya_aktual:.2f} kW",
        delta=f"Daya Air: {daya_hidrolis:.2f} kW",
        delta_color="inverse"
    )
    
    # Visualisasi Efisiensi dengan Progress Bar Dinamis
    st.markdown(f'<div class="parameter-text">⚡ <b>Efisiensi Sistem:</b> {efisiensi}%</div>', unsafe_allow_html=True)
    st.progress(efisiensi / 100)
    
    # Rincian Data Teknis dalam Baris Ringkas
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    st.markdown(f"🔹 **Massa Jenis Fluida ($\\\\rho$):** {rho} $kg/m^3$")
    st.markdown(f"🔹 **Laju Volume ($Q$):** {debit:.3f} $m^3/s$")
    st.markdown(f"🔹 **Tinggi Tekan ($H$):** {head:.1f} $m$")
    
    # Persamaan Matematika yang Digunakan
    st.markdown("---")
    st.markdown("**Formulasi Dasar:**")
    st.latex(r"P_{aktual} = \frac{\rho \cdot g \cdot Q \cdot H}{\eta \cdot 1000}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Status Evaluasi Sistem Berdasarkan Batas Daya
    if daya_aktual > 30:
        st.error("🚨 **STATUS: CRITICAL OVERLOAD**\n\nKebutuhan daya terlalu ekstrem (> 30 kW). Rekomendasi: Gunakan pipa berdiameter lebih besar untuk mengurangi *friction head loss*, atau bagi beban ke beberapa pompa pararel.")
    elif daya_aktual > 15:
        st.warning("⚠️ **STATUS: HEAVY DUTY**\n\nOperasi membutuhkan daya menengah atas (15 - 30 kW). Pastikan sistem pendingin motor listrik (*heatsink*) bekerja optimal.")
    else:
        st.success("✅ **STATUS: NORMAL OPERATION**\n\nSistem bekerja pada rentang daya efisien dan aman (< 15 kW). Konsumsi energi terkontrol dengan baik.")

# =========================
# KOLOM KANAN: ANIMASI CANVAS & GRAFIK BERJALAN
# =========================
with col_display:
    st.subheader("🔄 Visualisasi Aliran & Konstruksi Pompa")
    
    # Tombol Kontrol Pompa
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("▶️ Jalankan", use_container_width=True):
            st.session_state.run = True
    with c2:
        if st.button("⏹️ Stop", use_container_width=True):
            st.session_state.run = False
            
    is_running = "true" if st.session_state.run else "false"
    base_speed = np.clip(debit * 100, 1, 25)

    # HTML5 Canvas untuk Animasi Pompa
    canvas_html = f"""
    <div style="background: white; padding: 10px; border-radius: 12px; border: 1px solid #e0e0e0; text-align: center;">
        <div style="text-align: left; margin-bottom: 8px; font-weight: bold; font-family: sans-serif; font-size: 14px; color: #555;">
            Kondisi Pompa: <span style="color: {'#2ecc71' if st.session_state.run else '#e74c3c'};">
                {'● AKTIF (MENGALIR)' if st.session_state.run else '● NON-AKTIF'}
            </span>
        </div>
        <canvas id="pumpCanvas" width="650" height="300" style="background:#f4f7f9; border-radius: 8px;"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('pumpCanvas');
        const ctx = canvas.getContext('2d');
        const isRunning = {is_running};
        const speed = {base_speed};
        let angle = 0;
        let inletParticles = []; let outletParticles = [];
        
        for(let i=0; i<25; i++) {{
            inletParticles.push({{ x: Math.random() * 240, y: 135 + (Math.random() * 26), r: Math.random() * 2.5 + 1.5 }});
            outletParticles.push({{ x: 295 + (Math.random() * 26), y: Math.random() * 90, r: Math.random() * 2.5 + 1.5 }});
        }}

        function drawPump() {{
            ctx.fillStyle = "rgba(52, 152, 219, 0.12)"; ctx.fillRect(0, 135, 250, 30);
            ctx.strokeStyle = "#95a5a6"; ctx.lineWidth = 2.5; ctx.beginPath();
            ctx.moveTo(0, 135); ctx.lineTo(250, 135); ctx.moveTo(0, 165); ctx.lineTo(238, 165); ctx.stroke();

            ctx.fillStyle = "rgba(52, 152, 219, 0.12)"; ctx.fillRect(295, 0, 30, 90);
            ctx.beginPath(); ctx.moveTo(295, 0); ctx.lineTo(295, 90); ctx.moveTo(325, 0); ctx.lineTo(325, 70); ctx.stroke();

            ctx.fillStyle = "#2c3e50"; ctx.fillRect(360, 110, 100, 80);
            ctx.fillStyle = "#34495e";
            for(let m=0; m<6; m++) {{
                ctx.fillRect(370 + (m*14), 102, 7, 8); ctx.fillRect(370 + (m*14), 190, 7, 8);
            }}

            ctx.fillStyle = "#1a446c"; ctx.beginPath(); ctx.arc(310, 150, 60, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = "#112d47"; ctx.lineWidth = 3; ctx.stroke();

            ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(310, 150, 40, 0, Math.PI * 2); ctx.fill();
        }}

        function drawImpeller(rotAngle) {{
            ctx.save(); ctx.translate(310, 150); ctx.rotate(rotAngle);
            ctx.strokeStyle = "#7f8c8d"; ctx.lineWidth = 4;
            for (let i = 0; i < 6; i++) {{
                ctx.rotate((Math.PI * 2) / 6); ctx.beginPath(); ctx.quadraticCurveTo(0, 0, 15, 25); ctx.stroke();
            }}
            ctx.fillStyle = "#34495e"; ctx.beginPath(); ctx.arc(0, 0, 8, 0, Math.PI * 2); ctx.fill(); ctx.restore();
        }}

        function loop() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (isRunning) angle += (speed * 0.04);
            drawPump();

            ctx.fillStyle = "#3498db";
            inletParticles.forEach(p => {{
                ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
                if (isRunning) {{ p.x += speed * 0.4 + 0.3; if (p.x > 250) p.x = 0; }}
            }});

            drawImpeller(angle);

            ctx.fillStyle = "#2980b9";
            outletParticles.forEach(p => {{
                ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
                if (isRunning) {{ p.y -= speed * 0.5 + 0.3; if (p.y < 0) p.y = 85; }}
            }});

            requestAnimationFrame(loop);
        }}
        loop();
    </script>
    """
    st.components.v1.html(canvas_html, height=330)

    # ==========================================
    # GRAFIK BERJALAN (LIVE CHART)
    # ==========================================
    st.markdown("---")
    st.subheader("📊 Kurva Karakteristik Operasional Pompa (Live)")
    
    chart_placeholder = st.empty()

    q_curve = np.linspace(0.001, max(0.250, debit * 1.5), 100)
    p_curve = (rho * g * q_curve * head) / eta / 1000

    if st.session_state.run:
        for step in range(1, 31):
            if not st.session_state.run:
                break
                
            current_q = (debit / 30) * step
            current_p = (rho * g * current_q * head) / eta / 1000

            fig, ax = plt.subplots(figsize=(11, 3.5))
            ax.plot(q_curve, p_curve, color='#1f4e79', linewidth=2, alpha=0.5, label='Kurva Karakteristik')
            
            q_track = np.linspace(0.001, current_q, step)
            p_track = (rho * g * q_track * head) / eta / 1000
            ax.plot(q_track, p_track, color='#e74c3c', linewidth=3, label='Pertumbuhan Daya')
            
            ax.scatter(current_q, current_p, color='#e74c3c', s=130, zorder=5)
            ax.axhline(current_p, color='gray', linestyle=':', alpha=0.5)
            ax.axvline(current_q, color='gray', linestyle=':', alpha=0.5)

            ax.set_xlabel("Debit Fluida Q (m³/s)", fontsize=9)
            ax.set_ylabel("Daya Mekanis P (kW)", fontsize=9)
            ax.set_xlim(0, max(0.250, debit * 1.3))
            ax.set_ylim(0, max(p_curve) * 1.1)
            ax.grid(True, linestyle='--', alpha=0.3)
            
            chart_placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.04)

    if not st.session_state.run:
        fig, ax = plt.subplots(figsize=(11, 3.5))
        ax.plot(q_curve, p_curve, color='#1f4e79', linewidth=2.5, label='Kurva Karakteristik Daya')
        ax.scatter(debit, daya_aktual, color='#e74c3c', s=140, zorder=5, label='Titik Operasional Kerja')
        
        ax.axhline(daya_aktual, color='gray', linestyle=':', alpha=0.7)
        ax.axvline(debit, color='gray', linestyle=':', alpha=0.7)
        
        ax.set_xlabel("Debit Fluida Q (m³/s)", fontsize=9)
        ax.set_ylabel("Daya Mekanis P (kW)", fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend(loc='upper left', fontsize=9)
        
        chart_placeholder.pyplot(fig)
        plt.close(fig)
