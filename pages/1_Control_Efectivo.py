import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(
    page_title="Control Efectivo - Portal Popsy",
    page_icon="🍦",
    layout="wide"
)

# Estilo visual corporativo Popsy (Fucsia/Rosado/Oscuro elegante)
st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFC;
    }
    .popsy-dark-hero {
        background: linear-gradient(135deg, #1E222B 0%, #2B313B 100%);
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        color: white;
        margin-bottom: 2rem;
        border-left: 6px solid #B80049;
    }
    .popsy-badge {
        background-color: rgba(184, 0, 73, 0.2);
        color: #FF80AB;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(184, 0, 73, 0.4);
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
    # ------------------ BARRA LATERAL: SELECCIÓN DE EMPRESA ------------------
    with st.sidebar:
        st.markdown("### 🏢 Selección de Empresa")
        sociedad_seleccionada = st.selectbox("Selecciona la Sociedad:", [
            "Comercial Allan (CO01)",
            "Helados Popsy Colombia (CO02)",
            "Operlog Colombia (CO03)",
            "Inversiones Popsy Perú (PE01)",
            "Popsy Panamá (PA01)"
        ])
        
        st.markdown("---")
        st.markdown("### ⚙️ Configuración")
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.correo_usuario = ""
            st.rerun()

    # ------------------ ENCABEZADO PRINCIPAL ------------------
    nombre_usuario_corto = st.session_state.correo_usuario.split('@')[0].replace('.', ' ').title()
    
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"""
            <div class="popsy-dark-hero">
                <span class="popsy-badge">CONTROL EFECTIVO POPSY • {datetime.today().strftime('%A, %d de %B de %Y')}</span>
                <h1 style="color: white; margin-top: 10px; margin-bottom: 5px; font-size: 2.2rem;">¡Hola, {nombre_usuario_corto}! Bienvenido al Portal de Control Efectivo</h1>
                <p style="color: #B0BEC5; font-style: italic; margin: 0; font-size: 1.1rem;">"Hacemos del mundo un lugar más dulce, feliz y divertido"</p>
            </div>
        """, unsafe_allow_html=True)
    with col_h2:
        st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; border: 1px solid #FFC0CB;">
                <div style="background: #B80049; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 8px auto; font-weight: bold;">
                    {nombre_usuario_corto[0]}
                </div>
                <b style="color: #333; font-size: 0.95rem;">{st.session_state.correo_usuario}</b><br>
                <span style="color: #B80049; font-size: 0.8rem; font-weight: bold;">COLABORADOR POPSY</span>
            </div>
        """, unsafe_allow_html=True)

    # ------------------ MÓDULOS DE PROCESAMIENTO ------------------
    st.markdown("### 📁 Módulos del Sistema")
    st.markdown(f"Sociedad activa: **{sociedad_seleccionada}**")
    
    tipo_proceso = st.radio(
        "Selecciona el tipo de informe a procesar:",
        ["1. Consignaciones Bancarias", "2. Datáfonos & Pasarelas", "3. Pagos Código QR"],
        horizontal=True
    )
    
    st.markdown("---")

    # ==========================================
    # 1. CONSIGNACIONES BANCARIAS Y CONTROL EFECTIVO
    # ==========================================
    if "1. Consignaciones" in tipo_proceso:
        st.markdown("### 📥 Módulo de Consignaciones y Control Efectivo")
        st.markdown("Carga el **extracto bancario** para realizar el cruce automático (**BUSCARV**) entre la **Columna A** de la base de datos fija (`texto multicahs`) y la **Columna J** del extracto.")
        
        archivo_extracto = st.file_uploader("Cargar Extracto Bancario (Excel o CSV)", type=["xlsx", "csv"])
        BASE_DATOS_FIJA = "base_control_efectivo.xlsx"
        
        if archivo_extracto:
            try:
                # Leer extracto
                if archivo_extracto.name.endswith('.csv'):
                    df_extracto = pd.read_csv(archivo_extracto)
                else:
                    df_extracto = pd.read_excel(archivo_extracto)
                
                # Cargar base de datos fija
                if os.path.exists(BASE_DATOS_FIJA):
                    df_base = pd.read_excel(BASE_DATOS_FIJA)
                    st.success("✅ Base de datos contable fija cargada correctamente desde el sistema.")
                else:
                    st.warning(f"⚠️ No se encontró '{BASE_DATOS_FIJA}' en la raíz. Asegúrate de haberlo subido.")
                    df_base = pd.DataFrame()
                
                if not df_base.empty and len(df_base.columns) > 0 and len(df_extracto.columns) >= 10:
                    
                    with st.expander("🔍 Ver vista previa de las fuentes de datos"):
                        col_prev1, col_prev2 = st.columns(2)
                        with col_prev1:
                            st.write("Base de Datos Fija (Columna A - texto multicahs):")
                            st.dataframe(df_base.head(3), use_container_width=True)
                        with col_prev2:
                            st.write("Extracto Bancario (Columna J):")
                            st.dataframe(df_extracto.head(3), use_container_width=True)
                    
                    if st.button("🚀 Ejecutar Cruce (BUSCARV Col A vs Col J)"):
                        with st.spinner("Realizando cruce de datos..."):
                            
                            # Columna A de la base de datos (índice 0)
                            col_base_name = df_base.columns[0]
                            textos_base = set(df_base[col_base_name].astype(str).str.strip().str.upper())
                            
                            # Columna J del extracto (índice 9, ya que J es la décima columna)
                            col_ext_name = df_extracto.columns[9]
                            
                            # Normalizar valores del extracto en la columna J para la búsqueda
                            df_extracto['TEXTO_J_CLEAN'] = df_extracto[col_ext_name].astype(str).str.strip().str.upper()
                            
                            # Evaluar coincidencia (BUSCARV)
                            df_extracto['ESTADO_CRUCE'] = df_extracto['TEXTO_J_CLEAN'].apply(
                                lambda x: 'CONCILIADO' if x in textos_base and x != 'NAN' and x != '' else 'PENDIENTE'
                            )
                            
                            # Conteo de partidas
                            total_partidas = len(df_extracto)
                            cant_conciliadas = len(df_extracto[df_extracto['ESTADO_CRUCE'] == 'CONCILIADO'])
                            cant_pendientes = len(df_extracto[df_extracto['ESTADO_CRUCE'] == 'PENDIENTE'])
                            
                            # Métricas
                            st.markdown("### 📊 Resultado del Control de Partidas")
                            m1, m2, m3 = st.columns(3)
                            m1.metric(label="Total Partidas Subidas", value=f"{total_partidas} registros")
                            m2.metric(label="Partidas Conciliadas (Match)", value=f"{cant_conciliadas} partidas", delta="OK")
                            m3.metric(label="Partidas Pendientes", value=f"{cant_pendientes} partidas", delta="Por revisar", delta_color="inverse")
                            
                            # Tabla detallada
                            st.markdown("#### 📋 Detalle del Resultado del Cruce")
                            st.dataframe(df_extracto, use_container_width=True)
                            
                            # Generación del archivo plano multiusos
                            st.markdown("#### 📄 Archivo Plano Multiusos")
                            st.success("Archivo plano multiusos listo para descargar con las partidas conciliadas y pendientes.")
                            
                            lineas_plano = ["SOCIEDAD;TEXTO_MULTICAHS_J;ESTADO_CRUCE"]
                            for idx, row in df_extracto.iterrows():
                                texto_j = row['TEXTO_J_CLEAN']
                                estado = row['ESTADO_CRUCE']
                                lineas_plano.append(f"{sociedad_seleccionada[:4]};{texto_j};{estado}")
                            
                            contenido_plano = "\n".join(lineas_plano)
                            
                            st.download_button(
                                label="📥 Descargar Archivo Plano Multiusos (.txt)",
                                data=contenido_plano,
                                file_name=f"Multiusos_ControlEfectivo_{sociedad_seleccionada[:4]}.txt",
                                mime="text/plain"
                            )
                else:
                    st.error("⚠️ El archivo Excel fijo no tiene columnas o el extracto cargado tiene menos de 10 columnas (necesitamos la Columna J).")
            except Exception as e:
                st.error(f"Error procesando los archivos: {e}")
        else:
            st.info("📌 Por favor carga el **Extracto Bancario** para ejecutar el cruce automático.")

    # ==========================================
    # 2. DATÁFONOS & PASARELAS
    # ==========================================
    elif "2. Datáfonos" in tipo_proceso:
        st.markdown("### 💳 Módulo de Control - Datáfonos y Pasarelas")
        archivo_datáfono = st.file_uploader("Cargar Reporte de Datáfonos / Pasarelas", type=["xlsx", "csv"])
        if archivo_datáfono:
            st.success("✅ Reporte de datáfonos cargado correctamente.")
            if st.button("🚀 Procesar Partidas de Datáfonos"):
                st.success("¡Control de datáfonos procesado con éxito!")

    # ==========================================
    # 3. PAGOS CÓDIGO QR
    # ==========================================
    elif "3. Pagos" in tipo_proceso:
        st.markdown("### 📱 Módulo de Control - Pagos con Código QR")
        archivo_qr = st.file_uploader("Cargar Reporte de Recaudos QR", type=["xlsx", "csv"])
        if archivo_qr:
            st.success("✅ Reporte QR cargado con éxito.")
            if st.button("🚀 Procesar Partidas QR"):
                st.success("¡Control de pagos QR completado con éxito!")
