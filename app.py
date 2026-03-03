import streamlit as st
import os
import time
import random
from dotenv import load_dotenv
from google import genai
import base64

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="FitGuard AI", page_icon="💪", layout="centered")
st.title("💪 FitGuard AI")
st.subheader("Tu guardian virtual de entrenamiento")

tab1, tab2, tab3 = st.tabs(["Pre-Entreno", "Durante", "Post-Entreno"])

with tab1:
    st.header("Preparacion Mental Pre-Entreno")
    
    humor = st.selectbox("Como esta tu energia?", ["Alta", "Normal", "Baja", "Estresado"])
    horas_sueno = st.slider("Cuantas horas dormiste?", 0, 12, 7)
    estado_libre = st.text_area("Algo mas?", placeholder="Ej: Tuve un dia dificil...")
    
    if st.button("Analizar y generar mi plan"):
        with st.spinner("Analizando..."):
            prompt = f"Sos FitGuard AI, coach de fitness. El usuario tiene energia {humor}, durmio {horas_sueno} horas. Comentario: {estado_libre}. Dame: 1) Analisis de estado, 2) Tipo de entrenamiento recomendado, 3) Micro-tarea cognitiva BET, 4) Frase motivadora. En espanol, amigable y conciso."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.success("Tu plan esta listo!")
            st.markdown(response.text)

    st.divider()
    st.subheader("🧠 Protocolo BET — Activacion Cerebral 50Hz")
    st.write("Completá este protocolo antes de entrenar para elevar tu frecuencia cerebral al nivel óptimo (50Hz).")

    if "bet_step" not in st.session_state:
        st.session_state.bet_step = 0
        st.session_state.bet_score = 0
        st.session_state.reaction_start = None
        st.session_state.bet_complete = False

    if st.button("🚀 Iniciar Protocolo BET", disabled=st.session_state.bet_complete):
        st.session_state.bet_step = 1
        st.session_state.bet_score = 0
        st.session_state.bet_complete = False
        st.rerun()

    if st.session_state.bet_step == 1:
        st.markdown("### Paso 1 de 3 — Test de Memoria de Trabajo")
        st.write("Memorizá esta secuencia y escribila al reves:")
        secuencia = random.choice(["7-3-9-1", "4-8-2-6", "5-1-7-3", "9-2-4-8"])
        st.info(f"**{secuencia}**")
        respuesta = st.text_input("Escribí la secuencia al reves:")
        if st.button("Confirmar Paso 1"):
            inversa = "-".join(secuencia.split("-")[::-1])
            if respuesta.strip() == inversa:
                st.success("✅ Correcto! +1 punto de activacion")
                st.session_state.bet_score += 1
            else:
                st.warning(f"La respuesta correcta era: {inversa}")
            st.session_state.bet_step = 2
            st.rerun()

    if st.session_state.bet_step == 2:
        st.markdown("### Paso 2 de 3 — Calculo Mental Rapido")
        st.write("Resolvé estos calculos lo mas rapido posible:")
        ops = [
            (random.randint(10,50), random.randint(10,50), "+"),
            (random.randint(20,99), random.randint(1,19), "-"),
            (random.randint(2,9), random.randint(2,9), "x"),
        ]
        respuestas_correctas = 0
        for i, (a, b, op) in enumerate(ops):
            if op == "+":
                correcto = a + b
            elif op == "-":
                correcto = a - b
            else:
                correcto = a * b
            r = st.number_input(f"{a} {op} {b} =", key=f"op_{i}", step=1, value=0)
            if r == correcto:
                respuestas_correctas += 1
        if st.button("Confirmar Paso 2"):
            if respuestas_correctas == 3:
                st.success("✅ Perfecto! +2 puntos de activacion")
                st.session_state.bet_score += 2
            elif respuestas_correctas >= 1:
                st.warning(f"Correcto {respuestas_correctas}/3. +1 punto")
                st.session_state.bet_score += 1
            else:
                st.error("Seguimos entrenando la mente 💪")
            st.session_state.bet_step = 3
            st.rerun()

    if st.session_state.bet_step == 3:
        st.markdown("### Paso 3 de 3 — Foco y Respiracion")
        st.write("Realizá este ejercicio de respiracion para sincronizar tu cerebro:")
        st.info("**Inhala 4 segundos → Retene 4 segundos → Exhala 4 segundos** (repeti 3 veces)")
        if st.button("✅ Completé la respiracion"):
            st.session_state.bet_score += 2
            st.session_state.bet_step = 4
            st.rerun()

    if st.session_state.bet_step == 4:
        score = st.session_state.bet_score
        st.session_state.bet_complete = True
        if score >= 4:
            nivel = "OPTIMO 🟢"
            hz = "48-52 Hz"
            emoji = "🔥"
        elif score >= 2:
            nivel = "ACTIVADO 🟡"
            hz = "35-45 Hz"
            emoji = "⚡"
        else:
            nivel = "EN CALENTAMIENTO 🔴"
            hz = "20-30 Hz"
            emoji = "🧘"
        st.balloons()
        st.success(f"{emoji} Protocolo BET completado!")
        st.metric("Estado Cerebral", nivel)
        st.metric("Frecuencia Estimada", hz)
        with st.spinner("FitGuard AI analizando tu activacion..."):
            prompt = f"El atleta completo el protocolo BET con puntuacion {score}/5. Estado: {nivel}. Frecuencia cerebral estimada: {hz}. Dame una evaluacion de su estado cognitivo y una recomendacion especifica para su entrenamiento de hoy basada en neurociencia del deporte. En espanol, motivador y conciso."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.markdown(response.text)

