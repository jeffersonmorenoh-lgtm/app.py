import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="ALERT ELEF - Comando Móvil", 
    page_icon="📡", 
    layout="wide"
)

# --- 2. BASE DE DATOS MAESTRA DE TICKETS Y UMBRALES DE ELEFANTE ---
# Aquí puedes registrar todos los activos que sueles vigilar
BBDD_TICKETS = {
    "USO": {"threshold": 250, "name": "Petróleo ($USO)", "default_price": 123.10},
    "GLD": {"threshold": 300, "name": "Oro ($GLD)", "default_price": 215.50},
    "AMD": {"threshold": 180, "name": "AMD ($AMD)", "default_price": 271.20},
    "IWM": {"threshold": 200, "name": "Russell 2000 ($IWM)", "default_price": 276.40},
    "QQQ": {"threshold": 180, "name": "Nasdaq 100 ($QQQ)", "default_price": 638.00},
    "TSLA": {"threshold": 180, "name": "Tesla ($TSLA)", "default_price": 391.00},
    "AMZN": {"threshold": 180, "name": "Amazon ($AMZN)", "default_price": 185.30},
    "NVDA": {"threshold": 200, "name": "Nvidia ($NVDA)", "default_price": 125.50},
    "AAPL": {"threshold": 180, "name": "Apple ($AAPL)", "default_price": 190.20}
}

# --- 3. BARRA LATERAL: CONTROL DE MANDO (Para el móvil se oculta en un menú desplegable) ---
st.sidebar.header("🎛️ Configuración del Radar")

# ¡AQUÍ ESTÁ TU MEJORA! Selector dinámico de tickets para el Dashboard
tickets_seleccionados = st.sidebar.multiselect(
    "Selecciona los tickets en pantalla:",
    options=list(BBDD_TICKETS.keys()),
    default=["USO", "GLD", "AMD", "IWM", "QQQ", "TSLA"] # Tus 6 activos iniciales
)

st.title("📡 ALERT ELEF - Panel de Control")
st.write("Monitoreo dinámico de flujos institucionales y correlaciones.")

# --- 4. SIMULACIÓN DE DATOS REALES ---
def capturar_datos_mercado():
    # Simula el estado del mercado (Precios, volumen actual y estado de Bollinger)
    return {
        "USO": {"precio": 123.10, "volumen": 280, "bollinger": "Expandiendo ↕️"},
        "GLD": {"precio": 215.50, "volumen": 95,  "bollinger": "Comprimiendo 🛑"},
        "AMD": {"precio": 271.20, "volumen": 310, "bollinger": "Expandiendo ↕️"},
        "IWM": {"precio": 276.40, "volumen": 110, "bollinger": "Comprimiendo 🛑"},
        "QQQ": {"precio": 638.00, "volumen": 140, "bollinger": "Expandiendo ↕️"},
        "TSLA": {"precio": 391.00, "volumen": 85,  "bollinger": "Comprimiendo 🛑"},
        "AMZN": {"precio": 187.50, "volumen": 210, "bollinger": "Expandiendo ↕️"},
        "NVDA": {"precio": 128.20, "volumen": 90,  "bollinger": "Expandiendo ↕️"},
        "AAPL": {"precio": 191.00, "volumen": 75,  "bollinger": "Comprimiendo 🛑"}
    }

datos_actuales = capturar_datos_mercado()

# --- 5. ALERTA DE IMPACTO CRÍTICO ($USO) ---
if "USO" in tickets_seleccionados:
    if datos_actuales["USO"]["precio"] >= 123.00 and datos_actuales["USO"]["volumen"] >= BBDD_TICKETS["USO"]["threshold"]:
        st.error(f"⚠️ **ALERTA YUNQUE:** $USO en ${datos_actuales['USO']['precio']} con volumen fuerte. ¡La tecnología e IWM tienden a enfriarse!")

# --- 6. CONSTRUCCIÓN DE LA TABLA DINÁMICA ---
tabla_radar = []

for ticker in tickets_seleccionados:
    config = BBDD_TICKETS[ticker]
    vol = datos_actuales[ticker]["volumen"]
    precio = datos_actuales[ticker]["precio"]
    bandas = datos_actuales[ticker]["bollinger"]
    umbral = config["threshold"]
    
    # Lógica de color y estado basada en tus reglas principales
    if bandas == "Comprimiendo 🛑" and vol >= umbral:
        estado = "⚠️ EXHAUSTION (No Entry)"
    elif vol >= umbral:
        estado = "🚨 FUCSIA (Elefante)"
    else:
        estado = "🔵 Azul (Retail)"
        
    tabla_radar.append({
        "Ticket": ticker,
        "Precio": f"${precio:.2f}",
        "Vol. Inst": vol,
        "Umbral Mínimo": umbral,
        "Bandas (15m)": bandas,
        "Estado": estado
    })

# Evitar errores si el usuario deselecciona todos los tickets
if tabla_radar:
    df = pd.DataFrame(tabla_radar)

    # --- 7. FORMATO DE COLOR ESTILO TC2000 ---
    def colorear_estado(val):
        if "FUCSIA" in val:
            return 'background-color: #ff007f; color: white; font-weight: bold;' # Fucsia Institucional
        elif "EXHAUSTION" in val:
            return 'background-color: #b22222; color: white; font-weight: bold;' # Rojo Alerta Exhaustion Bias
        return 'background-color: #1e293b; color: #94a3b8;' # Azul/Gris Neutro

    df_styled = df.style.map(colorear_estado, subset=["Estado"])

    st.subheader("📊 Radar de Elefantes Personalizado")
    st.dataframe(df_styled, use_container_width=True, hide_index=True)
else:
    st.info("Selecciona al menos un ticket en la barra lateral para activar el radar.")

# --- 8. BOTÓN DE REFRESCO ---
if st.button("🔄 Actualizar Radar"):
    st.rerun()
