import streamlit as st
import os
import time
import random
from datetime import datetime, date
from dotenv import load_dotenv
from google import genai
import base64
import re

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ── OPEN WEARABLES INTEGRATION ─────────────────────────────────────────────
# Para conectar con Open Wearables real, reemplazá esta función por:
#   import requests
#   def get_wearable_data():
#       r = requests.get("http://localhost:8000/api/v1/health/summary", headers={"X-API-Key": OW_API_KEY})
#       return r.json()

def get_wearable_data():
    """Simula respuesta de Open Wearables API. Reemplazar con llamada real cuando esté disponible."""
    seed = datetime.now().day  # mismo valor todo el día, cambia mañana
    rng = random.Random(seed)
    hrv = rng.randint(42, 95)
    rhr = rng.randint(48, 72)
    sueño_profundo = round(rng.uniform(0.8, 2.8), 1)
    sueño_total = round(rng.uniform(5.5, 8.5), 1)
    pasos = rng.randint(2000, 14000)
    calorias = rng.randint(1400, 2800)
    spo2 = rng.randint(94, 99)
    stress = rng.randint(15, 75)
    return {
        "hrv_ms": hrv,
        "resting_hr": rhr,
        "deep_sleep_hours": sueño_profundo,
        "total_sleep_hours": sueño_total,
        "steps": pasos,
        "calories_burned": calorias,
        "spo2_percent": spo2,
        "stress_score": stress,
        "source": "Open Wearables (simulado)",
        "readiness": "Alta" if hrv > 70 and sueño_profundo > 1.5 else "Media" if hrv > 50 else "Baja"
    }

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

.welcome-bar { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px 24px; margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; }
.welcome-text { font-size: 16px; color: var(--text); }
.welcome-text span { color: var(--accent); font-weight: 600; }
.streak-badge { background: rgba(255,69,0,0.15); border: 1px solid rgba(255,69,0,0.3); border-radius: 20px; padding: 6px 16px; font-size: 13px; font-weight: 600; color: var(--accent); }

.progress-bar-bg { background: var(--surface2); border-radius: 8px; height: 6px; margin: 12px 0 24px 0; }
.progress-bar-fill { background: var(--accent); border-radius: 8px; height: 6px; }

.activation-bar-bg { background: var(--surface2); border-radius: 8px; height: 16px; margin: 8px 0; overflow: hidden; }
.activation-bar-fill { border-radius: 8px; height: 16px; }
.activation-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 4px; }

