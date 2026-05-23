import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Simulasi Pompa Air Pro", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Simulasi Daya Pompa Air Interaktif")
st.write("Visualisasi aliran fluida berdasarkan parameter input")

# =========================
# SESSION STATE
# =========================
if "run" not in st.session_state:
    st.session_state.run = False

# =========================
# INPUT (SIDEBAR)
# =========================
with st.sidebar:
    st.header("⚙️ Input Parameter")

    debit = st.slider("Debit (m³/s)", 0.01, 0.20, 0.05, step=0.01)
    head = st.number_input("Head (m)", 1.0, 50.0, 10.0, step=1.0)
    efisiensi = st.slider("Efisiensi (%)", 10, 100, 75)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("▶️ Jalankan", use_container_width=True):
            st.session_state.run = True
    with col_btn2:
        if st.button("⏹️ Stop", use_container_width=True):
            st.session_state.run = False

# =========================
# PERHITUNGAN
# =========================
rho = 1000
g = 9.81
eta = efisiensi / 100
daya = (rho * g * debit * head) / eta / 1000

# =========================
# LAYOUT UTAMA
# =========================
col1, col2 = st.columns([1.8, 1.2])

# =========================
# COL 1: ANIMASI REALISTIS (HTML5 CANVAS)
# =========================
with col1:
    st.subheader("🔄 Visualisasi Aliran Fluida")
    
    # Menentukan status dan kecepatan animasi berdasarkan state
    is_running = "true" if st.session_state.run else "false"
    # Kecepatan partikel proporsional terhadap debit
    base_speed = debit * 80 

    # Inject HTML & JavaScript Canvas untuk animasi pompa & partikel air yang halus
    canvas_html = f"""
    <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #e0e0e0; text-align: center;">
        <div style="text-align: left; margin-bottom: 10px; font-weight: bold; color: #333;">
            Status: <span style="color: {'#2ecc71' if st.session_state.run else '#e74c3c'};">
                {'● BERJALAN' if st.session_state.run else '● BERHENTI'}
            </span>
        </div>
        <canvas id="pumpCanvas" width="600" height="400" style="background:#f9fbfd; border-radius: 8px;"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('pumpCanvas');
        const ctx = canvas.getContext('2d');
        
        const isRunning = {is_running};
        const speed = {base_speed};
        let angle = 0;

        // Inisialisasi partikel air (posisi x, posisi y, ukuran, kecepatan individual)
        let inletParticles = [];
        let outletParticles = [];
        
        for(let i=0; i<30; i++) {{
            inletParticles.push({{ x: Math.random() * 230, y: 230 + (Math.random() * 30 - 15), r: Math.random() * 3 + 2 }});
            outletParticles.push({{ x: 300 + (Math.random() * 30 - 15), y: 170 - (Math.random() * 170), r: Math.random() * 3 + 2 }});
        }}

        function drawPumpStructure() {{
            // 1. Gambar Pipa Horizontal (Inlet Transparan)
            ctx.fillStyle = "rgba(41, 128, 185, 0.15)";
            ctx.fillRect(0, 210, 240, 40);
            ctx.strokeStyle = "#7f8c8d";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 210); ctx.lineTo(240, 210);
            ctx.moveTo(0, 250); ctx.lineTo(230, 250);
            ctx.stroke();

            // 2. Gambar Pipa Vertikal (Outlet Transparan)
            ctx.fillStyle = "rgba(41, 128, 185, 0.15)";
            ctx.fillRect(285, 0, 40, 160);
            ctx.beginPath();
            ctx.moveTo(285, 0); ctx.lineTo(285, 160);
            ctx.moveTo(325, 0); ctx.lineTo(325, 135);
            ctx.stroke();
            
            // Flensa Sambungan Pipa
            ctx.fillStyle = "#bdc3c7";
            ctx.fillRect(225, 205, 15, 50);
            ctx.fillRect(280, 145, 50, 15);

            // 3. Badan Pompa Snail Shell (Volute Casing) - Biru Metalik
            ctx.save();
            ctx.shadowBlur = 10;
            ctx.shadowColor = "rgba(0,0,0,0.2)";
            ctx.fillStyle = "#1f4e79"; 
            ctx.beginPath();
            ctx.arc(300, 230, 65, 0, Math.PI * 2);
            ctx.fill();
            ctx.lineWidth = 4;
            ctx.strokeStyle = "#153654";
            ctx.stroke();
            
            // Motor Listrik di Belakang Pompa
            ctx.fillStyle = "#2c3e50";
            ctx.fillRect(360, 190, 90, 80);
            // Sirip-sirip heatsink motor
            ctx.fillStyle = "#34495e";
            for(let m=0; m<5; m++) {{
                ctx.fillRect(370 + (m*15), 180, 8, 10);
                ctx.fillRect(370 + (m*15), 270, 8, 10);
            }}
            ctx.restore();

            // 4. Pusat Impeller
            ctx.fillStyle = "#ecf0f1";
            ctx.beginPath();
            ctx.arc(300, 230, 45, 0, Math.PI * 2);
            ctx.fill();
        }}

        function drawImpellerBlades(currentAngle) {{
            ctx.save();
            ctx.translate(300, 230);
            ctx.rotate(currentAngle);
            ctx.strokeStyle = "#7f8c8d";
            ctx.lineWidth = 5;
            ctx.lineCap = "round";
            
            // Menggambar bilah melengkung (Impeller Vanes)
            for (let i = 0; i < 6; i++) {{
                ctx.rotate((Math.PI * 2) / 6);
                ctx.beginPath();
                ctx.quadraticCurveTo(0, 0, 20, 30);
                ctx.stroke();
            }}
            
            // Poros Tengah
            ctx.fillStyle = "#2c3e50";
            ctx.beginPath();
            ctx.arc(0, 0, 10, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }}

        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Update Logika Animasi Jika Status RUN
            if (isRunning) {{
                angle += (speed * 0.05);
            }}

            // Tampilkan struktur dasar dan motor pompa
            drawPumpStructure();

            // Menggambar Aliran Partikel Air di Inlet
            ctx.fillStyle = "#3498db";
            inletParticles.forEach(p => {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
                if (isRunning) {{
                    p.x += speed * 0.5 + 0.5;
                    if (p.x > 250) p.x = 0; // Reset balik ke kiri pipa
                }}
            }});

            // Menggambar Impeller yang Berputar
            drawImpellerBlades(angle);

            // Menggambar Aliran Partikel Air di Outlet
            ctx.fillStyle = "#2980b9";
            outletParticles.forEach(p => {{
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
                if (isRunning) {{
                    p.y -= speed * 0.7 + 0.5;
                    if (p.y < 0) p.y = 150; // Reset balik ke leher pompa
                }}
            }});

            // Efek Air Pusaran di dalam Casing Pompa (Transparan)
            if (isRunning) {{
                ctx.fillStyle = "rgba(52, 152, 219, 0.4)";
                ctx.beginPath();
                ctx.arc(300, 230, 40, angle, angle + 1);
                ctx.lineWidth = 4;
                ctx.strokeStyle = "rgba(255,255,255,0.6)";
                ctx.stroke();
            }}

            requestAnimationFrame(animate);
        }}

        animate();
    </script>
    """
    st.components.v1.html(canvas_html, height=460)

