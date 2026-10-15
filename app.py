import streamlit as st
import pandas as pd
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Portal Contable POPSY",
    page_icon="🍦",
    layout="wide"
)

# Estilo visual corporativo (Diseño Popsy Fucsia/Rosado)
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #B80049;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555555;
        font-style: italic;
    }
    .stButton>button {
        background-color: #B80049;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #900038;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal con diseño corporativo
st.markdown('<p class="main-header">🍦 Portal Contable POPSY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">"Hacemos del mundo un lugar más dulce, feliz y divertido"</p>', unsafe_allow_html=True)
st.markdown("---")

# Cargar tabla de usuarios y permisos desde Excel de forma segura
USER_EXCEL = "usuarios_permisos.xlsx"

@st.cache_data
def cargar_usuarios():
    if os.path.exists(USER_EXCEL):
        try:
            df = pd.read_excel(USER_EXCEL)
            # Limpiar nombres de columnas por si tienen espacios ocultos
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            st.error(f"Error al leer el archivo Excel de usuarios: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

df_usuarios = cargar_usuarios()

# Control de sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "correo_usuario" not in st.session_state:
    st.session_state.correo_usuario = ""

# Interfaz de Login
if not st.session_state.autenticado:
    st.markdown("### 🔐 Acceso al Sistema Corporativo")
    st.info("Ingresa tu correo corporativo para acceder a los módulos autorizados (@heladospopsy.com).")
    
    with st.form("form_login"):
        correo_ingresado = st.text_input("Correo corporativo (@heladospopsy.com):", placeholder="nombre.apellido@heladospopsy.com")
        btn_ingresar = st.form_submit_button("Ingresar al Portal")
        
        if btn_ingresar:
            correo_limpio = correo_ingresado.strip().lower()
            
            # Validar dominio corporativo
            if not correo_limpio.endswith("@heladospopsy.com"):
                st.error("⚠️ Acceso denegado. Debes utilizar una cuenta de correo corporativa válida (@heladospopsy.com).")
            elif df_usuarios.empty:
                st.error("⚠️ No se encontró la base de datos de usuarios o está vacía.")
            else:
                # Buscar columna de correo de forma flexible (buscando 'correo' o 'email')
                col_correo = None
                for col in df_usuarios.columns:
                    if 'correo' in col.lower() or 'email' in col.lower():
                        col_correo = col
                        break
                
                if col_correo is None:
                    st.error("⚠️ El archivo Excel no contiene una columna identificable de 'correo' o 'email'.")
                else:
                    # Normalizar los correos del Excel para la comparación
                    correos_registrados = df_usuarios[col_correo].astype(str).str.strip().str.lower()
                    
                    if correo_limpio in correos_registrados.values:
                        st.session_state.autenticado = True
                        st.session_state.correo_usuario = correo_limpio
                        st.success("¡Acceso exitoso! Cargando portal...")
                        st.rerun()
                    else:
                        st.error("⚠️ Este correo no cuenta con permisos registrados en el sistema.")
else:
    # Pantalla principal una vez autenticado
    st.success(f"Bienvenida al sistema, **{st.session_state.correo_usuario}**")
    
    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.session_state.correo_usuario = ""
        st.rerun()
        
    st.markdown("---")
    st.markdown("### Módulos Disponibles")
    st.markdown("Utiliza el menú lateral izquierdo para navegar entre los diferentes módulos de control efectivo, legalizaciones y visualización de ventas.")
