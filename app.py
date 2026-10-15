import streamlit as st
import pandas as pd
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Portal Contable POPSY",
    page_icon="🍦",
    layout="wide"
)

st.title("🍦 Portal Contable POPSY")
st.markdown("### Sistema Integrado de Gestión Contable y Financiera")
st.markdown("---")

# Cargar tabla de usuarios y permisos desde Excel
USER_EXCEL = "usuarios_permisos.xlsx"

def cargar_usuarios():
    if os.path.exists(USER_EXCEL):
        return pd.read_excel(USER_EXCEL)
    else:
        # Respaldo por defecto en caso de no encontrar el Excel
        return pd.DataFrame({
            'correo': ['sandra.garcia@popsy.com.co'],
            'nombre': ['Sandra García'],
            'rol': ['Administrador'],
            'estado': ['Activo']
        })

df_usuarios = cargar_usuarios()

# Estado de la sesión
if "usuario_autenticado" not in st.session_state:
    st.session_state.usuario_autenticado = False
    st.session_state.datos_usuario = None

# ----------------------------------------------------
# 1. PANTALLA DE INICIO DE SESIÓN
# ----------------------------------------------------
if not st.session_state.usuario_autenticado:
    col_login, _ = st.columns([1, 1])
    with col_login:
        st.info("🔐 Ingresa tu correo corporativo para acceder a los módulos autorizados.")
        
        with st.form("login_form"):
            correo_input = st.text_input("Correo corporativo:").strip().lower()
            btn_ingresar = st.form_submit_button("Ingresar al Portal")
            
            if btn_ingresar:
                if correo_input:
                    usuario_match = df_usuarios[
                        (df_usuarios['correo'].str.strip().str.lower() == correo_input) & 
                        (df_usuarios['estado'].str.strip().str.lower() == 'activo')
                    ]
                    
                    if not usuario_match.empty:
                        st.session_state.usuario_autenticado = True
                        st.session_state.datos_usuario = usuario_match.iloc[0].to_dict()
                        st.rerun()
                    else:
                        st.error("❌ Correo no registrado o inactivo. Contacta al administrador.")
                else:
                    st.warning("Por favor ingresa un correo válido.")

# ----------------------------------------------------
# 2. PANEL PRINCIPAL Y VISUALIZACIÓN DE MÓDULOS
# ----------------------------------------------------
else:
    user = st.session_state.datos_usuario
    rol_actual = user['rol']
    
    # Barra lateral de información
    st.sidebar.markdown("### 👤 Perfil de Usuario")
    st.sidebar.write(f"**Nombre:** {user['nombre']}")
    st.sidebar.write(f"**Rol:** `{rol_actual}`")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔴 Cerrar Sesión"):
        st.session_state.usuario_autenticado = False
        st.session_state.datos_usuario = None
        st.rerun()

    st.success(f"¡Bienvenido/a, **{user['nombre']}**!")
    st.markdown("### 📌 Módulos Activos del Portal")
    st.caption("A continuación se presentan los módulos disponibles. Navega desde la barra lateral izquierda hacia tus módulos autorizados.")

    st.write("")

    # Definición de Módulos
    modulos = [
        {
            "titulo": "💵 Control de Efectivo",
            "descripcion": "Conciliación bancaria y cuadre de cajas multi-sociedad (CO01 / CO02).",
            "roles_permitidos": ["Administrador", "Contabilidad"]
        },
        {
            "titulo": "🧾 Legalizaciones PDV",
            "descripcion": "Recepción, auditoría y soporte de cajas menores y gastos de Puntos de Venta.",
            "roles_permitidos": ["Administrador", "Contabilidad", "PDV"]
        },
        {
            "titulo": "📊 Visualización de Ventas",
            "descripcion": "Análisis contable, métricas e ingresos por tienda.",
            "roles_permitidos": ["Administrador", "Contabilidad"]
        }
    ]

    cols = st.columns(3)

    for i, mod in enumerate(modulos):
        with cols[i % 3]:
            tiene_permiso = rol_actual in mod["roles_permitidos"]
            
            with st.container(border=True):
                st.subheader(mod["titulo"])
                st.write(mod["descripcion"])
                st.markdown("---")
                
                if tiene_permiso:
                    st.markdown("✅ **Acceso Autorizado**")
                    st.info("👉 Disponible en el menú lateral.")
                else:
                    st.markdown("🔒 **Acceso Restringido**")
                    st.caption(f"Disponible para roles: *{', '.join(mod['roles_permitidos'])}*")