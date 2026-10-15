import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Control Efectivo - Portal Popsy",
    page_icon="🍦",
    layout="wide"
)

# Estilo visual corporativo Popsy (Fucsia/Rosado)
st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFC;
    }
    .popsy-header {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%);
        padding: 1.5rem;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(184, 0, 73, 0.06);
        border: 2px solid #FFC0CB;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-title {
        font-size: 2.2rem;
        color: #B80049;
        font-weight: 800;
    }
    .popsy-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border-left: 5px solid #B80049;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #B80049 0%, #D81B60 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        border: none;
        box-shadow: 0 4px 10px rgba(184, 0, 73, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #900038 0%, #B80049 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Validación de seguridad: Verificar si el usuario ya inició sesión en app.py
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.markdown("""
        <div style="background-color: #FFF3CD; padding: 20px; border-radius: 10px; border-left: 6px solid #FFEEBA; text-align: center; margin-top: 50px;">
            <h3 style="color: #856404; margin-top: 0;">⚠️ Acceso Restringido</h3>
            <p style="font-size: 1.1rem; color: #533F03;">Por favor, regresa a la página principal (<b>app.py</b>) e inicia sesión con tu correo corporativo para acceder a este módulo.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # Encabezado del Módulo
    st.markdown("""
        <div class="popsy-header">
            <div class="main-title">💵 Control Efectivo POPSY</div>
            <p style="color: #666; font-style: italic; margin-bottom: 0;">Registro y arqueos de efectivo por Punto de Venta (PDV)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info(f"👤 Usuario conectado: **{st.session_state.correo_usuario}**")
    
    # Formulario de Registro de Control de Efectivo
    st.markdown("""
        <div class="popsy-card">
            <h3 style="color: #B80049; margin-top: 0;">📝 Registro de Arqueo Diario</h3>
        </div>
    """, unsafe_allow_html=True)

    with st.form("form_control_efectivo"):
        col1, col2 = st.columns(2)
        
        with col1:
            fecha_arqueo = st.date_input("Fecha del Arqueo", value=datetime.today())
            pdv = st.selectbox("Punto de Venta (PDV)", [
                "PDV Andino", 
                "PDV Retiro", 
                "PDV Gran Estación", 
                "PDV Unicentro", 
                "PDV Salitre Plaza", 
                "PDV Galerías"
            ])
            efectivo_sistema = st.number_input("Efectivo según Sistema ($)", min_value=0.0, format="%.2f")
            
        with col2:
            efectivo_fisico = st.number_input("Efectivo Físico Contado ($)", min_value=0.0, format="%.2f")
            consignaciones = st.number_input("Total Consignaciones / Transferencias ($)", min_value=0.0, format="%.2f")
            datafonos = st.number_input("Total Datafonos ($)", min_value=0.0, format="%.2f")

        observaciones = st.text_area("Observaciones o Diferencias Encontradas", placeholder="Escribe aquí cualquier novedad del arqueo...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn_guardar = st.form_submit_button("Guardar Registro de Efectivo")
        
        if btn_guardar:
            diferencia = efectivo_fisico - efectivo_sistema
            
            st.success("✅ ¡Registro procesado con éxito!")
            
            # Tarjeta de Resumen del Arqueo
            st.markdown(f"""
                <div class="popsy-card" style="border-left: 5px solid #4CAF50;">
                    <h4 style="color: #2E7D32; margin-top: 0;">Resumen del Arqueo - {pdv}</h4>
                    <p><b>Fecha:</b> {fecha_arqueo}</p>
                    <p><b>Efectivo Físico:</b> ${efectivo_fisico:,.2f}</p>
                    <p><b>Efectivo Sistema:</b> ${efectivo_sistema:,.2f}</p>
                    <p><b>Diferencia:</b> <span style="color: {'red' if diferencia != 0 else 'green'};"><b>${diferencia:,.2f}</b></span></p>
                    <p><b>Consignaciones:</b> ${consignaciones:,.2f} | <b>Datáfono:</b> ${datafonos:,.2f}</p>
                    <p><b>Observaciones:</b> {observaciones if observaciones else 'Ninguna'}</p>
                </div>
            """, unsafe_allow_html=True)

    # Sección de consulta rápida o historial simulado
    st.markdown("---")
    st.markdown("### 📊 Historial Reciente de Arqueos")
    
    # Tabla de ejemplo para ilustrar los registros guardados
    data_ejemplo = {
        "Fecha": ["2026-10-14", "2026-10-14", "2026-10-13"],
        "PDV": ["PDV Andino", "PDV Retiro", "PDV Gran Estación"],
        "Efectivo Físico": [450000, 320000, 510000],
        "Efectivo Sistema": [450000, 325000, 510000],
        "Diferencia": [0, -5000, 0],
        "Estado": ["Cuadrado", "Faltante", "Cuadrado"]
    }
    df_historial = pd.DataFrame(data_ejemplo)
    st.dataframe(df_historial, use_container_width=True)
