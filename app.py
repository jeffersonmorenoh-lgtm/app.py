import streamlit as st
import pandas as pd
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="ALERT ELEF - Mobile Command",
    page_icon="📡",
    layout="wide", # En PC se ve amplio, en móvil se apila verticalmente
)

# --- 2. BASE DE DATOS DE REGLAS (G-STATION) ---
# Umbrales y reglas fijadas en tu protocolo
TICKERS_CONFIG = {
    "USO": {"threshold": 250, "desc": "El Gatillo (Petróleo)"},
    "GLD": {"threshold": 300, "desc": "El Búnker (Oro)"},
    "AMD": {"threshold": 180, "desc": "Tecnología (Chips)"},
    "IWM": {"threshold": 200, "desc": "Small Caps"},
    "QQQ": {"threshold": 180, "desc": "Nasdaq 100"},
    "TSLA": {"threshold": 180, "desc": "Volatilidad Tech"}
}

st.title("📡 ALERT ELEF - Panel de Control")
st.write("Monitoreo de flujos institucionales en tiempo real.")

# --- 3. SIMULACIÓN DE ENTRADA DE DATOS (REEMPLAZAR CON API EN PRODUCCIÓN) ---
# Aquí conectarías tu API de Polygon o Alpaca para recibir datos reales
def capturar_datos_mercado():
    # Datos simulados para demostrar la reacción del Dashboard
    return {
        "USO": {"precio": 123.10, "volumen": 280},  # Elefante activo (>250)
        "GLD": {"precio": 215.50, "volumen": 95},   # Retail
        "AMD": {"precio": 271.20, "volumen": 310},  # Elefante activo (>180)
        "IWM": {"precio": 276.40, "volumen": 110},  # Retail
        "QQQ": {"precio": 638.00, "volumen": 140},  # Retail
        "TSLA": {"precio": 391.00, "volumen": 85}   # Retail
    }

datos = capturar_datos_mercado()

# --- 4. ZONA A: ALERTAS CRÍTICAS DE CORRELACIÓN ---
st.subheader("🚨 ALERTAS DE IMPACTO CRÍTICO")

# Alerta automática: Si USO rompe los $123 y tiene volumen institucional
if datos["USO"]["precio"] >= 123.00 and datos["USO"]["volumen"] >= TICKERS_CONFIG["USO"]["threshold"]:
    st.error(f"⚠️ **ALERTA YUNQUE:** $USO en ${datos['USO']['precio']} con Volumen de {datos['USO']['volumen']}. ¡Presión bajista inminente en Tech/IWM!")

# --- 5. ZONA B: MÓNITOR DE COLUMNAS (ALERT ELEF) ---
st.subheader("📊 Radar de Elefantes")

# Creamos una lista para estructurar la tabla de visualización
tabla_radar = []

for ticker, config in TICKERS_CONFIG.items():
    vol_actual = datos[ticker]["volumen"]
    precio_actual = datos[ticker]["precio"]
    umbral = config["threshold"]
    
    # Condición de Elefante (Volumen supera el umbral del sistema)
    if vol_actual >= umbral:
        status = "🚨 FUCSIA (Elefante)"
    else:
        status = "🔵 Azul (Retail)"
        
    tabla_radar.append({
        "Ticket": ticker,
        "Precio": f"${precio_actual:.2f}",
        "Vol. Inst": vol_actual,
        "Umbral Mínimo": umbral,
        "Estado": status
    })

df = pd.DataFrame(tabla_radar)

# Mostramos la tabla optimizada para pantallas responsivas
st.dataframe(
    df, 
    use_container_width=True, # Se estira para ocupar el 100% de la pantalla del móvil
    hide_index=True
)

# --- 6. AUTO-REFRESCO ---
# Botón para forzar la actualización manual en el móvil de forma rápida
if st.button("🔄 Actualizar Radar"):
    st.rerun()
