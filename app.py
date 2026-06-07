import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# =========================
# CONFIG & THEME (CYBER BLUE)
# =========================
st.set_page_config(page_title="Simulasi Pompa Air Pro", layout="wide")

# Custom CSS untuk memperbaiki kontras elemen input, tombol, dan card analisis
st.markdown("""
    <style>
    /* Mengubah background aplikasi utama */
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #0f3460 100%);
        color: #e2e8f0;
    }
    
    .block-container { padding-top: 1.5rem; }
    
    /* FIX: Kotak Input Parameter Sistem - Latar Putih, Teks Hitam Tegas */
    .stNumberInput div[data-baseweb="input"] { 
        border-radius: 8px; 
        background-color: #ffffff !important; 
        border: 2px solid #00f2fe !important; 
    }
    .stNumberInput input {
        color: #000000 !important; 
        font-weight: bold !important;
        font-size: 1.05rem !important;
    }
    
    /* Tombol plus minus bawaan di sisi kotak input */
    .stNumberInput button {
        background-color: #e2e8f0 !important;
        color: #000000 !important;
    }
    
    /* FIX: Desain Tombol Jalankan & Stop agar Kontras dan Jelas */
    .stButton button {
        background-color: #e2e8f0 !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 2px solid #00f2fe !important;
        box-shadow: 0 4px 10px rgba(0, 242, 254, 0.2);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #00f2fe !important;
        color: #0a192f !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.6);
    }
    
    label[data-testid="stWidgetLabel"] {
        color: #00f2fe !important;
        font-weight: 600;
    }
    
    /* Judul Subheader */
    h2, h3 {
        color: #00f2fe !important;
        font-weight: 700;
    }
    
    /* Card Hasil Analisis Mewah Transparan */
    .analysis-card {
        background: rgba(22, 33, 62, 0.7);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        margin-bottom: 15px;
    }
    .parameter-text {
        font-size: 0.95rem;
        color: #81e6d9;
        margin-bottom: 6px;
    }
    
    /* Modifikasi teks Metrik agar menyala */
    div[data-testid="stMetricValue"] { 
        font-size: 2.2rem; 
        font-weight: 700; 
        color: #00f2fe !important;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.title("💧 Simulasi Daya Pompa Air Interaktif")
st.write("Visualisasi aliran fluida dengan antarmuka industrial siber")

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
# KOLOM KIRI: INPUT & ANALISIS PLACEHOLDER
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
    
    # Nilai konstanta fisik
    rho = 1000  
    g = 9.81    
    eta = efisiensi / 100
    
    daya_hidrolis_maks = (rho * g * debit * head) / 1000  
    daya_aktual_maks = daya_hidrolis_maks / eta  
    
    # Elemen kontainer dinamis kosong untuk diisi oleh pergerakan angka berjalan
    metric_placeholder = st.empty()

# =========================
# KOLOM KANAN: ANIMASI CANVAS
# =========================
with col_display:
    st.subheader("🔄 Visualisasi Aliran & Konstruksi Realistis")
    
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("▶️ Jalankan", use_container_width=True):
            st.session_state.run = True
    with c2:
        if st.button("⏹️ Stop", use_container_width=True):
            st.session_state.run = False
            
    is_running = "true" if st.session_state.run else "false"
    base_speed = float(np.clip(debit * 100, 1, 25))
    status_text = "● AKTIF (PUMPING)" if st.session_state.run else "● SIAGA"
    status_color = "#2ecc71" if st.session_state.run else "#e74c3c"

    # HTML Modul Canvas Pompa Aman (Tanpa f-string langsung pada JS brackets)
    canvas_html = """
    <div style="background: #111a2e; padding: 10px; border-radius: 12px; border: 2px solid #00f2fe; text-align: center; box-shadow: 0 0 15px rgba(0,242,254,0.3);">
        <div style="text-align: left; margin-bottom: 8px; font-weight: bold; font-family: sans-serif; font-size: 14px; color: #00f2fe;">
            Kondisi Mesin: <span id="statusLabel" style="text-shadow: 0 0 8px;"></span>
        </div>
        <canvas id="pumpCanvas" width="650" height="300" style="background:#070d19; border-radius: 8px;"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('pumpCanvas');
        const ctx = canvas.getContext('2d');
        
        const isRunning = P_IS_RUNNING;
        const speed = P_SPEED;
        
        document.getElementById('statusLabel').innerText = "P_STATUS_TEXT";
        document.getElementById('statusLabel').style.color = "P_STATUS_COLOR";
        
        let angle = 0;
        let particles = [];
        
        for(let i=0; i<45; i++) {
            particles.push({
                stage: Math.random() > 0.5 ? 'inlet' : 'outlet',
                x: Math.random() * 240,
                y: 135 + (Math.random() * 24 + 3),
                r: Math.random() * 2.5 + 1.5,
                alpha: Math.random() * 0.5 + 0.5
            });
        }
        
        particles.forEach(p => {
            if(p.stage === 'outlet') {
                p.x = 295 + (Math.random() * 24 + 3);
                p.y = Math.random() * 90;
            }
        });

        function drawRealisticPump() {
            let pipeGlow = ctx.createLinearGradient(0, 135, 0, 165);
            pipeGlow.addColorStop(0, "rgba(0, 242, 254, 0.1)");
            pipeGlow.addColorStop(0.5, "rgba(0, 242, 254, 0.3)");
            pipeGlow.addColorStop(1, "rgba(0, 242, 254, 0.1)");
            
            ctx.fillStyle = pipeGlow;
            ctx.fillRect(0, 135, 250, 30);
            ctx.fillRect(295, 0, 30, 90);
            
            ctx.strokeStyle = "#4e6e8e"; ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, 135); ctx.lineTo(250, 135); ctx.moveTo(0, 165); ctx.lineTo(238, 165);
            ctx.moveTo(295, 0); ctx.lineTo(295, 90); ctx.moveTo(325, 0); ctx.lineTo(325, 70);
            ctx.stroke();

            let motorGrad = ctx.createLinearGradient(360, 110, 460, 110);
            motorGrad.addColorStop(0, "#1f2d3d");
            motorGrad.addColorStop(0.5, "#3a506b");
            motorGrad.addColorStop(1, "#111a24");
            ctx.fillStyle = motorGrad;
            ctx.fillRect(360, 110, 100, 80);
            
            ctx.fillStyle = "#0b132b";
            for(let m=0; m<7; m++) {
                ctx.fillRect(368 + (m*13), 102, 6, 8); 
                ctx.fillRect(368 + (m*13), 190, 6, 8);
            }

            let voluteGrad = ctx.createRadialGradient(310, 150, 10, 310, 150, 60);
            voluteGrad.addColorStop(0, "#1f4068");
            voluteGrad.addColorStop(0.8, "#162447");
            voluteGrad.addColorStop(1, "#0f1a30");
            
            ctx.fillStyle = voluteGrad;
            ctx.shadowBlur = 15; ctx.shadowColor = "rgba(0, 242, 254, 0.4)";
            ctx.beginPath(); ctx.arc(310, 150, 60, 0, Math.PI * 2); ctx.fill();
            ctx.shadowBlur = 0;
            
            ctx.strokeStyle = "#00f2fe"; ctx.lineWidth = 1.5; ctx.stroke();

            ctx.fillStyle = "rgba(10, 25, 47, 0.75)";
            ctx.beginPath(); ctx.arc(310, 150, 40, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = "rgba(0, 242, 254, 0.4)"; ctx.stroke();
        }

        function drawImpeller(rotAngle) {
            ctx.save(); ctx.translate(310, 150); ctx.rotate(rotAngle);
            ctx.strokeStyle = "#ffb703"; ctx.lineWidth = 4;
            ctx.shadowBlur = isRunning ? 8 : 0; ctx.shadowColor = "#ffb703";
            
            for (let i = 0; i < 6; i++) {
                ctx.rotate((Math.PI * 2) / 6); 
                ctx.beginPath(); 
                ctx.quadraticCurveTo(0, 0, 12, 28); 
                ctx.stroke();
            }
            
            let shaftGrad = ctx.createRadialGradient(0,0,2,0,0,8);
            shaftGrad.addColorStop(0, "#ffffff");
            shaftGrad.addColorStop(1, "#4a5568");
            ctx.fillStyle = shaftGrad; ctx.shadowBlur = 0;
            ctx.beginPath(); ctx.arc(0, 0, 8, 0, Math.PI * 2); ctx.fill();
            ctx.restore();
        }

        function loop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (isRunning) angle += (speed * 0.05);
            
            drawRealisticPump();

            particles.forEach(p => {
                ctx.save();
                ctx.fillStyle = "rgba(0, 242, 254, " + p.alpha + ")";
                ctx.shadowBlur = 6;
                ctx.shadowColor = "#00f2fe";
                ctx.beginPath(); 
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); 
                ctx.fill();
                ctx.restore();

                if (isRunning) {
                    if (p.stage === 'inlet') {
                        p.x += speed * 0.4 + 0.5;
                        if (p.x > 250) {
                            p.stage = 'outlet'; p.x = 295 + (Math.random() * 24); p.y = 90;
                        }
                    } else if (p.stage === 'outlet') {
                        p.y -= speed * 0.5 + 0.5;
                        if (p.y < 0) {
                            p.stage = 'inlet'; p.x = 0; p.y = 135 + (Math.random() * 24);
                        }
                    }
                }
            });

            drawImpeller(angle);
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """.replace("P_IS_RUNNING", is_running).replace("P_SPEED", str(base_speed)).replace("P_STATUS_TEXT", status_text).replace("P_STATUS_COLOR", status_color)
    
    st.components.v1.html(canvas_html, height=340)

    # ==========================================
    # LOGIKA GERAKAN GRAFIK & ANGKA BERJALAN
    # ==========================================
    st.markdown("---")
    st.subheader("📊 Kurva Karakteristik Operasional Pompa (Live)")
    
    chart_placeholder = st.empty()

    q_curve = np.linspace(0.001, max(0.250, debit * 1.5), 100)
    p_curve = (rho * g * q_curve * head) / eta / 1000

    plt.style.use('dark_background')

    # Fungsi untuk merender komponen analisis di kolom kiri secara berulang (efek animasi berjalan)
    def render_analysis_card(curr_aktual, curr_hidrolis):
        with metric_placeholder.container():
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.metric(
                label="🔋 Kebutuhan Daya Aktual (P_input)", 
                value=f"{curr_aktual:.2f} kW",
                delta=f"Daya Air: {curr_hidrolis:.2f} kW"
            )
            st.markdown(f'<div class="parameter-text">⚡ <b>Efisiensi Mekanis:</b> {efisiensi}%</div>', unsafe_allow_html=True)
            st.progress(efisiensi / 100)
            
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            st.write(f"🔹 **Massa Jenis Fluida ($\\rho$):** {rho} $kg/m^3$")
            st.write(f"🔹 **Laju Volume ($Q$):** {debit:.3f} $m^3/s$")
            st.write(f"🔹 **Tinggi Tekan ($H$):** {head:.1f} $m$")
            st.markdown("---")
            st.markdown("**Formulasi Dasar:**")
            st.latex(r"P_{aktual} = \frac{\rho \cdot g \cdot Q \cdot H}{\eta \cdot 1000}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Keterangan Analisis Singkat Otomatis di Bagian Bawah Card
            if curr_aktual > 30:
                st.error("🚨 **ANALISIS STATUS: CRITICAL OVERLOAD**\nKombinasi debit dan head terlalu ekstrem bagi efisiensi sistem. Risiko motor terbakar sangat tinggi.")
            elif curr_aktual > 15:
                st.warning("⚠️ **ANALISIS STATUS: HEAVY DUTY**\nSistem beroperasi pada beban kerja tinggi. Memerlukan sistem pendingin heatsink tambahan.")
            else:
                st.success("✅ **ANALISIS STATUS: NORMAL OPERATION**\nKonsumsi daya berada di batas aman regulasi standar pabrik industri.")

    # JIKA SIMULASI SEDANG BERJALAN
    if st.session_state.run:
        for step in range(1, 31):
            if not st.session_state.run:
                break
                
            # Menghitung nilai berjalan interpolatif (0 menuju batas atas input)
            current_q = (debit / 30) * step
            current_hidrolis = (rho * g * current_q * head) / 1000
            current_aktual = current_hidrolis / eta

            # 1. Update Angka Daya yang Berjalan di Kiri
            render_analysis_card(current_aktual, current_hidrolis)

            # 2. Update Grafik Lintasan Pertumbuhan di Kanan
            fig, ax = plt.subplots(figsize=(11, 3.5))
            fig.patch.set_facecolor('#0a192f')
            ax.set_facecolor('#070d19')

            ax.plot(q_curve, p_curve, color='#00f2fe', linewidth=2, alpha=0.3, label='Kurva Karakteristik')
            
            q_track = np.linspace(0.001, current_q, step)
            p_track = (rho * g * q_track * head) / eta / 1000
            ax.plot(q_track, p_track, color='#ffb703', linewidth=3, label='Pertumbuhan Daya')
            
            ax.scatter(current_q, current_aktual, color='#ff007f', s=130, zorder=5)
            ax.axhline(current_aktual, color='cyan', linestyle=':', alpha=0.3)
            ax.axvline(current_q, color='cyan', linestyle=':', alpha=0.3)

            ax.set_xlabel("Debit Fluida Q (m³/s)", fontsize=9, color='#81e6d9')
            ax.set_ylabel("Daya Mekanis P (kW)", fontsize=9, color='#81e6d9')
            ax.set_xlim(0, max(0.250, debit * 1.3))
            ax.set_ylim(0, max(p_curve) * 1.1)
            ax.grid(True, linestyle='--', alpha=0.1)
            
            chart_placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.04)

    # JIKA KONDISI DIAM / STOP
    if not st.session_state.run:
        # Kunci card analisis di angka maksimal target input
        render_analysis_card(daya_aktual_maks, daya_hidrolis_maks)
        
        # Kunci grafik stasioner tunggal beserta legenda penjelas
        fig, ax = plt.subplots(figsize=(11, 3.5))
        fig.patch.set_facecolor('#0a192f')
        ax.set_facecolor('#070d19')

        ax.plot(q_curve, p_curve, color='#00f2fe', linewidth=2.5, label='Kurva Karakteristik Daya')
        ax.scatter(debit, daya_aktual_maks, color='#ff007f', s=140, zorder=5, label='Titik Operasional Kerja')
        
        ax.axhline(daya_aktual_maks, color='cyan', linestyle=':', alpha=0.4)
        ax.axvline(debit, color='cyan', linestyle=':', alpha=0.4)
        
        ax.set_xlabel("Debit Fluida Q (m³/s)", fontsize=9, color='#81e6d9')
        ax.set_ylabel("Daya Mekanis P (kW)", fontsize=9, color='#81e6d9')
        ax.grid(True, linestyle='--', alpha=0.1)
        ax.legend(loc='upper left', fontsize=9)
        
        chart_placeholder.pyplot(fig)
        plt.close(fig)
