import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="ALERT ELEF - Mercado Real", 
    page_icon="📡", 
    layout="wide"
)

# --- 2. BBDD MAESTRA CON TICKETS REALES DE YAHOO FINANCE ---
# Nota: Modificamos los umbrales para adaptarlos al volumen real diario de Yahoo Finance (en millones de acciones)
BBDD_TICKETS = {
    "USO": {"threshold_m": 3.5, "name": "Petróleo ($USO)"},
    "GLD": {"threshold_m": 5.0, "name": "Oro ($GLD)"},
    "AMD": {"threshold_m": 45.0, "name": "AMD ($AMD)"},
    "IWM": {"threshold_m": 25.0, "name": "Russell 2000 ($IWM)"},
    "QQQ": {"threshold_m": 40.0, "name": "Nasdaq 100 ($QQQ)"},
    "TSLA": {"threshold_m": 70.0, "name": "Tesla ($TSLA)"},
    "AMZN": {"threshold_m": 30.0, "name": "Amazon ($AMZN)"},
    "NVDA": {"threshold_m": 150.0, "name": "Nvidia ($NVDA)"}
}

# --- 3. BARRA LATERAL: CONTROL DE MANDO ---
st.sidebar.header("🎛️ Configuración del Radar")

tickets_seleccionados = st.sidebar.multiselect(
    "Selecciona los tickets en pantalla:",
    options=list(BBDD_TICKETS.keys()),
    default=["USO", "GLD", "AMD", "IWM", "QQQ", "TSLA"]
)

# Selector de auto-refresco para que el móvil actualice solo
segundos_refresco = st.sidebar.slider("Auto-refrescar cada (segundos):", min_value=10, max_value=300, value=30)

st.title("📡 ALERT ELEF - Panel de Control en VIVO")
st.write("Monitoreo conectado a los mercados financieros en tiempo real.")

# --- 4. MOTOR DE DATOS REALES (¡EL CONECTOR!) ---
@st.cache_data(ttl=10) # Guarda los datos 10 segundos para no saturar las peticiones
def descargar_datos_vivos(lista_tickers):
    datos_vivos = {}
    for ticker in lista_tickers:
        try:
            # Conectamos con Yahoo Finance
            t_obj = yf.Ticker(ticker)
            info = t_obj.info
            
            # Extraemos precio actual y volumen acumulado del día
            precio = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
            volumen_puro = info.get("regularMarketVolume") or 0
            volumen_m = volumen_puro / 1_000_000 # Lo pasamos a millones para leerlo fácil
            
            # Cálculo simple de Bandas (Simulado con la tendencia del día para esta fase)
            cambio = info.get("regularMarketChangePercent", 0)
            bollinger = "Expandiendo ↕️" if abs(cambio) > 0.01 else "Comprimiendo 🛑"
            
            datos_vivos[ticker] = {
                "precio": precio,
                "volumen_m": volumen_m,
                "bollinger": bollinger
            }
        except:
            # Si falla la API en algún segundo, ponemos valores por defecto para no romper la app
            datos_vivos[ticker] = {"precio": 0.0, "volumen_m": 0.0, "bollinger": "Desconectado 🛑"}
    return datos_vivos

# --- 5. EJECUCIÓN DEL RADAR ---
if tickets_seleccionados:
    with st.spinner("Conectando con Wall Street..."):
        datos_actuales = descargar_datos_vivos(tickets_seleccionados)
    
    # Alerta Crítica del Yunque ($USO)
    if "USO" in datos_actuales:
        if datos_actuales["USO"]["precio"] >= 123.00:
            st.error(f"⚠️ **ALERTA YUNQUE:** $USO está en ${datos_actuales['USO']['precio']:.2f}. ¡Presión sobre el sector tecnológico!")

    # Construcción de la tabla
    tabla_radar = []
    for ticker in tickets_seleccionados:
        vol_m = datos_actuales[ticker]["volumen_m"]
        precio = datos_actuales[ticker]["precio"]
        bandas = datos_actuales[ticker]["bollinger"]
        umbral_m = BBDD_TICKETS[ticker]["threshold_m"]
        
        if bandas == "Comprimiendo 🛑" and vol_m >= umbral_m:
            estado = "⚠️ EXHAUSTION (No Entry)"
        elif vol_m >= umbral_m:
            estado = "🚨 FUCSIA (Elefante)"
        else:
            estado = "🔵 Azul (Retail)"
            
        tabla_radar.append({
            "Ticket": ticker,
            "Precio": f"${precio:.2f}",
            "Vol. Hoy (M)": f"{vol_m:.2f}M",
            "Umbral Inst.": f"{umbral_m:.1f}M",
            "Bandas (15m)": bandas,
            "Estado": estado
        })

    df = pd.DataFrame(tabla_radar)

    # Formato estético TC2000
    def colorear_estado(val):
        if "FUCSIA" in val:
            return 'background-color: #ff007f; color: white; font-weight: bold;'
        elif "EXHAUSTION" in val:
            return 'background-color: #b22222; color: white; font-weight: bold;'
        return 'background-color: #1e293b; color: #94a3b8;'

    df_styled = df.style.map(colorear_estado, subset=["Estado"])
    
    st.subheader("📊 Radar de Elefantes Real")
    st.dataframe(df_styled, use_container_width=True, hide_index=True)
    
    st.caption(f"Los datos se actualizan automáticamente cada {segundos_refresco} segundos.")

else:
    st.info("Selecciona activos en el menú lateral para encender los monitores.")

# --- 6. SISTEMA DE TEMPORIZADOR AUTOMÁTICO ---
time.sleep(segundos_refresco)
st.rerun()
