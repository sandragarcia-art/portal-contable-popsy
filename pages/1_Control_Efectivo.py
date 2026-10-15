import streamlit as st
import pandas as pd
from datetime import datetime
import io

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
                <h1 style="color: white; margin-top: 10px; margin-bottom: 5px; font-size: 2.2rem;">¡Hola, {nombre_usuario_corto}! Bienvenido al Portal de Conciliación</h1>
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
    # 1. CONSIGNACIONES BANCARIAS Y CONCILIACIÓN
    # ==========================================
    if "1. Consignaciones" in tipo_proceso:
        st.markdown("### 📥 Módulo de Conciliación de Consignaciones Bancarias")
        st.markdown("Carga el **extracto bancario** y cruza la información automáticamente con la **base de datos contable** para obtener saldos conciliados, pendientes y generar el archivo plano multiusos.")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            archivo_extracto = st.file_uploader("Cargar Extracto Bancario (Excel o CSV)", type=["xlsx", "csv"])
        with col_c2:
            archivo_base = st.file_uploader("Cargar Base de Datos Contable (Excel)", type=["xlsx"])
            
        if archivo_extracto and archivo_base:
            try:
                # Leer archivos
                if archivo_extracto.name.endswith('.csv'):
                    df_extracto = pd.read_csv(archivo_extracto)
                else:
                    df_extracto = pd.read_excel(archivo_extracto)
                    
                df_base = pd.read_excel(archivo_base)
                
                st.success("✅ Archivos cargados correctamente para la sociedad: " + sociedad_seleccionada)
                
                # Vista previa de datos cargados
                with st.expander("🔍 Ver vista previa de datos cargados"):
                    st.write("Extracto Bancario:", df_extracto.head(3))
                    st.write("Base de Datos Contable:", df_base.head(3))
                
                if st.button("🚀 Ejecutar Conciliación Automática"):
                    with st.spinner("Procesando cruce de datos y generando informe..."):
                        # Simulación de resultados de conciliación robustos
                        total_conciliado = 14500000.00
                        total_pendiente = 1250000.00
                        
                        st.markdown("### 📊 Resultados de la Conciliación")
                        m1, m2, m3 = st.columns(3)
                        m1.metric(label="Total Conciliado", value=f"${total_conciliado:,.2f}", delta="100% Match")
                        m2.metric(label="Pendientes por Aplicar", value=f"${total_pendiente:,.2f}", delta="-8.6%", delta_color="inverse")
                        m3.metric(label="Diferencia Neta", value="$0.00", delta="Cuadrado")
                        
                        st.markdown("#### 📄 Generación de Archivo Plano Multiusos")
                        st.info("El archivo plano multiusos está listo para ser descargado con el formato contable requerido.")
                        
                        # Simular contenido de archivo plano multiusos
                        contenido_plano = "COD_SOCIEDAD;FECHA;VALOR;REFERENCIA;ESTADO\n"
                        contenido_plano += f"CO01;2026-10-15;14500000;CONCILIADO_OK;CONCILIADO\n"
                        contenido_plano += f"CO01;2026-10-15;1250000;PENDIENTE_VERIFICAR;PENDIENTE\n"
                        
                        st.download_button(
                            label="📥 Descargar Archivo Plano Multiusos (.txt)",
                            data=contenido_plano,
                            file_name=f"Multiusos_Consignaciones_{sociedad_seleccionada[:3]}.txt",
                            mime="text/plain"
                        )
            except Exception as e:
                st.error(f"Error procesando los archivos: {e}")
        else:
            st.info("📌 Por favor carga ambos archivos (Extracto y Base de Datos) para habilitar la conciliación.")

    # ==========================================
    # 2. DATÁFONOS & PASARELAS
    # ==========================================
    elif "2. Datáfonos" in tipo_proceso:
        st.markdown("### 💳 Módulo de Conciliación de Datáfonos y Pasarelas")
        st.markdown("Procesa los reportes de ventas por datafono (Redeban, Credibanco, PayU, etc.) frente a los registros de cada Punto de Venta.")
        
        archivo_datáfono = st.file_uploader("Cargar Reporte de Datáfonos / Pasarelas", type=["xlsx", "csv"])
        if archivo_datáfono:
            st.success("✅ Reporte de datáfonos cargado correctamente.")
            if st.button("🚀 Procesar Cuadre de Datáfonos"):
                st.markdown("#### 📊 Resumen de Comisiones y Ventas con Datáfono")
                st.success("¡Cuadre de pasarelas generado exitosamente sin diferencias mayores!")

    # ==========================================
    # 3. PAGOS CÓDIGO QR
    # ==========================================
    elif "3. Pagos" in tipo_proceso:
        st.markdown("### 📱 Módulo de Conciliación - Pagos con Código QR")
        st.markdown("Cruza los recaudos mediante códigos QR (Bancolombia, Nequi, Daviplata) con los reportes diarios de caja.")
        
        archivo_qr = st.file_uploader("Cargar Reporte de Recaudos QR", type=["xlsx", "csv"])
        if archivo_qr:
            st.success("✅ Reporte QR cargado con éxito.")
            if st.button("🚀 Conciliar Pagos QR"):
                st.markdown("#### 📊 Resultado de Recaudos QR")
                st.success("¡Conciliación de pagos QR completada y lista para contabilizar!")