# =========================
# COL 2: OUTPUT METRIC
# =========================
with col2:
    st.subheader("⚡ Output")
    
    st.metric(label="Daya Pompa Aktual", value=f"{daya:.2f} kW")
    
    if daya > 20:
        st.error("⚠️ Status: Daya terlalu Tinggi! Periksa kembali debit/head.")
    else:
        st.success("✅ Status: Daya dalam batas Normal")

    st.write("### 📝 Rincian Parameter:")
    st.info(f"""
    *   **Debit Aliran ($Q$):** {debit} $m^3/s$
    *   **Total Head ($H$):** {head} $m$
    *   **Efisiensi Alat ($\eta$):** {efisiensi}%
    *   **Konstanta Fluida:** $\rho = 1000\ kg/m^3$
    """)

# =========================
# GRAFIK KURVA KINERJA POMPA
# =========================
st.markdown("---")
st.subheader("📊 Grafik Karakteristik Daya vs Debit")

# Generate data kurva parabola yang lebih realistis
q_range = np.linspace(0.01, 0.25, 100)
p_range = (rho * g * q_range * head) / eta / 1000

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(q_range, p_range, color='#1f4e79', linewidth=2.5, label='Kurva Kebutuhan Daya')
ax.scatter(debit, daya, color='#e74c3c', s=120, zorder=5, label='Titik Kerja Saat Ini')

# Garis bantu penunjuk titik (Dotted Lines)
ax.axhline(daya, color='gray', linestyle='--', linewidth=1)
ax.axvline(debit, color='gray', linestyle='--', linewidth=1)

# Estetika Grafik
ax.set_xlabel("Debit Aliran (m³/s)", fontsize=10)
ax.set_ylabel("Kebutuhan Daya (kW)", fontsize=10)
ax.setTitle(f"Kurva Sistem pada Head {head} meter", fontsize=11, fontweight='bold')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='upper left')

st.pyplot(fig)
