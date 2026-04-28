import streamlit as st
import random
import time

st.set_page_config(page_title="TCMP Industrial", layout="wide")

# ===== ESTILOS INDUSTRIALES (MODO NOCTURNO) =====
st.markdown("""
<style>
body {
    background-color: #0b0f14;
}

.panel {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #30363d;
}

.titulo {
    font-size: 30px;
    font-weight: bold;
    color: #00e5ff;
}

.alerta {
    background-color: #ff3b3b;
    color: white;
    padding: 25px;
    border-radius: 10px;
    text-align: center;
    font-size: 20px;
}

.ok {
    background-color: #00c853;
    color: white;
    padding: 25px;
    border-radius: 10px;
    text-align: center;
    font-size: 20px;
}

.metric-box {
    background-color: #0d1117;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid #30363d;
}

input {
    background-color: #0d1117 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ===== CONSTANTE DEL SISTEMA =====
UMBRAL = 2.0  # ppm fijo según diseño

# ===== HEADER =====
st.markdown("<div class='titulo'>TCMP - Torre de Control de Materia Prima</div>", unsafe_allow_html=True)
st.write("Simulación de inspección automatizada con umbral fijo de seguridad (2.0 ppm)")

st.divider()

# ===== INPUT DEL USUARIO =====
col1, col2 = st.columns(2)

with col1:
    lote = st.text_input("ID del lote", value=f"L-{random.randint(1000,9999)}")

with col2:
    nivel_input = st.number_input("Nivel de plomo a evaluar (ppm)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

st.divider()

# ===== BOTÓN PRINCIPAL =====
if st.button("🔍 Ejecutar inspección", use_container_width=True):

    with st.spinner("Analizando muestra con XRF..."):
        time.sleep(1.5)
        nivel = round(nivel_input, 2)

    st.divider()

    # ===== MÉTRICAS =====
    m1, m2, m3 = st.columns(3)

    m1.markdown(f"<div class='metric-box'><h3>{lote}</h3><p>Lote</p></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-box'><h3>{nivel} ppm</h3><p>Plomo detectado</p></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-box'><h3>{UMBRAL} ppm</h3><p>Umbral fijo</p></div>", unsafe_allow_html=True)

    st.divider()

    # ===== RESULTADO =====
    if nivel > UMBRAL:
        st.markdown(f"""
        <div class='alerta'>
        ⚠️ ALERTA DE SEGURIDAD<br><br>
        LOTE RECHAZADO<br><br>
        Nivel detectado: {nivel} ppm<br>
        Límite permitido: {UMBRAL} ppm<br><br>
        🔒 INTERLOCK ACTIVADO<br>
        Descarga bloqueada automáticamente
        </div>
        """, unsafe_allow_html=True)

        estado = "Rechazado"

    else:
        st.markdown(f"""
        <div class='ok'>
        ✅ LOTE APROBADO<br><br>
        Nivel detectado: {nivel} ppm<br>
        Dentro del límite permitido<br><br>
        🔓 Descarga habilitada
        </div>
        """, unsafe_allow_html=True)

        estado = "Aprobado"

    # ===== HISTORIAL =====
    if "historial" not in st.session_state:
        st.session_state.historial = []

    st.session_state.historial.append((lote, nivel, estado))

# ===== HISTORIAL GLOBAL =====
st.divider()
st.subheader("Historial de inspecciones")

if "historial" in st.session_state:
    for i, (l, n, e) in enumerate(st.session_state.historial[::-1]):
        st.write(f"{l} | {n} ppm | {e}")
else:
    st.write("Sin registros aún")
