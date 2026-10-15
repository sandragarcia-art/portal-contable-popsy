import streamlit as st

st.set_page_config(page_title="Control de Efectivo - POPSY", layout="wide")

if not st.session_state.get("usuario_autenticado", False):
    st.warning("⚠️ Inicia sesión en la página principal (app.py) para continuar.")
    st.stop()

rol_actual = st.session_state.datos_usuario.get("rol", "")
if rol_actual not in ["Administrador", "Contabilidad"]:
    st.error("🔒 No tienes permisos para acceder al módulo de Control de Efectivo.")
    st.info(f"Tu rol actual es: **{rol_actual}**.")
    st.stop()

st.title("💵 Módulo: Control de Efectivo")
st.write("Sistema de conciliación de cajas y bancos para Helados Popsy.")