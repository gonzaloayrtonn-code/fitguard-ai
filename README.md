# 💪 FitGuard AI
### Tu Guardian Virtual de Entrenamiento · Powered by Gemini

> **Gemini Live Agent Challenge 2025** — Live Agents + Multimodal I/O

## 🧠 ¿Qué es FitGuard AI?

FitGuard AI es un agente multimodal de fitness que combina análisis visual en tiempo real, coaching de voz con Gemini Live API, y Brain Endurance Training (BET) — una técnica de neurociencia para elevar la frecuencia cerebral a 50Hz antes de entrenar.

**Resuelve 3 problemas reales:**
- 30-70% de deportistas recreativos sufren lesiones evitables
- 70% abandona rutinas por burnout mental
- Falta de coaching personalizado accesible

## ✨ Features

### ⚡ Pre-Entreno
- Análisis de estado mental y energía
- Protocolo BET interactivo (memoria, cálculo, respiración)
- Estimación de frecuencia cerebral (Hz)
- Plan de entrenamiento personalizado con Gemini

### 🏋️ Durante el Entreno
- Análisis de postura en tiempo real con Gemini Vision
- Detección de errores biomecánicos y riesgos de lesión
- Micro-tareas BET entre sets para mantener 50Hz
- Coach de voz en tiempo real con Gemini Live API

### 🌙 Post-Entreno
- Análisis holístico de recuperación
- Plan de nutrición y descanso personalizado
- BET para el día siguiente

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI:** Google Gemini 2.5 Flash + Gemini Live API (audio nativo)
- **Vision:** Gemini multimodal (análisis de imagen/video)
- **Voice:** Gemini Live API con WebSockets en tiempo real
- **Deploy:** Google Cloud Run
- **SDK:** google-genai (Python)

## 🚀 Demo en Vivo

🌐 **App:** https://fitguard-ai-867186428147.us-central1.run.app

## 🏃 Instalación Local
`ash
git clone https://github.com/gonzaloayrtonn-code/fitguard-ai
cd fitguard-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
`

Crear archivo .env:
`
GEMINI_API_KEY=tu_api_key_aqui
`

Ejecutar app web:
`ash
streamlit run app.py
`

Ejecutar coach de voz:
`ash
python voice_agent.py
`

## 🧬 Brain Endurance Training (BET)

El BET es una técnica validada científicamente que entrena el cerebro bajo fatiga cognitiva para mejorar la resiliencia mental. FitGuard AI integra BET en 3 momentos clave:

1. **Pre-entreno:** Protocolo de activación para alcanzar 50Hz
2. **Durante:** Micro-tareas entre sets para mantener el estado óptimo  
3. **Post-entreno:** BET de recuperación para el día siguiente

## 📁 Estructura
`
fitguard-ai/
├── app.py              # App principal Streamlit
├── voice_agent.py      # Gemini Live API voice coach
├── requirements.txt    # Dependencias
├── Dockerfile          # Deploy en Cloud Run
└── .env               # API keys (no incluido)
`

## 👤 Autor

Gonzalo Ayrton Nuñez · [@gonzaloayrtonn-code](https://github.com/gonzaloayrtonn-code)

---
*Built for the Gemini Live Agent Challenge 2025*
