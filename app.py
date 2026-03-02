import streamlit as st
import os
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

with tab2:
    st.header("Coaching en Vivo")
    st.write("Subi una foto de tu postura durante el ejercicio y FitGuard AI la analizara.")
    ejercicio = st.selectbox("Que ejercicio estas haciendo?", ["Sentadilla", "Peso muerto", "Plancha", "Flexiones", "Estocada", "Otro"])
    foto = st.camera_input("Saca una foto de tu postura")
    if foto is not None:
        st.image(foto, caption="Tu postura", use_column_width=True)
        if st.button("Analizar mi postura"):
            with st.spinner("FitGuard AI analizando tu forma..."):
                img_bytes = foto.getvalue()
                img_b64 = base64.b64encode(img_bytes).decode()
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        {"role": "user", "parts": [
                            {"text": f"Sos FitGuard AI, experto en biomechanica y prevencion de lesiones. Analiza la postura del usuario haciendo {ejercicio}. Dame: 1) Evaluacion de la forma (que esta bien), 2) Errores detectados y riesgos de lesion, 3) Correcciones especificas, 4) Puntuacion de 1 a 10. En espanol, amigable y conciso."},
                            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                        ]}
                    ]
                )
                st.success("Analisis completado!")
                st.markdown(response.text)

with tab3:
    st.header("Recuperacion Post-Entreno")
    duracion = st.slider("Cuanto tiempo entrenaste? (minutos)", 0, 120, 45)
    intensidad = st.selectbox("Como fue la intensidad?", ["Suave", "Moderada", "Intensa", "Extrema"])
    dolor = st.multiselect("Sientes dolor en alguna zona?", ["No", "Piernas", "Espalda", "Hombros", "Rodillas", "Cuello"])
    notas = st.text_area("Como te sientes ahora?", placeholder="Ej: Cansado pero bien...")
    if st.button("Generar plan de recuperacion"):
        with st.spinner("Analizando tu entrenamiento..."):
            prompt = f"Sos FitGuard AI, coach de recuperacion. El usuario entreno {duracion} minutos con intensidad {intensidad}. Dolor en: {dolor}. Se siente: {notas}. Dame: 1) Analisis del entrenamiento, 2) Rutina de estiramiento, 3) Nutricion para recuperacion, 4) Recomendacion de descanso. En espanol, amigable y conciso."
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            st.success("Tu plan de recuperacion esta listo!")
            st.markdown(response.text)