import streamlit as st

st.set_page_config(page_title="Visualización de Ventas - POPSY", layout="wide")

if not st.session_state.get("usuario_autenticado", False):
    st.warning("⚠️ Inicia sesión en la página principal para continuar.")
    st.stop()

rol_actual = st.session_state.datos_usuario.get("rol", "")
if rol_actual not in ["Administrador", "Contabilidad"]:
    st.error("🔒 No tienes permisos para visualizar el módulo de ventas.")
    st.stop()

st.title("📊 Módulo: Visualización de Ventas")
st.write("Análisis e indicadores clave de ventas por tienda.")