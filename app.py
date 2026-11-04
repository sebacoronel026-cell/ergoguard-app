import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="ErgoGuard - Dashboard Ergonómico", page_icon=None, layout="wide")

# --- INYECCIÓN DE CSS LIMPIO Y PROFESIONAL ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
    .main {
        background-color: #0E1117;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .metric-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        border-color: #FF7A00;
    }
    .metric-title {
        font-size: 12px;
        color: #8B949E;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 26px;
        color: #F0F6FC;
        font-weight: 700;
    }
    .welcome-card {
        background: linear-gradient(135deg, #161B22 0%, #1F242C 100%);
        border: 1px solid #30363D;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 12px 24px rgba(0,0,0,0.5);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Inicializar el estado de la sesión
if "sesion_iniciada" not in st.session_state:
    st.session_state.sesion_iniciada = False
if "evaluador" not in st.session_state:
    st.session_state.evaluador = ""
if "empresa" not in st.session_state:
    st.session_state.empresa = ""
if "puesto" not in st.session_state:
    st.session_state.puesto = ""
if "analisis_realizado" not in st.session_state:
    st.session_state.analisis_realizado = False

# --- BOTÓN DE REINICIO EN LA BARRA LATERAL ---
if st.session_state.sesion_iniciada:
    if st.sidebar.button("🔄 Reiniciar Sesión / Cambiar Evaluador"):
        st.session_state.sesion_iniciada = False
        st.session_state.evaluador = ""
        st.session_state.empresa = ""
        st.session_state.puesto = ""
        st.session_state.analisis_realizado = False
        for k in ["input_evaluador", "input_empresa", "input_puesto"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

# --- PANTALLA 1: TARJETA DE IDENTIFICACIÓN DEL EVALUADOR ---
if not st.session_state.sesion_iniciada:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_center1, col_center2, col_center3 = st.columns([1, 2.2, 1])
    
    with col_center2:
        st.markdown("""
            <div class="welcome-card">
                <h2 style='color: #F0F6FC; margin-bottom: 5px;'><i class="fa-solid fa-shield-halved" style="color: #FF7A00;"></i> ErgoGuard</h2>
                <p style='color: #8B949E; font-size: 15px;'>Plataforma de evaluación postureo-dinámica avanzada conforme a la <b>Res. SRT 886/15</b>.</p>
                <hr style='border-color: #30363D; margin: 25px 0;'>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        evaluador_input = st.text_input("Nombre y Apellido del Evaluador / Técnico:", value=st.session_state.evaluador, key="input_evaluador", placeholder="Ej: Lic. Cristian Coronel")
        empresa_input = st.text_input("Empresa / Establecimiento:", value=st.session_state.empresa, key="input_empresa", placeholder="Ej: Planta Industrial S.A.")
        puesto_input = st.text_input("Puesto de Trabajo / Tarea Evaluada:", value=st.session_state.puesto, key="input_puesto", placeholder="Ej: Línea de Ensamble - Operación 3")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Iniciar Sesión de Análisis", use_container_width=True):
            if evaluador_input.strip() == "" or puesto_input.strip() == "":
                st.error("Por favor, complete al menos el nombre del evaluador y el puesto de trabajo.")
            else:
                st.session_state.evaluador = evaluador_input
                st.session_state.empresa = empresa_input if empresa_input else "No especificada"
                st.session_state.puesto = puesto_input
                st.session_state.sesion_iniciada = True
                st.rerun()

    st.stop()

# --- PANTALLA 2: DASHBOARD PRINCIPAL PROFESIONAL ---
st.markdown("### <i class='fa-solid fa-shield-halved' style='color: #FF7A00;'></i> ErgoGuard &bull; Monitor REBA (Grupo A)", unsafe_allow_html=True)
st.markdown(f"<span style='color: #8B949E;'>Evaluador:</span> <b>{st.session_state.evaluador}</b> &nbsp;|&nbsp; <span style='color: #8B949E;'>Empresa:</span> <b>{st.session_state.empresa}</b> &nbsp;|&nbsp; <span style='color: #8B949E;'>Puesto:</span> <b>{st.session_state.puesto}</b>", unsafe_allow_html=True)
st.divider()

# --- BARRA LATERAL: CARGA Y PARÁMETROS MANUALES ---
st.sidebar.markdown("### <i class='fa-solid fa-database' style='color: #FF7A00;'></i> Adquisición de Datos", unsafe_allow_html=True)
archivo_subido = st.sidebar.file_uploader("Subir archivo CSV de la MicroSD", type=["csv"])

st.sidebar.divider()
st.sidebar.markdown("### <i class='fa-solid fa-sliders' style='color: #FF7A00;'></i> Parámetros Manuales (REBA)", unsafe_allow_html=True)

carga_opcion = st.sidebar.selectbox(
    "Peso o Fuerza ejercida:",
    ["< 2 kg (+0)", "2 kg a 10 kg (+1)", "> 10 kg (+2)"]
)
fuerza_brusca = st.sidebar.checkbox("Aplicación brusca o repentina de fuerza (+1)")

agarre_opcion = st.sidebar.selectbox(
    "Calidad del Agarre:",
    ["Bueno (+0)", "Aceptable (+1)", "Pobre (+2)", "Inaceptable / Peligroso (+3)"]
)

st.sidebar.divider()

# --- BOTÓN DE ACCIÓN: ANALIZAR ---
# Cada vez que se sube un nuevo archivo o se cambian los parámetros, permitimos disparar el análisis
ejecutar_analisis = st.sidebar.button("🚀 Ejecutar Análisis REBA", use_container_width=True)

if ejecutar_analisis or st.session_state.analisis_realizado:
    if archivo_subido is not None:
        st.session_state.analisis_realizado = True
    else:
        st.sidebar.warning("⚠️ Debe subir un archivo CSV antes de ejecutar el análisis.")
        st.session_state.analisis_realizado = False

# Mapeo manual
puntos_carga = 1 if "2 kg a 10 kg" in carga_opcion else (2 if "> 10 kg" in carga_opcion else 0)
if fuerza_brusca:
    puntos_carga += 1

puntos_agarre = 0
if "Aceptable" in agarre_opcion:
    puntos_agarre = 1
elif "Pobre" in agarre_opcion:
    puntos_agarre = 2
elif "Inaceptable" in agarre_opcion:
    puntos_agarre = 3

columnas_necesarias = [
    "timestamp", "tronco_flex", "tronco_inc", "tronco_giro",
    "cuello_flex", "cuello_inc", "cuello_giro", "muslo_ang", "pantorrilla_ang"
]

# --- BLOQUEO SI NO SE HA PRESIONADO EL BOTÓN O NO HAY ARCHIVO ---
if not st.session_state.analisis_realizado or archivo_subido is None:
    st.info(f"👋 **Hola, {st.session_state.evaluador}.** El sistema está configurado y a la espera. Por favor, suba el archivo CSV en el panel izquierdo, ajuste los parámetros manuales y presione el botón **'Ejecutar Análisis REBA'** para iniciar.")
    st.stop()

# Si el usuario presionó el botón y subió el archivo, leemos y procesamos de forma segura
try:
    df = pd.read_csv(archivo_subido)
    if not all(col in df.columns for col in columnas_necesarias):
        st.error("⚠️ El archivo CSV subido no contiene las 8 columnas requeridas para el análisis multiaxial del Grupo A.")
        st.session_state.analisis_realizado = False
        st.stop()
except Exception as e:
    st.error(f"Error al leer el archivo: {e}")
    st.session_state.analisis_realizado = False
    st.stop()

# --- PROCESAMIENTO DE DATOS ---
df["pierna_flex_rel"] = (df["muslo_ang"] - df["pantorrilla_ang"]).abs().round(1)

def procesar_reba_a(data):
    ptos_tronco, ptos_cuello, ptos_pierna, score_a_total = [], [], [], []
    for _, row in data.iterrows():
        flex_t = row.get("tronco_flex", 0)
        inc_t = abs(row.get("tronco_inc", 0))
        giro_t = abs(row.get("tronco_giro", 0))
        p_t = 1 if flex_t <= 0 else (2 if flex_t <= 20 else (3 if flex_t <= 60 else 4))
        if inc_t > 5 or giro_t > 5: p_t += 1
            
        flex_c = row.get("cuello_flex", 0)
        inc_c = abs(row.get("cuello_inc", 0))
        giro_c = abs(row.get("cuello_giro", 0))
        p_c = 1 if flex_c <= 20 else 2
        if inc_c > 5 or giro_c > 5: p_c += 1
            
        p_rel = row.get("pierna_flex_rel", 0)
        p_p = 1 if p_rel < 30 else (2 if p_rel <= 60 else 3)
            
        score_a = p_t + p_c + p_p + puntos_carga + puntos_agarre
        ptos_tronco.append(p_t)
        ptos_cuello.append(p_c)
        ptos_pierna.append(p_p)
        score_a_total.append(score_a)
        
    data["P_Tronco"] = ptos_tronco
    data["P_Cuello"] = ptos_cuello
    data["P_Pierna"] = ptos_pierna
    data["Puntaje_Grupo_A"] = score_a_total
    return data

df_procesado = procesar_reba_a(df.copy())
pico_maximo_grupo_a = int(df_procesado["Puntaje_Grupo_A"].max())
promedio_grupo_a = float(df_procesado["Puntaje_Grupo_A"].mean())

if pico_maximo_grupo_a <= 3:
    nivel_riesgo, color_badge = "Nivel 1 - Riesgo Bajo (Aceptable)", "#238636"
elif pico_maximo_grupo_a <= 6:
    nivel_riesgo, color_badge = "Nivel 2 - Riesgo Medio (Comprobar)", "#9E6A03"
elif pico_maximo_grupo_a <= 9:
    nivel_riesgo, color_badge = "Nivel 3 - Riesgo Alto (Cambios pronto)", "#BD561D"
else:
    nivel_riesgo, color_badge = "Nivel 4 - Riesgo Muy Alto (Urgente)", "#DA3633"

# --- PANEL SUPERIOR DE MÉTRICAS ---
st.markdown("#### Resultado Global del Muestreo (Grupo A)")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Puntuación Pico (Máxima)</div>
            <div class="metric-value">{pico_maximo_grupo_a} pts</div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Puntuación Promedio Sesión</div>
            <div class="metric-value">{promedio_grupo_a:.1f} pts</div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Evaluación de Riesgo</div>
            <div class="metric-value" style="font-size: 15px; color: {color_badge}; margin-top: 5px;">{nivel_riesgo}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

sc1, sc2, sc3, sc4 = st.columns(4)
sc1.metric("Registros Muestreados", len(df_procesado))
sc2.metric("Pto. Carga/Fuerza", f"+{puntos_carga}")
sc3.metric("Pto. Agarre", f"+{puntos_agarre}")
sc4.metric("Duración Muestreo", f"{len(df_procesado)} segundos")

st.divider()

# --- FUNCIÓN PARA GENERAR GRÁFICOS ONDULADOS CON DEGRADADO ---
def crear_grafico_ondas(df_data, columnas, titulo, colores):
    fig = go.Figure()
    
    for col, color in zip(columnas, colores):
        rgb = f"rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15)"
        
        fig.add_trace(go.Scatter(
            x=df_data["timestamp"],
            y=df_data[col],
            name=col.replace("_", " ").title(),
            mode='lines+markers',
            line=dict(width=3, color=color, shape='spline'),
            marker=dict(size=4, color=color),
            fill='tozeroy',
            fillcolor=rgb
        ))
        
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=14, color="#F0F6FC")),
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#C9D1D9")),
        xaxis=dict(showgrid=True, gridcolor="#21262D", color="#8B949E", title="Tiempo (s)"),
        yaxis=dict(showgrid=True, gridcolor="#21262D", color="#8B949E")
    )
    return fig

# --- PESTAÑAS PRINCIPALES CON GRÁFICOS MODERNOS ---
tab1, tab2, tab3 = st.tabs(["Gráficos Espaciales (MPU-6050)", "Evaluación Grupo A REBA", "Datos Crudos MicroSD"])

with tab1:
    st.subheader("Evolución Multiaxial por Articulación (Ondas Smooth)")
    
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        fig_tronco = crear_grafico_ondas(
            df_procesado, 
            ["tronco_flex", "tronco_inc", "tronco_giro"], 
            "Tronco (Flexión / Inclinación / Giro)", 
            ["#FF7A00", "#58A6FF", "#3FB950"]
        )
        st.plotly_chart(fig_tronco, use_container_width=True)
        
    with g_col2:
        fig_cuello = crear_grafico_ondas(
            df_procesado, 
            ["cuello_flex", "cuello_inc", "cuello_giro"], 
            "Cuello (Flexión / Inclinación / Giro)", 
            ["#F78166", "#79C0FF", "#56D364"]
        )
        st.plotly_chart(fig_cuello, use_container_width=True)
        
    fig_pierna = crear_grafico_ondas(
        df_procesado, 
        ["pierna_flex_rel"], 
        "Pierna (Ángulo Relativo Muslo - Pantorrilla)", 
        ["#A371F7"]
    )
    st.plotly_chart(fig_pierna, use_container_width=True)

with tab2:
    st.subheader("Comportamiento Temporal de Puntos Parciales por Articulación")
    fig_reba = crear_grafico_ondas(
        df_procesado,
        ["P_Tronco", "P_Cuello", "P_Pierna"],
        "Puntuación Parcial REBA por Segundo",
        ["#FF7A00", "#79C0FF", "#A371F7"]
    )
    st.plotly_chart(fig_reba, use_container_width=True)

with tab3:
    st.subheader("Tabla de Registros de Sensores y Puntuaciones Parciales")
    df_tabla_visible = df_procesado.drop(columns=["Puntaje_Grupo_A"])
    st.dataframe(df_tabla_visible, use_container_width=True)