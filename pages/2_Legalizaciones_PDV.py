import streamlit as st

st.set_page_config(page_title="Legalizaciones PDV - POPSY", layout="wide")

if not st.session_state.get("usuario_autenticado", False):
    st.warning("⚠️ Inicia sesión en la página principal para continuar.")
    st.stop()

st.title("🧾 Módulo: Legalizaciones PDV")
st.write("Gestión y auditoría de legalizaciones de gastos por Punto de Venta.")