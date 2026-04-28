import streamlit as st
import random
import time

st.set_page_config(page_title="TCMP Industrial", layout="wide")

# ===== ESTILOS INDUSTRIALES =====
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.panel {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #333;
}

.titulo {
    font-size: 28px;
    font-weight: bold;
    color: #00d4ff;
}

.alerta {
    background-color: #ff2e2e;
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
    background-color: #11151c;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown("<div class='titulo'>TCMP - Torre de Control de Materia Prima</div>", unsafe_allow_html=True)
st.write("Sistema automatizado de detección de metales pesados (Simulación)")

st.divider()

# ===== CONFIGURACIÓN =====
col1, col2 = st.columns(2)

with col1:
    umbral = st.slider("Umbral permitido (ppm)", 0.5, 5.0, 2.0)

with col2:
    lote = st.text_input("ID del lote", value=f"L-{random.randint(1000,9999)}")

st.divider()

# ===== BOTÓN PRINCIPAL =====
if st.button("🔍 Iniciar inspección", use_container_width=True):

    with st.spinner("Analizando muestra con XRF..."):
        time.sleep(2)
        nivel = round(random.uniform(0.5, 5.0), 2)

    st.divider()

    # ===== MÉTRICAS =====
    m1, m2, m3 = st.columns(3)

    m1.markdown(f"<div class='metric-box'><h3>{lote}</h3><p>Lote</p></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-box'><h3>{nivel} ppm</h3><p>Plomo detectado</p></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-box'><h3>{umbral} ppm</h3><p>Umbral</p></div>", unsafe_allow_html=True)

    st.divider()

    # ===== RESULTADO =====
    if nivel > umbral:
        st.markdown(f"""
        <div class='alerta'>
        ⚠️ ALERTA DE SEGURIDAD<br><br>
        LOTE RECHAZADO<br><br>
        Nivel detectado: {nivel} ppm<br>
        Límite permitido: {umbral} ppm<br><br>
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
