import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =========================
# CONFIG & THEME
# =========================
st.set_page_config(page_title="Simulasi Pompa Air Pro", layout="wide")

# Custom CSS untuk mempercantik card dan input box
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stNumberInput div[data-baseweb="input"] {
        border-radius: 8px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f4e79;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Simulasi Daya Pompa Air Interaktif")
st.write("Visualisasi aliran fluida dinamis dengan input presisi")

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
# KOLOM KIRI: INPUT PARAMETER (DIKETIK)
# =========================
with col_control:
    st.subheader("⚙️ Parameter Sistem")
    
    debit = st.number_input(
        "Debit Aliran (Q) dalam m³/s", 
        min_value=0.001, 
        max_value=1.000, 
        value=0.050, 
        step=0.005,
        format="%.3f",
        help="Ketik nilai debit air. Contoh: 0.050"
    )
    
    head = st.number_input(
        "Total Head Pompa (H) dalam meter", 
        min_value=0.1, 
        max_value=100.0, 
        value=10.0, 
        step=0.5,
        format="%.1f",
        help="Ketik tinggi dorong pompa dalam satuan meter."
    )
    
    efisiensi = st.number_input(
        "Efisiensi Pompa (η) dalam %", 
        min_value=5, 
        max_value=100, 
        value=75, 
        step=1,
        help="Ketik efisiensi mekanis pompa (5% - 100%)."
    )
    
    st.markdown("---")
    st.subheader("⚡ Hasil Analisis")
    
    # Perhitungan Mekanika Fluida & Daya
    rho = 1000  # kg/m³
    g = 9.81    # m/s²
    eta = efisiensi / 100
    daya = (rho * g * debit * head) / eta / 1000  # Rumus Daya Hidrolis (kW)
    
    st.metric(label="Kebutuhan Daya Aktual", value=f"{daya:.2f} kW")
    
    if daya > 20:
        st.error("⚠️ Overload: Daya terlalu tinggi untuk sistem standar!")
    else:
        st.success("✅ Aman: Kapasitas daya dalam batas normal.")

# =========================
# KOLOM KANAN: ANIMASI CANVAS & GRAFIK
# =========================
with col_display:
    st.subheader("🔄 Visualisasi Aliran & Konstruksi Pompa")
    
    # Pengkondisian tombol kontrol di atas canvas
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("▶️ Jalankan", use_container_width=True):
            st.session_state.run = True
    with c2:
        if st.button("⏹️ Stop", use_container_width=True):
            st.session_state.run = False
            
    is_running = "true" if st.session_state.run else "false"
    base_speed = np.clip(debit * 100, 1, 25)

    # HTML5 Canvas Animation Code
    canvas_html = f"""
    <div style="background: white; padding: 10px; border-radius: 12px; border: 1px solid #e0e0e0; text-align: center;">
        <div style="text-align: left; margin-bottom: 8px; font-weight: bold; font-family: sans-serif; font-size: 14px; color: #555;">
            Kondisi Pompa: <span style="color: {'#2ecc71' if st.session_state.run else '#e74c3c'};">
                {'● AKTIF (MENGALIR)' if st.session_state.run else '● NON-AKTIF'}
            </span>
        </div>
        <canvas id="pumpCanvas" width="650" height="350" style="background:#f4f7f9; border-radius: 8px;"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('pumpCanvas');
        const ctx = canvas.getContext('2d');
        
        const isRunning = {is_running};
        const speed = {base_speed};
        let angle = 0;

        let inletParticles = [];
        let outletParticles = [];
        
        for(let i=0; i<25; i++) {{
            inletParticles.push({{ x: Math.random() * 240, y: 185 + (Math.random() * 26), r: Math.random() * 2.5 + 1.5 }});
            
            // PERBAIKAN DI SINI: Memisahkan penutup object kurung kurawal agar f-string Python tidak error
            outletParticles.push({{ 
                x: 295 + (Math.random() * 26), 
                y: Math.random() * 130, 
                r: Math.random() * 2.5 + 1.5 
            }});
        }}

        function drawPump() {{
            // Pipa Suction (Inlet)
            ctx.fillStyle = "rgba(52, 152, 219, 0.12)";
            ctx.fillRect(0, 185, 250, 30);
            ctx.strokeStyle = "#95a5a6";
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.moveTo(0, 185); ctx.lineTo(250, 185);
            ctx.moveTo(0, 215); ctx.lineTo(238, 215);
            ctx.stroke();

            // Pipa Discharge (Outlet)
            ctx.fillStyle = "rgba(52, 152, 219, 0.12)";
            ctx.fillRect(295, 0, 30, 130);
            ctx.beginPath();
            ctx.moveTo(295, 0); ctx.lineTo(295, 130);
            ctx.moveTo(325, 0); ctx.lineTo(325, 110);
            ctx.stroke();

            // Casing Blok Motor (Heatsink)
            ctx.fillStyle = "#2c3e50";
            ctx.fillRect(360, 160, 100, 80);
            ctx.fillStyle = "#34495e";
            for(let m=0; m<6; m++) {{
                ctx.fillRect(370 + (m*14), 152, 7, 8);
                ctx.fillRect(370 + (m*14), 240, 7, 8);
            }}

            // Rumah Siput Pompa (Volute Casing)
            ctx.fillStyle = "#1a446c";
            ctx.beginPath();
            ctx.arc(310, 200, 60, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#112d47";
            ctx.lineWidth = 3;
            ctx.stroke();

            // Ruang Impeller Internal
            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(310, 200, 40, 0, Math.PI * 2);
            ctx.fill();
        }}

        function drawImpeller(rotAngle) {{
            ctx.save();
            ctx.translate(310, 200);
            ctx.rotate(rotAngle);
            ctx.strokeStyle = "#7f8c8d";
            ctx.lineWidth = 4;
            
            for (let i = 0; i < 6; i++) {{
                ctx.rotate((Math.PI * 2) / 6);
                ctx.beginPath();
                ctx.quadraticCurveTo(0, 0, 15, 25);
                ctx.stroke();
            }}
            
            ctx.fillStyle = "#34495e";
            ctx.beginPath();
            ctx.arc(0, 0, 8, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }}

        function loop() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (isRunning) angle += (speed * 0.04);

            drawPump();

            // Partikel Air Masuk (Inlet)
            ctx.fillStyle = "#3498db";
            inletParticles.forEach(p => {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
                if (isRunning) {{
                    p.x += speed * 0.4 + 0.3;
                    if (p.x > 250) p.x = 0;
                }}
            }});

            drawImpeller(angle);

            // Partikel Air Keluar (Outlet)
            ctx.fillStyle = "#2980b9";
            outletParticles.forEach(p => {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
                if (isRunning) {{
                    p.y -= speed * 0.5 + 0.3;
                    if (p.y < 0) p.y = 125;
                }}
            }});

            requestAnimationFrame(loop);
        }}
        loop();
    </script>
    """
    st.components.v1.html(canvas_html, height=395)

# =========================
# GRAFIK DIAGRAM DI BAGIAN BAWAH
# =========================
st.markdown("---")
st.subheader("📊 Kurva Karakteristik Operasional Pompa")

# Membuat kalkulasi kurva kontinu
q_curve = np.linspace(0.001, 0.250, 150)
p_curve = (rho * g * q_curve * head) / eta / 1000

fig, ax = plt.subplots(figsize=(11, 3.5))
ax.plot(q_curve, p_curve, color='#1f4e79', linewidth=2.5, label='Kurva Karakteristik Daya')
ax.scatter(debit, daya, color='#e74c3c', s=140, zorder=5, label='Titik Operasional Kerja')

# Garis putus-putus proyeksi titik
ax.axhline(daya, color='gray', linestyle=':', alpha=0.7)
ax.axvline(debit, color='gray', linestyle=':', alpha=0.7)

ax.set_xlabel("Debit Fluida Q (m³/s)", fontsize=9)
ax.set_ylabel("Daya Mekanis P (kW)", fontsize=9)
ax.set_title(f"Analisis Dinamis pada Konstanta Head {head} meter", fontsize=10, fontweight='bold', color='#333333')
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend(loc='upper left', fontsize=9)

st.pyplot(fig)
