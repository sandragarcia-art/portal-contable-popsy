import streamlit as st
import pandas as pd
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Portal Contable POPSY",
    page_icon="🍦",
    layout="wide"
)

# Estilo visual corporativo e imponente estilo Popsy
st.markdown("""
    <style>
    /* Fondo general sutil */
    .stApp {
        background-color: #FAFAFC;
    }
    
    /* Contenedor principal de bienvenida */
    .popsy-hero {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(184, 0, 73, 0.08);
        text-align: center;
        border: 2px solid #FFC0CB;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3rem;
        color: #B80049;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    
    .sub-title {
        font-size: 1.3rem;
        color: #666666;
        font-style: italic;
        font-weight: 500;
    }

    /* Estilo para los contenedores de acceso */
    .login-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border-top: 5px solid #B80049;
    }
    
    /* Botón personalizado fucsia Popsy */
    .stButton>button {
        background: linear-gradient(135deg, #B80049 0%, #D81B60 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        border: none;
        width: 100%;
        box-shadow: 0 4px 12px rgba(184, 0, 73, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #900038 0%, #B80049 100%);
        box-shadow: 0 6px 16px rgba(184, 0, 73, 0.3);
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Sección de Bienvenida Impactante tipo Banner
st.markdown("""
