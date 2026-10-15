import streamlit as st

st.set_page_config(
    page_title="Legalizaciones PDV - Portal Popsy",
    page_icon="🍦",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #FAFAFC; }
    .popsy-header {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%);
        padding: 1.5rem;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(184, 0, 73, 0.06);
        border: 2px solid #FFC0CB;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-title { font-size: 2.2rem; color: #B80049; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.markdown("""
        <div style="background-color: #FFF3CD; padding: 20px; border-radius: 10px; border-left: 6px solid #FFEEBA; text-align: center; margin-top: 50px;">
            <h3 style="color: #856404; margin-top: 0;">⚠️ Acceso Restringido</h3>
            <p style="font-size: 1.1rem; color: #533F03;">Por favor, regresa a la página principal (<b>app.py</b>) e inicia sesión con tu correo corporativo para acceder a este módulo.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="popsy-header">
            <div class="main-title">📋 Legalizaciones PDV POPSY</div>
            <p style="color: #666; font-style: italic; margin-bottom: 0;">Registro y control de gastos por punto de venta</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.success(f"Sesión activa con: **{st.session_state.correo_usuario}**")
    st.markdown("### Gestión de Legalizaciones")
    st.info("Módulo de legalizaciones cargado correctamente.")
