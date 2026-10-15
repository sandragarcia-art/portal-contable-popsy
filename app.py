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
    .stApp {
        background-color: #FAFAFC;
    }
    
    /* Banner de bienvenida estilo Popsy */
    .popsy-hero {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(184, 0, 73, 0.08);
        text-align: center;
        border: 2px solid #FFC0CB;
        margin-bottom: 1.5rem;
    }
    
    .main-title {
        font-size: 2.8rem;
        color: #B80049;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    
    .sub-title {
        font-size: 1.2rem;
        color: #666666;
        font-style: italic;
    }

    /* Tarjetas de contenido */
    .popsy-card {
        background: white;
        padding: 1.8rem;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
        border-left: 6px solid #B80049;
        margin-bottom: 1.5rem;
    }
    
    /* Botón personalizado fucsia Popsy */
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

# Encabezado principal tipo Banner
st.markdown("""
    <div class="popsy-hero">
        <div class="main-title">🍦 Portal Contable POPSY</div>
        <div class="sub-title">"Hacemos del mundo un lugar más dulce, feliz y divertido"</div>
    </div>
""", unsafe_allow_html=True)

# Cargar tabla de usuarios y permisos desde Excel de forma segura
USER_EXCEL = "usuarios_permisos.xlsx"

@st.cache_data
def cargar_usuarios():
    if os.path.exists(USER_EXCEL):
        try:
            df = pd.read_excel(USER_EXCEL)
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

# Interfaz de Login o Panel Principal
if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
            <div class="popsy-card" style="border-left: 6px solid #B80049; text-align: center;">
                <h3 style="color: #B80049; margin-bottom: 0.5rem;">🔐 Acceso Corporativo</h3>
                <p style="color: #555; font-size: 0.95rem;">Ingresa tu correo autorizado para continuar.</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_login"):
            correo_ingresado = st.text_input("Correo corporativo:", placeholder="nombre.apellido@heladospopsy.com")
            st.markdown("<br>", unsafe_allow_html=True)
            btn_ingresar = st.form_submit_button("Ingresar al Portal")
            
            if btn_ingresar:
                correo_limpio = correo_ingresado.strip().lower()
                
                if not correo_limpio.endswith("@heladospopsy.com"):
                    st.error("⚠️ Acceso denegado. Debe ser una cuenta oficial (@heladospopsy.com).")
                elif df_usuarios.empty:
                    st.error("⚠️ Base de datos de usuarios no disponible.")
                else:
                    col_correo = None
                    for col in df_usuarios.columns:
                        if 'correo' in col.lower() or 'email' in col.lower():
                            col_correo = col
                            break
                    
                    if col_correo is None:
                        st.error("⚠️ El Excel no contiene una columna de correo válida.")
                    else:
                        correos_registrados = df_usuarios[col_correo].astype(str).str.strip().str.lower()
                        
                        if correo_limpio in correos_registrados.values:
                            st.session_state.autenticado = True
                            st.session_state.correo_usuario = correo_limpio
                            st.success("¡Bienvenida! Ingresando al sistema...")
                            st.rerun()
                        else:
                            st.error("⚠️ Este correo no cuenta con permisos registrados.")
else:
    # 1. PRIMERO: Mostrar correo corporativo autenticado y botón de salir
    st.markdown(f"""
        <div class="popsy-card">
            <h4 style="color: #B80049; margin-top: 0;">👤 Sesión Activa</h4>
            <p style="font-size: 1.1rem; color: #333; margin-bottom: 0.5rem;">Correo corporativo: <b>{st.session_state.correo_usuario}</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.correo_usuario = ""
            st.rerun()
            
    st.markdown("---")
    
    # 2. SEGUNDO: Mostrar los Módulos Disponibles de forma destacada
    st.markdown("""
        <div class="popsy-card" style="border-left: 6px solid #FF4081;">
            <h3 style="color: #B80049; margin-top: 0;">🚀 Módulos Disponibles</h3>
            <p style="color: #555; font-size: 1.05rem; line-height: 1.5;">
                Bienvenida al sistema integrado. Utiliza el menú lateral izquierdo para navegar e ingresar a los diferentes módulos de control:
            </p>
            <ul style="color: #444; font-size: 1rem; line-height: 1.6;">
                <li><b>Control Efectivo:</b> Gestión y arqueos de efectivo.</li>
                <li><b>Legalizaciones PDV:</b> Registro y control de gastos por punto de venta.</li>
                <li><b>Visualización Ventas:</b> Tableros de análisis y reportes financieros.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
