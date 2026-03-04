import streamlit as st
import os
import time
import random
from dotenv import load_dotenv
from google import genai
import base64

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="FitGuard AI", page_icon="💪", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #0a0a0a;
    --surface: #111111;
    --surface2: #1a1a1a;
    --accent: #ff4500;
    --accent2: #ff6b35;
    --text: #f0f0f0;
    --muted: #666666;
    --success: #00d084;
    --border: #222222;
}

* { font-family: 'DM Sans', sans-serif !important; }
.stApp { background: var(--bg) !important; color: var(--text) !important; }
.stApp > header { background: transparent !important; }
section[data-testid="stSidebar"] { display: none; }
h1, h2, h3 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 2px !important; }

.hero {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0800 50%, #0a0a0a 100%);
    border: 1px solid #1f1f1f;
    border-radius: 16px;
    padding: 48px 40px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,69,0,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title { font-family: 'Bebas Neue', sans-serif !important; font-size: 64px !important; line-height: 1 !important; color: #ffffff !important; margin: 0 !important; letter-spacing: 4px; }
.hero-title span { color: var(--accent); }
.hero-sub { color: var(--muted); font-size: 16px; margin-top: 8px; font-weight: 300; letter-spacing: 3px; text-transform: uppercase; }

.section-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 32px; margin-bottom: 24px; }
.section-title { font-family: 'Bebas Neue', sans-serif !important; font-size: 28px !important; letter-spacing: 3px !important; color: var(--text) !important; margin-bottom: 4px !important; }
.accent-bar { width: 40px; height: 3px; background: var(--accent); border-radius: 2px; margin-bottom: 24px; }

.bet-step { background: var(--surface2); border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 8px; padding: 20px 24px; margin: 16px 0; }
.bet-number { font-family: 'Bebas Neue', sans-serif !important; font-size: 48px; color: var(--accent); opacity: 0.3; line-height: 1; }

.timer-display { background: var(--surface2); border: 2px solid var(--accent); border-radius: 12px; padding: 16px; text-align: center; margin: 12px 0; }
.timer-value { font-family: 'Bebas Neue', sans-serif !important; font-size: 56px; color: var(--accent); line-height: 1; }
.timer-label { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 2px; }

.hz-display { background: linear-gradient(135deg, #1a0800, #0a0a0a); border: 1px solid var(--accent); border-radius: 12px; padding: 24px; text-align: center; margin: 16px 0; }
.hz-value { font-family: 'Bebas Neue', sans-serif !important; font-size: 72px; color: var(--accent); line-height: 1; }
.hz-label { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 3px; }

.stButton > button { background: var(--accent) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; letter-spacing: 1px !important; text-transform: uppercase !important; padding: 12px 28px !important; transition: all 0.2s !important; font-size: 13px !important; }
.stButton > button:hover { background: var(--accent2) !important; transform: translateY(-1px) !important; box-shadow: 0 8px 24px rgba(255,69,0,0.3) !important; }

.stSelectbox > div > div, .stTextArea > div > div > textarea, .stNumberInput > div > div > input { background: var(--surface2) !important; border: 1px solid var(--border) !important; color: var(--text) !important; border-radius: 8px !important; }
.stSlider > div > div > div { background: var(--accent) !important; }

.stTabs [data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: 10px !important; padding: 4px !important; gap: 4px !important; border: 1px solid var(--border) !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--muted) !important; border-radius: 8px !important; font-weight: 600 !important; letter-spacing: 1px !important; text-transform: uppercase !important; font-size: 12px !important; }
.stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }

div[data-testid="metric-container"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 16px !important; }
div[data-testid="metric-container"] label { color: var(--muted) !important; text-transform: uppercase !important; letter-spacing: 2px !important; font-size: 11px !important; }
div[data-testid="metric-container"] div[data-testid="metric-value"] { color: var(--accent) !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 36px !important; }

.tag { display: inline-block; background: rgba(255,69,0,0.15); color: var(--accent); border: 1px solid rgba(255,69,0,0.3); border-radius: 20px; padding: 4px 12px; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-right: 8px; }
.divider { height: 1px; background: var(--border); margin: 32px 0; }
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-title">FIT<span>GUARD</span> AI</div>
    <div class="hero-sub">Tu guardian virtual de entrenamiento · Powered by Gemini</div>
    <br>
    <span class="tag">🧠 Brain Endurance Training</span>
    <span class="tag">📹 Vision AI</span>
    <span class="tag">🎙️ Live Voice</span>
</div>
""", unsafe_allow_html=True)

# Session state init
for key, val in [("bet_step", 0), ("bet_score", 0), ("bet_complete", False), 
                  ("bet_start_time", None), ("bet_seq", None), ("bet_ops", None), ("bet_pattern", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

tab1, tab2, tab3 = st.tabs(["⚡ Pre-Entreno", "🏋️ Durante", "🌙 Post-Entreno"])

with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Estado Mental</div><div class="accent-bar"></div>', unsafe_allow_html=True)
        humor = st.selectbox("Nivel de energía", ["Alta", "Normal", "Baja", "Estresado"])
        horas_sueno = st.slider("Horas de sueño", 0, 12, 7)
        estado_libre = st.text_area("¿Algo más?", placeholder="Ej: Tuve un día difícil...")
        if st.button("⚡ Analizar y generar plan"):
            with st.spinner("FitGuard AI analizando..."):
                prompt = f"Sos FitGuard AI, coach de fitness de élite. El usuario tiene energía {humor}, durmió {horas_sueno} horas. Comentario: {estado_libre}. Dame: 1) Análisis de estado, 2) Tipo de entrenamiento recomendado, 3) Micro-tarea cognitiva BET, 4) Frase motivadora. En español, amigable y conciso."
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.success("✅ Plan generado")
                st.markdown(response.text)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Protocolo BET</div><div class="accent-bar"></div>', unsafe_allow_html=True)
        st.write("Elevá tu frecuencia cerebral al nivel óptimo para entrenar.")

        if st.button("🚀 Iniciar Protocolo BET", disabled=st.session_state.bet_complete):
            st.session_state.bet_step = 1
            st.session_state.bet_score = 0
            st.session_state.bet_complete = False
            st.session_state.bet_start_time = time.time()
            st.session_state.bet_seq = random.choice(["7-3-9-1", "4-8-2-6", "5-1-7-3", "9-2-4-8"])
            st.session_state.bet_ops = [
                (random.randint(10,50), random.randint(10,50), "+"),
                (random.randint(20,99), random.randint(1,19), "-"),
                (random.randint(2,9), random.randint(2,9), "x"),
            ]
            nums = list(range(1, 6))
            random.shuffle(nums)
            st.session_state.bet_pattern = nums
            st.rerun()

        # PASO 1 — Memoria de trabajo con timer
        if st.session_state.bet_step == 1:
            elapsed = int(time.time() - st.session_state.bet_start_time) if st.session_state.bet_start_time else 0
            remaining = max(0, 30 - elapsed)
            st.markdown('<div class="bet-step">', unsafe_allow_html=True)
            st.markdown('<div class="bet-number">01</div>', unsafe_allow_html=True)
            st.markdown("**Memoria de Trabajo** — Invertí la secuencia")
            st.info(f"Secuencia: **{st.session_state.bet_seq}**")
            st.markdown(f'<div class="timer-display"><div class="timer-value">{remaining}s</div><div class="timer-label">Tiempo restante</div></div>', unsafe_allow_html=True)
            respuesta = st.text_input("Escribí al revés:", key="r1")
            if st.button("Confirmar →", key="c1"):
                inversa = "-".join(st.session_state.bet_seq.split("-")[::-1])
                tiempo_usado = int(time.time() - st.session_state.bet_start_time)
                if respuesta.strip() == inversa:
                    pts = 2 if tiempo_usado <= 15 else 1
                    st.success(f"✅ Correcto en {tiempo_usado}s — +{pts} pts")
                    st.session_state.bet_score += pts
                else:
                    st.warning(f"Era: {inversa}")
                st.session_state.bet_step = 2
                st.session_state.bet_start_time = time.time()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # PASO 2 — Cálculo mental con timer
        if st.session_state.bet_step == 2:
            elapsed = int(time.time() - st.session_state.bet_start_time) if st.session_state.bet_start_time else 0
            remaining = max(0, 45 - elapsed)
            st.markdown('<div class="bet-step">', unsafe_allow_html=True)
            st.markdown('<div class="bet-number">02</div>', unsafe_allow_html=True)
            st.markdown("**Cálculo Mental** — Velocidad + precisión")
            st.markdown(f'<div class="timer-display"><div class="timer-value">{remaining}s</div><div class="timer-label">Tiempo restante</div></div>', unsafe_allow_html=True)
            correctos = 0
            for i, (a, b, op) in enumerate(st.session_state.bet_ops):
                correcto = a+b if op=="+" else a-b if op=="-" else a*b
                r = st.number_input(f"{a} {op} {b} =", key=f"op_{i}", step=1, value=0)
                if r == correcto:
                    correctos += 1
            if st.button("Confirmar →", key="c2"):
                tiempo_usado = int(time.time() - st.session_state.bet_start_time)
                pts = correctos + (1 if tiempo_usado <= 20 else 0)
                st.session_state.bet_score += min(pts, 3)
                st.session_state.bet_step = 3
                st.session_state.bet_start_time = time.time()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # PASO 3 — Patrón visual con timer
        if st.session_state.bet_step == 3:
            elapsed = int(time.time() - st.session_state.bet_start_time) if st.session_state.bet_start_time else 0
            remaining = max(0, 30 - elapsed)
            st.markdown('<div class="bet-step">', unsafe_allow_html=True)
            st.markdown('<div class="bet-number">03</div>', unsafe_allow_html=True)
            st.markdown("**Patrón Visual** — Encontrá la secuencia correcta")
            patron = st.session_state.bet_pattern
            siguiente = (patron[-1] % 5) + 1
            st.info(f"Patrón: **{' → '.join(map(str, patron))} → ?**")
            opciones = list(set(range(1, 7)) - {patron[-1]})
            random.shuffle(opciones)
            opciones = opciones[:3] + [siguiente]
            random.shuffle(opciones)
            st.markdown(f'<div class="timer-display"><div class="timer-value">{remaining}s</div><div class="timer-label">Tiempo restante</div></div>', unsafe_allow_html=True)
            resp = st.radio("¿Cuál sigue?", opciones, key="patron_resp", horizontal=True)
            if st.button("Confirmar →", key="c3"):
                tiempo_usado = int(time.time() - st.session_state.bet_start_time)
                if resp == siguiente:
                    pts = 2 if tiempo_usado <= 15 else 1
                    st.success(f"✅ Correcto — +{pts} pts")
                    st.session_state.bet_score += pts
                else:
                    st.warning(f"Era: {siguiente}")
                st.session_state.bet_step = 4
                st.session_state.bet_start_time = time.time()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # PASO 4 — Respiración
        if st.session_state.bet_step == 4:
            st.markdown('<div class="bet-step">', unsafe_allow_html=True)
            st.markdown('<div class="bet-number">04</div>', unsafe_allow_html=True)
            st.markdown("**Respiración Neural** — Sincronizá tu cerebro")
            st.info("Inhala 4s → Retené 4s → Exhalá 4s · Repetí 3 veces")
            if st.button("✅ Completé la respiración", key="c4"):
                st.session_state.bet_score += 2
                st.session_state.bet_step = 5
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # RESULTADO FINAL
        if st.session_state.bet_step == 5:
            score = st.session_state.bet_score
            st.session_state.bet_complete = True
            hz = "48-52 Hz" if score >= 6 else "35-45 Hz" if score >= 3 else "20-30 Hz"
            nivel = "ÓPTIMO 🟢" if score >= 6 else "ACTIVADO 🟡" if score >= 3 else "EN CALENTAMIENTO 🔴"
            st.markdown(f'<div class="hz-display"><div class="hz-value">{hz.split("-")[0]}</div><div class="hz-label">Hz estimados · Estado: {nivel} · Score: {score}/9</div></div>', unsafe_allow_html=True)
            with st.spinner("Analizando activación cerebral..."):
                prompt = f"Atleta completó protocolo BET con puntuación {score}/9. Estado: {nivel}. Frecuencia: {hz}. Evaluación cognitiva breve y recomendación de entrenamiento basada en neurociencia. Español, motivador, conciso."
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.markdown(response.text)
            if st.button("🔄 Reiniciar BET"):
                st.session_state.bet_step = 0
                st.session_state.bet_score = 0
                st.session_state.bet_complete = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Análisis de Postura</div><div class="accent-bar"></div>', unsafe_allow_html=True)
        ejercicio = st.selectbox("Ejercicio", ["Sentadilla", "Peso muerto", "Plancha", "Flexiones", "Estocada", "Otro"])
        foto = st.camera_input("📸 Capturá tu postura")
        if foto is not None:
            st.image(foto, width=300)
            if st.button("🔍 Analizar postura"):
                with st.spinner("Vision AI analizando forma..."):
                    img_b64 = base64.b64encode(foto.getvalue()).decode()
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[{"role": "user", "parts": [
                            {"text": f"Sos FitGuard AI, experto en biomecánica. Analizá postura en {ejercicio}. Dame: 1) Lo que está bien, 2) Errores y riesgos, 3) Correcciones específicas, 4) Puntuación /10. Español, conciso."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                        ]}]
                    )
                    st.success("✅ Análisis completado")
                    st.markdown(response.text)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">BET Entre Sets</div><div class="accent-bar"></div>', unsafe_allow_html=True)
        st.write("Micro-tarea cognitiva durante el descanso para mantener 50Hz.")
        if st.button("🎯 Nueva micro-tarea"):
            tareas = [
                "Contá hacia atrás de 100 de a 7: 100, 93, 86...",
                "Nombrá 5 animales con la misma letra que tu nombre",
                "Visualizá tu próximo set perfecto — 30 segundos",
                "Respiración: inhala 4s, retené 4s, exhalá 4s — 3 veces",
                "Mental: 17 × 6 = ?",
                "Recordá los últimos 5 ejercicios en orden",
                "Deletreá tu apellido al revés",
                "Sumá todos los números del 1 al 10",
            ]
            st.markdown(f'<div class="bet-step"><strong>Micro-tarea:</strong><br><br>{random.choice(tareas)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Voice Coach</div><div class="accent-bar"></div>', unsafe_allow_html=True)
        st.info("🎙️ Para activar el coach de voz en tiempo real, ejecutá en tu terminal:\n\n`python voice_agent.py`")
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recuperación Holística</div><div class="accent-bar"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        duracion = st.slider("Duración (min)", 0, 120, 45)
    with col2:
        intensidad = st.selectbox("Intensidad", ["Suave", "Moderada", "Intensa", "Extrema"])
    with col3:
        dolor = st.multiselect("Zona de dolor", ["Ninguna", "Piernas", "Espalda", "Hombros", "Rodillas", "Cuello"])

    notas = st.text_area("¿Cómo te sentís?", placeholder="Ej: Cansado pero bien...")

    if st.button("🌙 Generar plan de recuperación"):
        with st.spinner("Analizando entrenamiento..."):
            prompt = f"FitGuard AI coach de recuperación. Entrenó {duracion} min, intensidad {intensidad}, dolor en {dolor}. Estado: {notas}. Dame: 1) Análisis, 2) Estiramientos, 3) Nutrición, 4) Descanso, 5) BET para mañana. Español, conciso."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.success("✅ Plan de recuperación listo")
            st.markdown(response.text)
    st.markdown('</div>', unsafe_allow_html=True)