import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Control Bancario y Efectivo POPSY",
    page_icon="🍦",
    layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: var(--background-secondary, #FFFFFF);
        padding: 12px 25px;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .brand-logo {
        background-color: #FFF0F5;
        color: #C2185B;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    .user-pill {
        display: flex;
        align-items: center;
        gap: 10px;
        background: var(--background-secondary, #FFFFFF);
        border: 1px solid #E5E7EB;
        padding: 6px 14px;
        border-radius: 30px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .avatar {
        background-color: #C2185B;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
    }
    .user-info {
        display: flex;
        flex-direction: column;
        line-height: 1.2;
    }
    .user-name {
        font-weight: 700;
        font-size: 13px;
    }
    .user-role {
        font-size: 10px;
        font-weight: 700;
        color: #C2185B;
        letter-spacing: 0.5px;
    }
    .hero-banner {
        background: linear-gradient(135deg, #111827 0%, #1F2937 60%, #374151 100%);
        color: white;
        padding: 30px 35px;
        border-radius: 18px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    .badge-tag {
        background-color: rgba(194, 24, 91, 0.25);
        color: #F472B6;
        padding: 5px 14px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 12px;
        border: 1px solid rgba(244, 114, 182, 0.3);
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        margin: 0 0 6px 0;
        color: #FFFFFF !important;
    }
    .hero-sub {
        color: #D1D5DB !important;
        font-size: 14px;
        margin: 0;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# --- VALIDACIÓN DE SESIÓN ---
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.markdown("""
        <div style="background-color: #FFF3CD; padding: 25px; border-radius: 12px; border-left: 6px solid #FFEEBA; text-align: center; margin-top: 50px;">
            <h3 style="color: #856404; margin-top: 0;">⚠️ Acceso Restringido</h3>
            <p style="font-size: 1.1rem; color: #533F03;">Por favor, regresa a la página principal (<b>app.py</b>) e inicia sesión con tu correo corporativo para acceder a este módulo.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    nombre_corto = st.session_state.get('usuario_nombre', st.session_state.correo_usuario.split('@')[0].replace('.', ' ').title())

    # --- TOP BAR SUPERIOR ---
    st.markdown(f"""
        <div class="top-bar">
            <div class="brand-logo">PORTAL CONTABLE POPSY</div>
            <div class="user-pill">
                <div class="avatar">{nombre_corto[0]}</div>
                <div class="user-info">
                    <span class="user-name">{nombre_corto}</span>
                    <span class="user-role">COLABORADOR POPSY</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- HERO BANNER ---
    fecha_actual = datetime.now().strftime('%A, %d de %B de %Y').capitalize()
    st.markdown(f"""
        <div class="hero-banner">
            <div class="badge-tag">🍦 CONTROL BANCARIO & EFECTIVO • {fecha_actual}</div>
            <h1 class="hero-title">¡Hola, {nombre_corto.split()[0]}! Diagnóstico y Conciliación Multicash</h1>
            <p class="hero-sub">"Hacemos del mundo un lugar más dulce, feliz y divertido"</p>
        </div>
    """, unsafe_allow_html=True)

    # --- SIDEBAR: SELECCIÓN DE EMPRESA Y CONFIGURACIÓN ---
    st.sidebar.markdown("### 🏢 Selección de Empresa")
    sociedad_seleccionada = st.sidebar.selectbox(
        "Selecciona la Sociedad:",
        [
            "Comercial Allan (CO01)",
            "Expertos en Café (CO02)",
            "Expertos en Café Peru (PE02 - En Proceso)",
            "Franquicias Unidad del Peru (PE01 - En Proceso)",
            "Panameña de Helados (PA01 - En Proceso)"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Configuración")
    if st.sidebar.button("Cerrar Sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

    if "CO01" in sociedad_seleccionada:
        codigo_sociedad = "CO01"
        nombre_archivo_base = "base_control_efectivo.xlsx"
    elif "CO02" in sociedad_seleccionada:
        codigo_sociedad = "CO02"
        nombre_archivo_base = "base_datos_co02.xlsx"
    else:
        codigo_sociedad = None

    # --- CARGA DEL EXTRACTO Y CLASIFICACIÓN CON BASE UNIFICADA ---
    st.markdown(f"### 📥 Carga de Multicash / Extracto Bancario • {sociedad_seleccionada}")
    
    if codigo_sociedad and os.path.exists(nombre_archivo_base):
        uploaded_multicash = st.file_uploader(f"Sube el Extracto Bancario para Diagnóstico y Procesamiento ({sociedad_seleccionada})", type=["xlsx", "csv"], key="diag_multicash_v2")

        if uploaded_multicash:
            try:
                # Cargar pestañas de la base unificada
                df_base_tiendas = pd.read_excel(nombre_archivo_base, sheet_name='Hoja1')
                df_cuentas_bancos = pd.read_excel(nombre_archivo_base, sheet_name='Cuentas_Bancos')
                
                df_extracto = pd.read_excel(uploaded_multicash) if uploaded_multicash.name.endswith('.xlsx') else pd.read_csv(uploaded_multicash)
                
                # Normalizar nombres de columnas
                df_base_tiendas.columns = [str(c).strip().upper() for c in df_base_tiendas.columns]
                df_cuentas_bancos.columns = [str(c).strip().upper() for c in df_cuentas_bancos.columns]
                df_extracto.columns = [str(c).strip().upper() for c in df_extracto.columns]
                
                # Mapa de búsqueda por TEXTO MULTICASH
                df_base_tiendas['TEXTO_CLEAN'] = df_base_tiendas['TEXTO MULTICAHS'].astype(str).str.strip().str.upper()
                mapa_multicash = {}
                for _, r in df_base_tiendas.iterrows():
                    mapa_multicash[r['TEXTO_CLEAN']] = {
                        'cb_sap': r.get('CB SAP', ''),
                        'pdv_sap': r.get('PDV SAP', ''),
                        'tipificacion': r.get('TIPIFICACION', '')
                    }
                    
                # Detectar columna de texto en el extracto (normalmente Columna J o similar)
                col_ref_ext = df_extracto.columns[min(9, len(df_extracto.columns) - 1)]
                
                def clasificar_con_maestra(row):
                    ref_text = str(row.get(col_ref_ext, '')).strip().upper()
                    
                    # 1. Búsqueda exacta o parcial en Hoja1
                    if ref_text in mapa_multicash:
                        info = mapa_multicash[ref_text]
                        return info['tipificacion'], info['pdv_sap'], info['cb_sap']
                    
                    # Búsqueda por contención
                    for k, info in mapa_multicash.items():
                        if k and k in ref_text:
                            return info['tipificacion'], info['pdv_sap'], info['cb_sap']
                            
                    return 'POR IDENTIFICAR', '', ''

                resultados_clasificacion = df_extracto.apply(clasificar_con_maestra, axis=1)
                df_extracto['TIPIFICACION_DETECTADA'] = [r[0] for r in resultados_clasificacion]
                df_extracto['PDV_SAP'] = [r[1] for r in resultados_clasificacion]
                df_extracto['CB_SAP'] = [r[2] for r in resultados_clasificacion]
                
                total_registros = len(df_extracto)
                df_cons = df_extracto[df_extracto['TIPIFICACION_DETECTADA'] == 'Consignaciones']
                df_dtf = df_extracto[df_extracto['TIPIFICACION_DETECTADA'] == 'Datafonos']
                df_qr = df_extracto[df_extracto['TIPIFICACION_DETECTADA'] == 'QR']
                df_por_id = df_extracto[df_extracto['TIPIFICACION_DETECTADA'] == 'POR IDENTIFICAR']
                
                # --- DASHBOARD DE RESULTADOS DE TIPOS DE OPERACIÓN ---
                st.markdown("#### 📊 Diagnóstico y Clasificación Unificada")
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("📄 Total Extracto", f"{total_registros} partidas")
                m2.metric("🏦 Consignaciones", f"{len(df_cons)} partidas", f"{(len(df_cons)/total_registros)*100:.1f}%")
                m3.metric("💳 Datáfonos", f"{len(df_dtf)} partidas", f"{(len(df_dtf)/total_registros)*100:.1f}%")
                m4.metric("📱 QR", f"{len(df_qr)} partidas", f"{(len(df_qr)/total_registros)*100:.1f}%")
                m5.metric("❓ Por Identificar", f"{len(df_por_id)} partidas", delta_color="inverse")
                
                st.markdown("---")
                
                # --- NAVEGACIÓN EN PESTAÑAS DE DETALLE ---
                t_cons, t_dtf, t_qr, t_pend = st.tabs([
                    "🏦 Consignaciones", 
                    "💳 Datáfonos", 
                    "📱 QR", 
                    "❓ Por Identificar / Cartera"
                ])
                
                with t_cons:
                    st.markdown(f"##### Transacciones Identificadas como Consignaciones ({len(df_cons)})")
                    st.dataframe(df_cons, use_container_width=True)

                with t_dtf:
                    st.markdown(f"##### Transacciones Identificadas como Datáfonos ({len(df_dtf)})")
                    st.dataframe(df_dtf, use_container_width=True)

                with t_qr:
                    st.markdown(f"##### Transacciones Identificadas como Código QR ({len(df_qr)})")
                    st.dataframe(df_qr, use_container_width=True)

                with t_pend:
                    st.markdown(f"##### Transacciones Sin Match Directo / Cartera ({len(df_por_id)})")
                    st.dataframe(df_por_id, use_container_width=True)

            except Exception as e:
                st.error(f"Error procesando la base unificada: {e}")