with tab2:
    st.header("Coaching en Vivo")
    st.write("Subi una foto de tu postura durante el ejercicio y FitGuard AI la analizara.")
    ejercicio = st.selectbox("Que ejercicio estas haciendo?", ["Sentadilla", "Peso muerto", "Plancha", "Flexiones", "Estocada", "Otro"])
    foto = st.camera_input("Saca una foto de tu postura")
    if foto is not None:
        st.image(foto, caption="Tu postura", width=400)
        if st.button("Analizar mi postura"):
            with st.spinner("FitGuard AI analizando tu forma..."):
                img_bytes = foto.getvalue()
                img_b64 = base64.b64encode(img_bytes).decode()
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        {"role": "user", "parts": [
                            {"text": f"Sos FitGuard AI, experto en biomechanica y prevencion de lesiones. Analiza la postura del usuario haciendo {ejercicio}. Dame: 1) Evaluacion de la forma, 2) Errores detectados y riesgos de lesion, 3) Correcciones especificas, 4) Puntuacion de 1 a 10. En espanol, amigable y conciso."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                        ]}
                    ]
                )
                st.success("Analisis completado!")
                st.markdown(response.text)

    st.divider()
    st.subheader("🧠 BET Entre Sets")
    st.write("Realizá esta micro-tarea cognitiva durante tu descanso entre series:")
    if st.button("🎯 Nueva micro-tarea BET"):
        tareas = [
            "Conta hacia atras de 100 de a 7: 100, 93, 86...",
            "Nembra 5 animales que empiecen con la misma letra que tu nombre",
            "Visualiza tu proximo set perfecto durante 30 segundos",
            "Respira: inhala 4s, retene 4s, exhala 4s — 3 veces",
            "Resuelve mentalmente: 17 x 6 = ?",
            "Recordá los ultimos 5 ejercicios que hiciste hoy en orden",
        ]
        tarea = random.choice(tareas)
        st.info(f"**Micro-tarea:** {tarea}")
        st.caption("Completá esto durante tu descanso para mantener tu cerebro activo y en 50Hz")

with tab3:
    st.header("Recuperacion Post-Entreno")
    duracion = st.slider("Cuanto tiempo entrenaste? (minutos)", 0, 120, 45)
    intensidad = st.selectbox("Como fue la intensidad?", ["Suave", "Moderada", "Intensa", "Extrema"])
    dolor = st.multiselect("Sientes dolor en alguna zona?", ["No", "Piernas", "Espalda", "Hombros", "Rodillas", "Cuello"])
    notas = st.text_area("Como te sientes ahora?", placeholder="Ej: Cansado pero bien...")
    if st.button("Generar plan de recuperacion"):
        with st.spinner("Analizando tu entrenamiento..."):
            prompt = f"Sos FitGuard AI, coach de recuperacion. El usuario entreno {duracion} minutos con intensidad {intensidad}. Dolor en: {dolor}. Se siente: {notas}. Dame: 1) Analisis del entrenamiento, 2) Rutina de estiramiento, 3) Nutricion para recuperacion, 4) Recomendacion de descanso, 5) BET para manana (micro-tarea cognitiva para mantener neuroplasticidad). En espanol, amigable y conciso."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.success("Tu plan de recuperacion esta listo!")
            st.markdown(response.text)