.hz-display { background: linear-gradient(135deg, #1a0800, #0a0a0a); border: 1px solid var(--accent); border-radius: 12px; padding: 24px; text-align: center; margin: 16px 0; }
.hz-value { font-family: 'Bebas Neue', sans-serif !important; font-size: 72px; color: var(--accent); line-height: 1; }
.hz-label { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 3px; }

.motivational { background: linear-gradient(135deg, #1a0800, #0d0d0d); border-left: 4px solid var(--accent); border-radius: 8px; padding: 16px 20px; margin: 16px 0; font-style: italic; color: var(--text); font-size: 15px; }

.badge-card { background: #1a1a1a; border: 1px solid #ff4500; border-radius: 12px; padding: 16px; text-align: center; }
.badge-icon { font-size: 28px; }
.badge-title { color: #ff4500; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.badge-desc { color: #666; font-size: 10px; margin-top: 2px; }

.stButton > button { background: var(--accent) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; letter-spacing: 1px !important; text-transform: uppercase !important; padding: 12px 28px !important; transition: all 0.2s !important; font-size: 13px !important; }
.stButton > button:hover { background: var(--accent2) !important; transform: translateY(-1px) !important; box-shadow: 0 8px 24px rgba(255,69,0,0.3) !important; }
.stButton > button:disabled { background: #333 !important; color: #666 !important; }

.stSelectbox > div > div, .stTextArea > div > div > textarea, .stNumberInput > div > div > input { background: var(--surface2) !important; border: 1px solid var(--border) !important; color: var(--text) !important; border-radius: 8px !important; }
.stSlider > div > div > div { background: var(--accent) !important; }

.stTabs [data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: 10px !important; padding: 4px !important; gap: 4px !important; border: 1px solid var(--border) !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--muted) !important; border-radius: 8px !important; font-weight: 600 !important; letter-spacing: 1px !important; text-transform: uppercase !important; font-size: 12px !important; }
.stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }

div[data-testid="metric-container"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; padding: 16px !important; }
div[data-testid="metric-container"] label { color: var(--muted) !important; text-transform: uppercase !important; letter-spacing: 2px !important; font-size: 11px !important; }
div[data-testid="metric-container"] div[data-testid="metric-value"] { color: var(--accent) !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 36px !important; }

.tag { display: inline-block; background: rgba(255,69,0,0.15); color: var(--accent); border: 1px solid rgba(255,69,0,0.3); border-radius: 20px; padding: 4px 12px; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-right: 8px; }
.guide-text { color: var(--muted); font-size: 13px; padding: 12px; border: 1px dashed var(--border); border-radius: 8px; text-align: center; margin: 12px 0; }

.bet-number { font-family: 'Bebas Neue', sans-serif !important; font-size: 48px; color: var(--accent); opacity: 0.3; line-height: 1; }
.timer-box { background: var(--surface2); border: 2px solid var(--accent); border-radius: 12px; padding: 16px; text-align: center; margin: 12px 0; }
.timer-val { font-family: 'Bebas Neue', sans-serif !important; font-size: 56px; color: var(--accent); line-height: 1; }
.timer-lbl { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 2px; }

@media (max-width: 600px) {
    .hero-title { font-size: 48px !important; }
    .hz-value { font-size: 56px !important; }
    .timer-val { font-size: 40px !important; }
}
</style>
""", unsafe_allow_html=True)


def get_greeting():
    h = datetime.now().hour
    if h < 12:
        return "Buenos días"
    if h < 19:
        return "Buenas tardes"
    return "Buenas noches"


def get_motivational():
    frases = [
        "El dolor de hoy es la fuerza de mañana.",
        "Tu único límite eres vos mismo.",
        "Cada rep cuenta. Cada día importa.",
        "La disciplina supera a la motivación.",
        "Los campeones se hacen cuando nadie mira.",
        "No pares cuando duela. Para cuando termines.",
        "El cerebro entrena al cuerpo. Entrena los dos.",
    ]
    return random.choice(frases)


defaults = {
    "onboarding_done": False,
    "bet_step": 0,
    "bet_score": 0,
    "bet_complete": False,
    "bet_start_time": None,
    "bet_seq": None,
    "bet_ops": None,
    "bet_pattern": None,
    "session_bet_score": None,
    "session_postura_score": None,
    "session_plan_generado": False,
    "streak": 1,
    "last_session": date.today(),
    "voice_process": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

if "session_start" not in st.session_state:
    st.session_state.session_start = time.time()

if date.today() > st.session_state.last_session:
    st.session_state.streak += 1
    st.session_state.last_session = date.today()

# ONBOARDING
if not st.session_state.onboarding_done:
    st.markdown("""
    <div style="max-width:600px;margin:80px auto;text-align:center;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:72px;color:#ff4500;letter-spacing:4px;line-height:1;">
            FITGUARD<br><span style="color:white;">AI</span>
        </div>
        <div style="color:#666;font-size:14px;letter-spacing:3px;text-transform:uppercase;margin:12px 0 40px;">
            Tu guardián virtual de entrenamiento
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin:32px 0;">
            <div style="background:#111;border:1px solid #222;border-radius:12px;padding:24px 16px;">
                <div style="font-size:32px;margin-bottom:8px;">🧠</div>
                <div style="color:#ff4500;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;">BET Protocol</div>
                <div style="color:#666;font-size:12px;margin-top:4px;">Eleva tu cerebro a 50Hz</div>
            </div>
            <div style="background:#111;border:1px solid #222;border-radius:12px;padding:24px 16px;">
                <div style="font-size:32px;margin-bottom:8px;">📹</div>
                <div style="color:#ff4500;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;">Vision AI</div>
                <div style="color:#666;font-size:12px;margin-top:4px;">Análisis de postura en vivo</div>
            </div>
            <div style="background:#111;border:1px solid #222;border-radius:12px;padding:24px 16px;">
                <div style="font-size:32px;margin-bottom:8px;">🎙️</div>
                <div style="color:#ff4500;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:1px;">Voice Coach</div>
                <div style="color:#666;font-size:12px;margin-top:4px;">Coach de voz en tiempo real</div>
            </div>
        </div>
        <div style="color:#444;font-size:13px;margin-bottom:32px;">
            Prevención de lesiones · Neurociencia aplicada · Coaching personalizado
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("EMPEZAR MI ENTRENAMIENTO", use_container_width=True):
        st.session_state.onboarding_done = True
        st.rerun()
    st.stop()


# HERO
st.markdown("""
<div class="hero">
    <div class="hero-title">FIT<span>GUARD</span> AI</div>
    <div class="hero-sub">Tu guardián virtual de entrenamiento &middot; Powered by Gemini</div>
    <br>
    <span class="tag">🧠 Brain Endurance Training</span>
    <span class="tag">📹 Vision AI</span>
    <span class="tag">🎙️ Live Voice</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="welcome-bar">
    <div class="welcome-text">{get_greeting()}, <span>Atleta</span> - ¿listo para entrenar?</div>
    <div class="streak-badge">🔥 {st.session_state.streak} días seguidos</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="motivational">"{get_motivational()}"</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Pre-Entreno", "Durante", "Post-Entreno"])


# ── TAB 1 ──────────────────────────────────────────────────────────────────
with tab1:

    # --- Open Wearables Panel ---
    wd = get_wearable_data()
    readiness_color = "#00d084" if wd["readiness"] == "Alta" else "#ffaa00" if wd["readiness"] == "Media" else "#ff4500"
    st.markdown(f"""
    <div style="background:#111;border:1px solid #222;border-radius:14px;padding:20px 24px;margin-bottom:20px;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:2px;color:#fff;">
                ⌚ OPEN WEARABLES
            </div>
            <div style="background:rgba(255,69,0,0.15);border:1px solid rgba(255,69,0,0.3);border-radius:20px;padding:4px 14px;font-size:11px;font-weight:600;color:#ff4500;letter-spacing:1px;">
                DATOS DE HOY
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
            <div style="background:#1a1a1a;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#ff4500;">{wd["hrv_ms"]}</div>
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">HRV ms</div>
            </div>
            <div style="background:#1a1a1a;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#ff4500;">{wd["resting_hr"]}</div>
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">FC Rep.</div>
            </div>
            <div style="background:#1a1a1a;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#ff4500;">{wd["deep_sleep_hours"]}h</div>
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Sueño Prof.</div>
            </div>
            <div style="background:#1a1a1a;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:{readiness_color};">{wd["readiness"]}</div>
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Readiness</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:12px;">
            <div style="background:#1a1a1a;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#ff4500;">{wd["steps"]:,}</div>
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Pasos</div>
            </div>
            <div style="background:#1a1a1a;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#ff4500;">{wd["spo2_percent"]}%</div>
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">SpO2</div>
            </div>
            <div style="background:#1a1a1a;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#ff4500;">{wd["stress_score"]}</div>
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Estrés</div>
            </div>
            <div style="background:#1a1a1a;border-radius:10px;padding:14px;text-align:center;">
                <div style="font-size:22px;font-weight:700;color:#ff4500;">{wd["total_sleep_hours"]}h</div>
                <div style="font-size:10px;color:#666;text-transform:uppercase;letter-spacing:1px;margin-top:2px;">Sueño Total</div>
            </div>
        </div>
        <div style="margin-top:12px;font-size:11px;color:#444;text-align:right;">
            via {wd["source"]} · Garmin · Whoop · Apple Health
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # --- Estado Mental ---
    with col1:
        st.subheader("Estado Mental")
        humor = st.selectbox("Nivel de energía", ["Alta", "Normal", "Baja", "Estresado"])
        horas_sueno = st.slider("Horas de sueño", 3, 10, 7)
        estado_libre = st.text_area("Algo más?", placeholder="Ej: Tuve un día difícil...")
        if st.button("Analizar y generar plan"):
            with st.spinner("FitGuard AI analizando..."):
                wearable_context = f"""
Datos biométricos del wearable (Open Wearables API):
- HRV: {wd['hrv_ms']} ms ({"excelente" if wd['hrv_ms'] > 70 else "normal" if wd['hrv_ms'] > 50 else "bajo"})
- Frecuencia cardíaca en reposo: {wd['resting_hr']} bpm
- Sueño profundo: {wd['deep_sleep_hours']}h de {wd['total_sleep_hours']}h totales
- Pasos hoy: {wd['steps']:,}
- SpO2: {wd['spo2_percent']}%
- Score de estrés: {wd['stress_score']}/100
- Readiness general: {wd['readiness']}
"""
                prompt = f"""Sos FitGuard AI, coach de fitness de elite con acceso a datos biométricos reales.

{wearable_context}

Estado subjetivo del atleta:
- Energía percibida: {humor}
- Horas de sueño reportadas: {horas_sueno}h
- Comentario: {estado_libre}

Analizá la combinación de datos objetivos (wearable) y subjetivos. Dame:
1) Análisis del estado real basado en HRV y sueño profundo
2) Tipo de entrenamiento recomendado (considerando readiness: {wd['readiness']})
3) Alerta si hay discrepancia entre lo que siente y lo que muestran los datos
4) Frase motivadora personalizada

En español, amigable y conciso."""
                try:
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                    st.success("Plan generado con datos biométricos")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # --- Protocolo BET ---
    with col2:
        st.subheader("Protocolo BET")
        st.write("Eleva tu frecuencia cerebral al nivel óptimo para entrenar.")

        score_actual = st.session_state.bet_score
        activacion_pct = min(int((score_actual / 9) * 100), 100)
        st.caption(f"Nivel de activación cerebral: {activacion_pct}%")
        st.progress(activacion_pct / 100)

        # Inicializar datos BET una sola vez
        if not st.session_state.bet_complete and st.session_state.bet_seq is None:
            st.session_state.bet_seq = random.choice(["7-3-9-1", "4-8-2-6", "5-1-7-3", "9-2-4-8"])
            st.session_state.bet_ops = [
                (random.randint(10, 50), random.randint(10, 50), "+"),
                (random.randint(20, 99), random.randint(1, 19), "-"),
                (random.randint(2, 9), random.randint(2, 9), "x"),
            ]
            start = random.randint(1, 5)
            patron = [start]
            for _ in range(4):
                patron.append((patron[-1] % 5) + 1)
            st.session_state.bet_pattern = patron
            st.session_state.bet_start_time = time.time()

        if not st.session_state.bet_complete and st.session_state.bet_seq is not None:
            # FORMULARIO ÚNICO — sin st.rerun() entre pasos
            st.divider()
            st.markdown("**01 — Memoria de Trabajo**")
            st.info(f"Secuencia: **{st.session_state.bet_seq}** — invertila con guiones")
            r1 = st.text_input("Secuencia al revés (ej: 1-9-3-7):", key="r1")

            st.divider()
            st.markdown("**02 — Cálculo Mental**")
            responses = []
            for i, (a, b, op) in enumerate(st.session_state.bet_ops):
                r = st.number_input(f"{a} {op} {b} =", key=f"op_{i}", step=1, value=0)
                responses.append(r)

            st.divider()
            st.markdown("**03 — Patrón Visual**")
            patron = st.session_state.bet_pattern
            siguiente = (patron[-1] % 5) + 1
            st.info(f"Patrón: **{' - '.join(map(str, patron))} - ?**")
            otras = [x for x in range(1, 7) if x != siguiente]
            random.shuffle(otras)
            opciones = sorted(otras[:3] + [siguiente])
            resp_patron = st.radio("¿Cuál es el siguiente?", opciones, key="patron_resp", horizontal=True)

            st.divider()
            st.markdown("**04 — Respiración Neural**")
            st.info("🫁 Inhala 4s — Retén 4s — Exhala 4s — Repite 3 veces antes de confirmar")
            respiracion = st.checkbox("✅ Completé la respiración", key="resp_check")

            if st.button("COMPLETAR PROTOCOLO BET", disabled=not respiracion):
                score = 0
                tiempo_usado = int(time.time() - st.session_state.bet_start_time)
                inversa = "-".join(st.session_state.bet_seq.split("-")[::-1])
                if r1.strip() == inversa:
                    score += 2 if tiempo_usado <= 30 else 1
                correctos = 0
                for i, (a, b, op) in enumerate(st.session_state.bet_ops):
                    correcto = a + b if op == "+" else a - b if op == "-" else a * b
                    if responses[i] == correcto:
                        correctos += 1
                score += min(correctos + (1 if tiempo_usado <= 60 else 0), 3)
                if resp_patron == siguiente:
                    score += 2 if tiempo_usado <= 45 else 1
                score += 2
                st.session_state.bet_score = score
                st.session_state.bet_complete = True
                st.session_state.session_bet_score = score

        if st.session_state.bet_complete:
            score = st.session_state.session_bet_score
            hz = "48-52 Hz" if score >= 6 else "35-45 Hz" if score >= 3 else "20-30 Hz"
            nivel = "ÓPTIMO" if score >= 6 else "ACTIVADO" if score >= 3 else "EN CALENTAMIENTO"
            emoji = "🟢" if score >= 6 else "🟡" if score >= 3 else "🔴"
            st.markdown(f'<div class="hz-display"><div class="hz-value">{hz.split("-")[0]}</div><div class="hz-label">Hz estimados · {nivel} {emoji} · Score: {score}/9</div></div>', unsafe_allow_html=True)

            badges = []
            if score >= 8: badges.append(("🏆", "MAESTRO COGNITIVO", "Score perfecto"))
            if score >= 6: badges.append(("⚡", "CEREBRO ACTIVADO", "Frecuencia óptima"))
            if score >= 3: badges.append(("🧠", "ENFOCADO", "BET completado"))
            badges.append(("✅", "GUERRERO MENTAL", "Protocolo finalizado"))

            cols = st.columns(len(badges))
            for i, (icon, title, desc) in enumerate(badges):
                with cols[i]:
                    st.markdown(f'<div class="badge-card"><div class="badge-icon">{icon}</div><div class="badge-title">{title}</div><div class="badge-desc">{desc}</div></div>', unsafe_allow_html=True)

            with st.spinner("Analizando activación cerebral..."):
                prompt = f"Atleta completó protocolo BET con puntuación {score}/9. Estado: {nivel}. Frecuencia: {hz}. Evaluación cognitiva breve y recomendación de entrenamiento. Español, motivador, conciso."
                try:
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

            if st.button("Reiniciar BET"):
                st.session_state.bet_step = 0
                st.session_state.bet_score = 0
                st.session_state.bet_complete = False
                st.session_state.bet_seq = None
                st.session_state.bet_ops = None
                st.session_state.bet_pattern = None


# ── TAB 2 ──────────────────────────────────────────────────────────────────
with tab2:
    col1, col2 = st.columns([1, 1])

    # --- Análisis de Postura ---
    with col1:
        st.subheader("Análisis de Postura")
        ejercicio = st.selectbox("Ejercicio", ["Sentadilla", "Peso muerto", "Plancha", "Flexiones", "Estocada", "Otro"])
        st.markdown('<div class="guide-text">Posiciónate frente a la cámara y captura tu postura durante el ejercicio</div>', unsafe_allow_html=True)
        foto = st.camera_input("Captura tu postura")
        if foto is not None:
            st.image(foto, width=300)
            if st.button("Analizar postura"):
                with st.spinner("Vision AI analizando forma..."):
                    img_b64 = base64.b64encode(foto.getvalue()).decode()
                    prompt = f"Sos FitGuard AI, experto en biomecánica. Analiza la postura en {ejercicio}. Dame: 1) Lo que está bien, 2) Errores y riesgos de lesión, 3) Correcciones específicas, 4) Puntuación /10. En español, conciso."
                    image_part = {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[prompt, image_part]
                        )
                        st.success("Análisis completado")
                        st.markdown(response.text)
                        match = re.search(r"Puntuación\s*:\s*(\d+)/10", response.text, re.IGNORECASE)
                        if match:
                            score = int(match.group(1))
                            st.session_state.session_postura_score = score
                            st.metric("Puntuación de Postura", f"{score}/10")
                        else:
                            st.warning("No se pudo parsear la puntuación")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    # --- BET Entre Sets + Voice Coach ---
    with col2:
        st.subheader("BET Entre Sets")
        st.write("Micro-tarea cognitiva durante el descanso para mantener 50Hz.")
        if st.button("Nueva micro-tarea"):
            tareas = [
                "Contá hacia atrás de 100 de a 7: 100, 93, 86...",
                "Nombrá 5 animales con la misma letra que tu nombre",
                "Visualizá tu próximo set perfecto — 30 segundos",
                "Respiración: inhala 4s, retén 4s, exhala 4s — 3 veces",
                "Cálculo mental: 17 x 6 = ?",
                "Recordá los últimos 5 ejercicios en orden",
                "Deletreá tu apellido al revés",
                "Sumá todos los números del 1 al 10",
                "Nombrá 3 cosas que ves, 2 que escuchas, 1 que sentís",
                "Contá los objetos rectangulares en la habitación",
            ]
            st.info(random.choice(tareas))

        st.divider()
        st.subheader("Voice Coach")
        st.info("Corré python voice_agent.py en tu terminal para activar el coach de voz con Gemini Live API.")

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("🎙️ Activar Voice Coach", disabled=st.session_state.voice_process is not None, key="btn_voice_start"):
                import subprocess
                st.session_state.voice_process = subprocess.Popen(["python", "voice_agent.py"])
                st.rerun()
        with col_v2:
            if st.button("⏹️ Detener", disabled=st.session_state.voice_process is None, key="btn_voice_stop"):
                st.session_state.voice_process.terminate()
                st.session_state.voice_process = None
                st.rerun()

        if st.session_state.voice_process is not None:
            st.success("🟢 Voice Coach activo — Gemini Live API escuchando...")


# ── TAB 3 ──────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Recuperación Holística")

    if st.session_state.session_bet_score is not None or st.session_state.session_postura_score is not None:
        st.markdown("**Resumen de tu sesión de hoy:**")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            duracion_sesion = int((time.time() - st.session_state.session_start) / 60)
            st.metric("Tiempo en app", f"{duracion_sesion} min")
        with col_s2:
            bet_val = f"{st.session_state.session_bet_score}/9" if st.session_state.session_bet_score is not None else "Sin completar"
            st.metric("Score BET", bet_val)
        with col_s3:
            postura_val = f"{st.session_state.session_postura_score}/10" if isinstance(st.session_state.session_postura_score, int) else "Sin analizar"
            st.metric("Puntuación de Postura", postura_val)
        st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        duracion = st.slider("Duración del entreno (min)", 0, 120, 45, key="slider_duracion")
    with col2:
        intensidad = st.selectbox("Intensidad", ["Suave", "Moderada", "Intensa", "Extrema"])
    with col3:
        dolor = st.multiselect("Zona de dolor", ["Ninguna", "Piernas", "Espalda", "Hombros", "Rodillas", "Cuello"])
        if "Ninguna" in dolor:
            dolor = ["Ninguna"]

    notas = st.text_area("¿Cómo te sentís?", placeholder="Ej: Cansado pero bien...")

    if st.button("Generar plan de recuperación"):
        st.session_state.session_plan_generado = True
        bet_info = f"Score BET: {st.session_state.session_bet_score}/9." if st.session_state.session_bet_score else ""
        with st.spinner("Analizando entrenamiento..."):
            prompt = f"""FitGuard AI coach de recuperación con datos biométricos reales.

Datos del wearable post-entreno (Open Wearables API):
- HRV: {wd['hrv_ms']} ms | FC reposo: {wd['resting_hr']} bpm | SpO2: {wd['spo2_percent']}%
- Sueño anoche: {wd['total_sleep_hours']}h ({wd['deep_sleep_hours']}h profundo)
- Estrés acumulado: {wd['stress_score']}/100 | Readiness: {wd['readiness']}

Sesión de hoy: {duracion} min, intensidad {intensidad}, dolor en {', '.join(dolor)}. {bet_info}
Estado subjetivo: {notas}

Dame: 1) Análisis de recuperación considerando HRV y readiness, 2) Estiramientos priorizados, 3) Nutrición específica, 4) Horas de sueño objetivo esta noche, 5) BET para mañana según predicción de recuperación. Español, conciso."""
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.success("Plan de recuperación listo")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {str(e)}")

        st.divider()
        st.subheader("Dashboard de Sesión")
        tiempo_total = int((time.time() - st.session_state.session_start) / 60)
        bet_score = st.session_state.session_bet_score
        hz_final = "48-52 Hz" if bet_score and bet_score >= 6 else "35-45 Hz" if bet_score and bet_score >= 3 else "N/A"
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Tiempo total", f"{tiempo_total} min")
        with c2:
            st.metric("Score BET", f"{bet_score}/9" if bet_score else "—")
        with c3:
            st.metric("Hz alcanzados", hz_final)
        with c4:
            st.metric("Intensidad", intensidad)
        rendimiento = 20
        if bet_score:
            rendimiento += int((bet_score / 9) * 50)
        if isinstance(st.session_state.session_postura_score, int):
            rendimiento += int(st.session_state.session_postura_score / 10 * 30)
        color_r = "#00d084" if rendimiento >= 70 else "#ffaa00" if rendimiento >= 40 else "#ff4500"
        st.markdown(f"""
        <div style="margin-top:16px;">
            <div style="color:#666;font-size:11px;text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;">Rendimiento global de la sesión</div>
            <div style="background:#1a1a1a;border-radius:8px;height:20px;overflow:hidden;">
                <div style="background:{color_r};width:{rendimiento}%;height:20px;border-radius:8px;display:flex;align-items:center;justify-content:center;">
                    <span style="color:white;font-size:11px;font-weight:600;">{rendimiento}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
