import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# =========================
# CONFIG & THEME
# =========================
st.set_page_config(page_title="Simulasi Pompa Air Pro", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stNumberInput div[data-baseweb="input"] { border-radius: 8px; }
    div[data-testid="stMetricValue"] { font-size: 2.2rem; font-weight: 700; color: #1f4e79; }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Simulasi Daya Pompa Air Interaktif")
st.write("Visualisasi aliran fluida dan grafik pertumbuhan daya secara Real-Time")

# =========================
# SESSION STATE
# =========================
if "run" not in st.session_state:
    st.session_state.run = False

# =========================
# LAYOUT UTAMA (2 KOLOM BALANS)
# =========================
col_control, col_display = st.columns([1.1, 1.9])

# =========================
# KOLOM KIRI: INPUT PARAMETER
# =========================
with col_control:
    st.subheader("⚙️ Parameter Sistem")
    
    debit = st.number_input(
        "Debit Aliran (Q) dalam m³/s", 
        min_value=0.001, max_value=1.000, value=0.050, step=0.005, format="%.3f"
    )
    head = st.number_input(
        "Total Head Pompa (H) dalam meter", 
        min_value=0.1, max_value=100.0, value=10.0, step=0.5, format="%.1f"
    )
    efisiensi = st.number_input(
        "Efisiensi Pompa (η) dalam %", 
        min_value=5, max_value=100, value=75, step=1
    )
    
    st.markdown("---")
    st.subheader("⚡ Hasil Analisis")
    
    rho = 1000  
    g = 9.81    
    eta = efisiensi / 100
    daya_maks = (rho * g * debit * head) / eta / 1000  
    
    st.metric(label="Kebutuhan Daya Aktual", value=f"{daya_maks:.2f} kW")
    
    if daya_maks > 20:
        st.error("⚠️ Overload: Daya terlalu tinggi untuk sistem standar!")
    else:
        st.success("✅ Aman: Kapasitas daya dalam batas normal.")

# =========================
# KOLOM KANAN: ANIMASI CANVAS & GRAFIK BERJALAN
# =========================
with col_display:
    st.subheader("🔄 Visualisasi Aliran & Konstruksi Pompa")
    
    # Tombol Kontrol
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
            inletParticles.push({{ x: Math.random() * 240, y: 160 + (Math.random() * 26), r: Math.random() * 2.5 + 1.5 }});
            outletParticles.push({{ x: 295 + (Math.random() * 26), y: Math.random() * 110, r: Math.random() * 2.5 + 1.5 }});
        }}

        function drawPump() {{
            // Pipa Inlet
            ctx.fillStyle = "rgba(52, 152, 219, 0.12)"; ctx.fillRect(0, 160, 250, 30);
            ctx.strokeStyle = "#95a5a6"; ctx.lineWidth = 2.5; ctx.beginPath();
            ctx.moveTo(0, 160); ctx.lineTo(250, 160); ctx.moveTo(0, 190); ctx.lineTo(238, 190); ctx.stroke();

            // Pipa Outlet
            ctx.fillStyle = "rgba(52, 152, 219, 0.12)"; ctx.fillRect(295, 0, 30, 110);
            ctx.beginPath(); ctx.moveTo(295, 0); ctx.lineTo(295, 110); ctx.moveTo(325, 0); ctx.lineTo(325, 90); ctx.stroke();

            // Motor
            ctx.fillStyle = "#2c3e50"; ctx.fillRect(360, 135, 100, 80);
            ctx.fillStyle = "#34495e";
            for(let m=0; m<6; m++) {{
                ctx.fillRect(370 + (m*14), 127, 7, 8); ctx.fillRect(370 + (m*14), 215, 7, 8);
            }}

            // Casing Volute
            ctx.fillStyle = "#1a446c"; ctx.beginPath(); ctx.arc(310, 175, 60, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = "#112d47"; ctx.lineWidth = 3; ctx.stroke();

            // Impeller Space
            ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(310, 175, 40, 0, Math.PI * 2); ctx.fill();
        }}

        function drawImpeller(rotAngle) {{
            ctx.save(); ctx.translate(310, 175); ctx.rotate(rotAngle);
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
                if (isRunning) {{ p.y -= speed * 0.5 + 0.3; if (p.y < 0) p.y = 105; }}
            }});

            requestAnimationFrame(loop);
        }}
        loop();
    </script>
    """
    st.components.v1.html(canvas_html, height=340)

    # ==========================================
    # LOGIKA GRAFIK BERJALAN (LIVE CHART)
    # ==========================================
    st.markdown("---")
    st.subheader("📊 Kurva Karakteristik Operasional Pompa (Live)")
    
    # Wadah kosong khusus untuk menaruh grafik agar bisa di-update berkala
    chart_placeholder = st.empty()

    # Membuat base kurva tipis di latar belakang
    q_curve = np.linspace(0.001, max(0.250, debit * 1.5), 100)
    p_curve = (rho * g * q_curve * head) / eta / 1000

    if st.session_state.run:
        # Loop untuk menjalankan pergerakan grafik titik kerja
        for step in range(1, 31):
            # Jika user menekan tombol stop di tengah jalan, hentikan loop grafik
            if not st.session_state.run:
                break
                
            # Naikkan nilai debit dan daya secara bertahap (efek animasi loading)
            current_q = (debit / 30) * step
            current_p = (rho * g * current_q * head) / eta / 1000

            fig, ax = plt.subplots(figsize=(11, 3.5))
            ax.plot(q_curve, p_curve, color='#1f4e79', linewidth=2, alpha=0.5, label='Kurva Karakteristik')
            
            # Garis jejak jalannya grafik
            q_track = np.linspace(0.001, current_q, step)
            p_track = (rho * g * q_track * head) / eta / 1000
            ax.plot(q_track, p_track, color='#e74c3c', linewidth=3, label='Pertumbuhan Daya')
            
            # Titik kerja yang sedang berjalan
            ax.scatter(current_q, current_p, color='#e74c3c', s=130, zorder=5)

            # Proyeksi garis putus-putus
            ax.axhline(current_p, color='gray', linestyle=':', alpha=0.5)
            ax.axvline(current_q, color='gray', linestyle=':', alpha=0.5)

            ax.set_xlabel("Debit Fluida Q (m³/s)", fontsize=9)
            ax.set_ylabel("Daya Mekanis P (kW)", fontsize=9)
            ax.set_xlim(0, max(0.250, debit * 1.3))
            ax.set_ylim(0, max(p_curve) * 1.1)
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Tampilkan grafik ke placeholder
            chart_placeholder.pyplot(fig)
            plt.close(fig)
            
            # Kecepatan update grafik
            time.sleep(0.04)

    # Kondisi standar/ketika di-stop (Menampilkan grafik statis di titik akhir)
    if not st.session_state.run:
        fig, ax = plt.subplots(figsize=(11, 3.5))
        ax.plot(q_curve, p_curve, color='#1f4e79', linewidth=2.5, label='Kurva Karakteristik Daya')
        ax.scatter(debit, daya_maks, color='#e74c3c', s=140, zorder=5, label='Titik Operasional Kerja')
        
        ax.axhline(daya_maks, color='gray', linestyle=':', alpha=0.7)
        ax.axvline(debit, color='gray', linestyle=':', alpha=0.7)
        
        ax.set_xlabel("Debit Fluida Q (m³/s)", fontsize=9)
        ax.set_ylabel("Daya Mekanis P (kW)", fontsize=9)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend(loc='upper left', fontsize=9)
        
        chart_placeholder.pyplot(fig)
        plt.close(fig)
        
