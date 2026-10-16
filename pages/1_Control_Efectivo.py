import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import altair as alt
from io import BytesIO

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
    .metric-card {
        background: white;
        border: 1px solid #E5E7EB;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        text-align: center;
    }
    .metric-title {
        font-size: 12px;
        font-weight: 700;
        color: #6B7280;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .metric-val {
        font-size: 16px;
        font-weight: 800;
        color: #1F2937;
    }
    .metric-sub {
        font-size: 14px;
        font-weight: 700;
        color: #C2185B;
        margin-top: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# --- GESTIÓN DE HISTÓRICO Y NOTAS EN SESIÓN Y EXCEL ---
ARCHIVO_HISTORICO = "historico_cierres.xlsx"

def cargar_historico_excel():
    if os.path.exists(ARCHIVO_HISTORICO):
        try:
            return pd.read_excel(ARCHIVO_HISTORICO).to_dict('records')
        except:
            return []
    return []

if "notas_partidas" not in st.session_state:
    st.session_state.notas_partidas = {}

# --- VALIDACIÓN DE SESIÓN Y REDIRECCIÓN AUTOMÁTICA ---
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.warning("⚠️ No se detectó una sesión activa. Redirigiendo al inicio de sesión...")
    st.switch_page("app.py")
else:
    nombre_corto = st.session_state.get('usuario_nombre', st.session_state.correo_usuario.split('@')[0].replace('.', ' ').title())

    # --- TOP BAR SUPERIOR ---
    st.markdown(f"""
        <div class="top-bar">
            <div class="brand-logo">CONTROL EFECTIVO POPSY</div>
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
            <div class="badge-tag">🍦 CONTROL EFECTIVO & PLANOS SAP • {fecha_actual}</div>
            <h1 class="hero-title">¡Hola, {nombre_corto.split()[0]}! Bienvenido a Cruce Bancario de Control Efectivo</h1>
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

    # CONFIGURACIÓN DINÁMICA SEGÚN SOCIEDAD
    if "CO01" in sociedad_seleccionada:
        codigo_sociedad = "CO01"
        nombre_archivo_base = "base_control_efectivo.xlsx"
        nombre_archivo_matriz_dtf = "base_datafonos.xlsx"
        nombre_archivo_comercios = "Comercio Datafonos.xlsx"
        maneja_qr = True
    elif "CO02" in sociedad_seleccionada:
        codigo_sociedad = "CO02"
        nombre_archivo_base = "base_datos_co02.xlsx"
        nombre_archivo_matriz_dtf = "base_datafonos_co02.xlsx"
        nombre_archivo_comercios = "Comercio Datafonos_co02.xlsx"
        maneja_qr = False
    else:
        codigo_sociedad = None

    # ACTUALIZADOR DE BASES MAESTRAS EN EL SIDEBAR
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Gestión de Maestros")
    with st.sidebar.expander("📂 Cargar / Actualizar Maestros"):
        up_base_custom = st.file_uploader("Actualizar Base Tiendas Multicash", type=["xlsx", "xls"], key="up_m_tiendas")
        if up_base_custom:
            try:
                with open(nombre_archivo_base, "wb") as f:
                    f.write(up_base_custom.getbuffer())
                st.success("✅ Base de Tiendas actualizada!")
            except Exception as e:
                st.error(f"Error guardando maestro: {e}")

        up_dtf_custom = st.file_uploader("Actualizar Matriz Datáfonos", type=["xlsx", "xls"], key="up_m_dtf")
        if up_dtf_custom:
            try:
                with open(nombre_archivo_matriz_dtf, "wb") as f:
                    f.write(up_dtf_custom.getbuffer())
                st.success("✅ Matriz Datáfonos actualizada!")
            except Exception as e:
                st.error(f"Error guardando maestro: {e}")

    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

    # --- FUNCIONES DE GENERACIÓN DE PLANOS ---
    def generar_plano_multiusos_consignaciones(df_filtrado, codigo_sociedad):
        columnas_multiusos = [
            'ID', 'USUARIO', 'LEDGER', 'FECHA DOC', 'CLASE DOCUMENTO', 'SOCIEDAD', 'FECHA CONT',
            'FECHA REG', 'MONEDA TR', 'TASA DE CAMBIO', 'REFERENCIA', 'TEXTO CABECERA',
            'IDENTIFICADOR PI', 'POSICION', 'CLAVE CONTABILIZACION', 'CUENTA DE MAYOR',
            'CLASE DE CUENTA', 'PROVEEDOR', 'CLIENTE', 'PAGADOR ALTERNATIVO', 'INDICADOR CME',
            'VALOR TR', 'IND IVA', 'CALCULAR IMP. AUTOMATICO', 'FECHA BASE', 'CONDICION PAGO',
            'FECHA VALOR', 'Orden de Compra', 'Posicion OC', 'ORDEN', 'CECO', 'CEBE', 'GRAFO',
            'OPERACION GRAFO', 'ELEMENTO PEP', 'ASIGNACION', 'CLAVE DE REF_1', 'CLAVE DE REF_2',
            'CLAVE DE REF_3', 'TEXTO POSICION', 'INDICADOR TP. RETENCIONES 1', 'INDICADOR RETENCION  1',
            'BASE RETENCION 1', 'BASE RETENCION DOC 1', 'INDICADOR TP. RETENCIONES 2', 'INDICADOR RETENCION  2',
            'BASE RETENCION 2', 'BASE RETENCION DOC 2', 'INDICADOR TP. RETENCIONES 3', 'INDICADOR RETENCION  3',
            'BASE RETENCION 3', 'BASE RETENCION DOC 3', 'INDICADOR TP. RETENCIONES 4', 'INDICADOR RETENCION  4',
            'BASE RETENCION 4', 'BASE RETENCION DOC4', 'INDICADOR TP. RETENCIONES 5', 'INDICADOR RETENCION  5',
            'BASE RETENCION 5', 'BASE RETENCION DOC 5', 'AÑO', 'MES', 'MONEDA', 'OBJETO COSTO',
            'CLASE DE ACTIVIDAD', 'POSICION DE LA ORDEN', 'HOJA DE RUTA', 'SEGMENTO', 'PRODUCTO',
            'OF VENTAS', 'CLIENTE CAR', 'CLASE MEDIO DE TRANSPORTE', 'ZONA', 'MEDIO DE TRANSPORTE',
            'GRUPO MATERIAL 1', 'GRUPO MATERIAL 2', 'GRUPO MATERIAL 3', 'GRUPO MATERIAL 4',
            'VALOR LC', 'FECHA RFERENCIA PAGO', 'DOCUMENTO REFERENCIA', 'FECHA REFERENCIA', 'BLOQUEO PAGO'
        ]
        
        filas = []
        fecha_hoy = datetime.now().strftime('%d.%m.%Y')
        cuenta_banco_default = 11100511
        cuenta_ingreso_default = 11050502
        nit_corporativo = "8600538311"
        
        col_ref = df_filtrado.columns[min(9, len(df_filtrado.columns) - 1)]
        col_fec = next((c for c in df_filtrado.columns if 'fecha' in c.lower() or 'date' in c.lower()), None)
        col_cta = df_filtrado.columns[1] if len(df_filtrado.columns) > 1 else None

        for idx, (_, row) in enumerate(df_filtrado.iterrows(), start=1):
            ref_val = str(row.get(col_ref, row.iloc[0])).strip()
            
            cuenta_banco_val = cuenta_banco_default
            if col_cta and col_cta in row and pd.notna(row[col_cta]):
                try:
                    cuenta_banco_val = int(float(str(row[col_cta]).strip()))
                except:
                    pass

            fecha_doc = fecha_hoy
            if col_fec and col_fec in row and pd.notna(row[col_fec]):
                val_fec = row[col_fec]
                if isinstance(val_fec, datetime):
                    fecha_doc = val_fec.strftime('%d.%m.%Y')
                else:
                    try:
                        parsed = pd.to_datetime(str(val_fec).strip())
                        if pd.notna(parsed):
                            fecha_doc = parsed.strftime('%d.%m.%Y')
                    except:
                        pass

            cebe_val = str(row.get('CB_SAP', ''))
            pdv_val = str(row.get('PDV_SAP', ''))
            
            val_raw = row.get('VALOR_LIMPIO', 0)
            try:
                valor_val = int(round(abs(float(val_raw))))
            except:
                valor_val = 0
                
            if valor_val <= 0:
                continue
                
            texto_pos = f"{fecha_doc} CG {pdv_val}"
            
            p1 = {c: None for c in columnas_multiusos}
            p1.update({
                'ID': idx, 'FECHA DOC': fecha_doc, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                'FECHA CONT': fecha_doc, 'FECHA REG': fecha_doc, 'MONEDA TR': 'COP',
                'REFERENCIA': ref_val, 'TEXTO CABECERA': f"CG {ref_val}",
                'IDENTIFICADOR PI': idx, 'POSICION': 1, 'CLAVE CONTABILIZACION': 50,
                'CUENTA DE MAYOR': cuenta_banco_val, 'VALOR TR': valor_val, 'CEBE': cebe_val,
                'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_pos
            })
            
            p2 = {c: None for c in columnas_multiusos}
            p2.update({
                'ID': idx, 'FECHA DOC': fecha_doc, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                'FECHA CONT': fecha_doc, 'FECHA REG': fecha_doc, 'MONEDA TR': 'COP',
                'REFERENCIA': ref_val, 'TEXTO CABECERA': f"CG {ref_val}",
                'IDENTIFICADOR PI': idx, 'POSICION': 2, 'CLAVE CONTABILIZACION': 40,
                'CUENTA DE MAYOR': cuenta_ingreso_default, 'VALOR TR': valor_val, 'CEBE': cebe_val,
                'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_pos
            })
            
            filas.append(p1)
            filas.append(p2)
            
        return pd.DataFrame(filas)[columnas_multiusos]

    def generar_plano_multiusos_datafonos(df_filtrado, df_matriz_dtf, codigo_sociedad):
        columnas_multiusos = [
            'ID', 'USUARIO', 'LEDGER', 'FECHA DOC', 'CLASE DOCUMENTO', 'SOCIEDAD', 'FECHA CONT',
            'FECHA REG', 'MONEDA TR', 'TASA DE CAMBIO', 'REFERENCIA', 'TEXTO CABECERA',
            'IDENTIFICADOR PI', 'POSICION', 'CLAVE CONTABILIZACION', 'CUENTA DE MAYOR',
            'CLASE DE CUENTA', 'PROVEEDOR', 'CLIENTE', 'PAGADOR ALTERNATIVO', 'INDICADOR CME',
            'VALOR TR', 'IND IVA', 'CALCULAR IMP. AUTOMATICO', 'FECHA BASE', 'CONDICION PAGO',
            'FECHA VALOR', 'Orden de Compra', 'Posicion OC', 'ORDEN', 'CECO', 'CEBE', 'GRAFO',
            'OPERACION GRAFO', 'ELEMENTO PEP', 'ASIGNACION', 'CLAVE DE REF_1', 'CLAVE DE REF_2',
            'CLAVE DE REF_3', 'TEXTO POSICION', 'INDICADOR TP. RETENCIONES 1', 'INDICADOR RETENCION  1',
            'BASE RETENCION 1', 'BASE RETENCION DOC 1', 'INDICADOR TP. RETENCIONES 2', 'INDICADOR RETENCION  2',
            'BASE RETENCION 2', 'BASE RETENCION DOC 2', 'INDICADOR TP. RETENCIONES 3', 'INDICADOR RETENCION  3',
            'BASE RETENCION 3', 'BASE RETENCION DOC 3', 'INDICADOR TP. RETENCIONES 4', 'INDICADOR RETENCION  4',
            'BASE RETENCION 4', 'BASE RETENCION DOC4', 'INDICADOR TP. RETENCIONES 5', 'INDICADOR RETENCION  5',
            'BASE RETENCION 5', 'BASE RETENCION DOC 5', 'AÑO', 'MES', 'MONEDA', 'OBJETO COSTO',
            'CLASE DE ACTIVIDAD', 'POSICION DE LA ORDEN', 'HOJA DE RUTA', 'SEGMENTO', 'PRODUCTO',
            'OF VENTAS', 'CLIENTE CAR', 'CLASE MEDIO DE TRANSPORTE', 'ZONA', 'MEDIO DE TRANSPORTE',
            'GRUPO MATERIAL 1', 'GRUPO MATERIAL 2', 'GRUPO MATERIAL 3', 'GRUPO MATERIAL 4',
            'VALOR LC', 'FECHA RFERENCIA PAGO', 'DOCUMENTO REFERENCIA', 'FECHA REFERENCIA', 'BLOQUEO PAGO'
        ]
        
        filas = []
        fecha_hoy = datetime.now().strftime('%d.%m.%Y')
        nit_corporativo = "8600538311"
        
        mapa_columnas_vlr = {
            'Vlr Abono': 'VLR ABONO',
            'Vlr Comision': 'VLR COMISION',
            'Vlr Rete Fuente': 'VLR RETE FUENTE',
            'Vlr Rete Ica': 'VLR RETE ICA',
            'Vlr Rete Iva': 'VLR RETE IVA',
            'Vlr Total': 'VLR TOTAL'
        }

        for idx, (_, row) in enumerate(df_filtrado.iterrows(), start=1):
            trn_val = int(row.get('TRN', 6))
            comercio_val = str(row.get('COMERCIO', idx)).strip()
            
            fecha_doc = fecha_hoy
            val_fec = row.get('F ABONO', row.get('F PROCESO', None))
            if pd.notna(val_fec):
                try:
                    fec_str = str(val_fec).strip()
                    parsed = pd.to_datetime(fec_str)
                    if pd.notna(parsed):
                        fecha_doc = parsed.strftime('%d.%m.%Y')
                except:
                    pass

            pdv_val = str(row.get('PDV_SAP', ''))
            cebe_val = str(row.get('CB', ''))
            
            filas_matriz = df_matriz_dtf[df_matriz_dtf['TRN'] == trn_val]
            
            pos_efectiva = 1
            for _, m_row in filas_matriz.iterrows():
                tipo_cta = str(m_row['TIPO CUENTA']).strip()
                cuenta_sap = int(m_row['CUENTA SAP'])
                cc_sap = int(m_row['CC SAP'])
                
                col_plano = mapa_columnas_vlr.get(tipo_cta, None)
                val_raw = row.get(col_plano, 0) if col_plano else 0
                try:
                    valor_val = int(round(abs(float(val_raw))))
                except:
                    valor_val = 0
                
                if valor_val == 0:
                    continue
                
                texto_pos = f"{fecha_doc} DTF {pdv_val}"
                
                p = {c: None for c in columnas_multiusos}
                p.update({
                    'ID': idx, 'FECHA DOC': fecha_doc, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                    'FECHA CONT': fecha_doc, 'FECHA REG': fecha_doc, 'MONEDA TR': 'COP',
                    'REFERENCIA': comercio_val, 'TEXTO CABECERA': f"DTF {comercio_val}",
                    'IDENTIFICADOR PI': idx, 'POSICION': pos_efectiva, 'CLAVE CONTABILIZACION': cc_sap,
                    'CUENTA DE MAYOR': cuenta_sap, 'VALOR TR': valor_val, 'CEBE': cebe_val,
                    'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_pos
                })
                filas.append(p)
                pos_efectiva += 1
            
        return pd.DataFrame(filas)[columnas_multiusos]

    def generar_plano_multiusos_qr(df_filtrado, df_matriz_dtf, codigo_sociedad):
        columnas_multiusos = [
            'ID', 'USUARIO', 'LEDGER', 'FECHA DOC', 'CLASE DOCUMENTO', 'SOCIEDAD', 'FECHA CONT',
            'FECHA REG', 'MONEDA TR', 'TASA DE CAMBIO', 'REFERENCIA', 'TEXTO CABECERA',
            'IDENTIFICADOR PI', 'POSICION', 'CLAVE CONTABILIZACION', 'CUENTA DE MAYOR',
            'CLASE DE CUENTA', 'PROVEEDOR', 'CLIENTE', 'PAGADOR ALTERNATIVO', 'INDICADOR CME',
            'VALOR TR', 'IND IVA', 'CALCULAR IMP. AUTOMATICO', 'FECHA BASE', 'CONDICION PAGO',
            'FECHA VALOR', 'Orden de Compra', 'Posicion OC', 'ORDEN', 'CECO', 'CEBE', 'GRAFO',
            'OPERACION GRAFO', 'ELEMENTO PEP', 'ASIGNACION', 'CLAVE DE REF_1', 'CLAVE DE REF_2',
            'CLAVE DE REF_3', 'TEXTO POSICION', 'INDICADOR TP. RETENCIONES 1', 'INDICADOR RETENCION  1',
            'BASE RETENCION 1', 'BASE RETENCION DOC 1', 'INDICADOR TP. RETENCIONES 2', 'INDICADOR RETENCION  2',
            'BASE RETENCION 2', 'BASE RETENCION DOC 2', 'INDICADOR TP. RETENCIONES 3', 'INDICADOR RETENCION  3',
            'BASE RETENCION 3', 'BASE RETENCION DOC 3', 'INDICADOR TP. RETENCIONES 4', 'INDICADOR RETENCION  4',
            'BASE RETENCION 4', 'BASE RETENCION DOC4', 'INDICADOR TP. RETENCIONES 5', 'INDICADOR RETENCION  5',
            'BASE RETENCION 5', 'BASE RETENCION DOC 5', 'AÑO', 'MES', 'MONEDA', 'OBJETO COSTO',
            'CLASE DE ACTIVIDAD', 'POSICION DE LA ORDEN', 'HOJA DE RUTA', 'SEGMENTO', 'PRODUCTO',
            'OF VENTAS', 'CLIENTE CAR', 'CLASE MEDIO DE TRANSPORTE', 'ZONA', 'MEDIO DE TRANSPORTE',
            'GRUPO MATERIAL 1', 'GRUPO MATERIAL 2', 'GRUPO MATERIAL 3', 'GRUPO MATERIAL 4',
            'VALOR LC', 'FECHA RFERENCIA PAGO', 'DOCUMENTO REFERENCIA', 'FECHA REFERENCIA', 'BLOQUEO PAGO'
        ]
        
        filas = []
        fecha_hoy = datetime.now().strftime('%d.%m.%Y')
        nit_corporativo = "8600538311"
        
        mapa_columnas_vlr = {
            'Vlr Abono': 'VALOR TOTAL',
            'Vlr Comision': 'VALOR COMISION',
            'Vlr Total': 'VALOR TOTAL',
            'Vlr Rete Fuente': 'VALOR RETE FUENTE',
            'Vlr Rete Ica': 'VALOR RETE ICA',
            'Vlr Rete Iva': 'VALOR RETE IVA'
        }

        for idx, (_, row) in enumerate(df_filtrado.iterrows(), start=1):
            comercio_val = str(row.get('CODIGO UNICO', idx)).strip()
            
            fecha_doc = fecha_hoy
            val_fec = row.get('FECHA DE CONSUMO', None)
            if pd.notna(val_fec):
                try:
                    fec_str = str(int(val_fec)) if isinstance(val_fec, (int, float)) else str(val_fec).strip()
                    parsed = pd.to_datetime(fec_str, format='%Y%m%d', errors='coerce')
                    if pd.notna(parsed):
                        fecha_doc = parsed.strftime('%d.%m.%Y')
                except:
                    pass

            pdv_val = str(row.get('PDV_SAP', ''))
            cebe_val = str(row.get('CB', ''))
            
            filas_matriz = df_matriz_dtf[df_matriz_dtf['TRN'] == 6]
            if len(filas_matriz) == 0:
                filas_matriz = df_matriz_dtf
            
            pos_efectiva = 1
            for _, m_row in filas_matriz.iterrows():
                tipo_cta = str(m_row['TIPO CUENTA']).strip()
                cuenta_sap = int(m_row['CUENTA SAP'])
                cc_sap = int(m_row['CC SAP'])
                
                col_plano = None
                for k, v in mapa_columnas_vlr.items():
                    if k.lower() in tipo_cta.lower():
                        col_plano = v
                        break
                if not col_plano:
                    col_plano = 'VALOR TOTAL' if 'total' in tipo_cta.lower() else 'VALOR COMISION'
                
                val_raw = row.get(col_plano, 0) if col_plano in row else 0
                try:
                    valor_val = int(round(abs(float(val_raw))))
                except:
                    valor_val = 0
                
                if valor_val == 0:
                    continue
                
                texto_pos = f"{fecha_doc} QR DE {pdv_val}"
                
                p = {c: None for c in columnas_multiusos}
                p.update({
                    'ID': idx, 'FECHA DOC': fecha_doc, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                    'FECHA CONT': fecha_doc, 'FECHA REG': fecha_doc, 'MONEDA TR': 'COP',
                    'REFERENCIA': comercio_val, 'TEXTO CABECERA': f"PAGO QR",
                    'IDENTIFICADOR PI': idx, 'POSICION': pos_efectiva, 'CLAVE CONTABILIZACION': cc_sap,
                    'CUENTA DE MAYOR': cuenta_sap, 'VALOR TR': valor_val, 'CEBE': cebe_val,
                    'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_pos
                })
                filas.append(p)
                pos_efectiva += 1
            
        return pd.DataFrame(filas)[columnas_multiusos]

    def generar_plano_multiusos_payments_way(df_filtrado, df_matriz_dtf, codigo_sociedad):
        columnas_multiusos = [
            'ID', 'USUARIO', 'LEDGER', 'FECHA DOC', 'CLASE DOCUMENTO', 'SOCIEDAD', 'FECHA CONT',
            'FECHA REG', 'MONEDA TR', 'TASA DE CAMBIO', 'REFERENCIA', 'TEXTO CABECERA',
            'IDENTIFICADOR PI', 'POSICION', 'CLAVE CONTABILIZACION', 'CUENTA DE MAYOR',
            'CLASE DE CUENTA', 'PROVEEDOR', 'CLIENTE', 'PAGADOR ALTERNATIVO', 'INDICADOR CME',
            'VALOR TR', 'IND IVA', 'CALCULAR IMP. AUTOMATICO', 'FECHA BASE', 'CONDICION PAGO',
            'FECHA VALOR', 'Orden de Compra', 'Posicion OC', 'ORDEN', 'CECO', 'CEBE', 'GRAFO',
            'OPERACION GRAFO', 'ELEMENTO PEP', 'ASIGNACION', 'CLAVE DE REF_1', 'CLAVE DE REF_2',
            'CLAVE DE REF_3', 'TEXTO POSICION', 'INDICADOR TP. RETENCIONES 1', 'INDICADOR RETENCION  1',
            'BASE RETENCION 1', 'BASE RETENCION DOC 1', 'INDICADOR TP. RETENCIONES 2', 'INDICADOR RETENCION  2',
            'BASE RETENCION 2', 'BASE RETENCION DOC 2', 'INDICADOR TP. RETENCIONES 3', 'INDICADOR RETENCION  3',
            'BASE RETENCION 3', 'BASE RETENCION DOC 3', 'INDICADOR TP. RETENCIONES 4', 'INDICADOR RETENCION  4',
            'BASE RETENCION 4', 'BASE RETENCION DOC4', 'INDICADOR TP. RETENCIONES 5', 'INDICADOR RETENCION  5',
            'BASE RETENCION 5', 'BASE RETENCION DOC 5', 'AÑO', 'MES', 'MONEDA', 'OBJETO COSTO',
            'CLASE DE ACTIVIDAD', 'POSICION DE LA ORDEN', 'HOJA DE RUTA', 'SEGMENTO', 'PRODUCTO',
            'OF VENTAS', 'CLIENTE CAR', 'CLASE MEDIO DE TRANSPORTE', 'ZONA', 'MEDIO DE TRANSPORTE',
            'GRUPO MATERIAL 1', 'GRUPO MATERIAL 2', 'GRUPO MATERIAL 3', 'GRUPO MATERIAL 4',
            'VALOR LC', 'FECHA RFERENCIA PAGO', 'DOCUMENTO REFERENCIA', 'FECHA REFERENCIA', 'BLOQUEO PAGO'
        ]
        
        filas = []
        fecha_hoy = datetime.now().strftime('%d.%m.%Y')
        nit_corporativo = "8600538311"
        
        mapa_columnas_vlr = {
            'Vlr Abono': 'VALOR TOTAL',
            'Vlr Comision': 'VALOR COMISION',
            'Vlr Total': 'VALOR TOTAL',
            'Vlr Rete Fuente': 'VALOR RETE FUENTE',
            'Vlr Rete Ica': 'VALOR RETE ICA',
            'Vlr Rete Iva': 'VALOR RETE IVA'
        }

        for idx, (_, row) in enumerate(df_filtrado.iterrows(), start=1):
            comercio_val = str(row.get('REFERENCIA', row.get('COMERCIO', ''))).strip()
            
            fecha_doc = fecha_hoy
            val_fec = row.get('FECHA', row.get('FECHA DE PAGO', None))
            if pd.notna(val_fec):
                try:
                    fec_str = str(val_fec).strip()
                    parsed = pd.to_datetime(fec_str, errors='coerce')
                    if pd.notna(parsed):
                        fecha_doc = parsed.strftime('%d.%m.%Y')
                except:
                    pass

            pdv_val = str(row.get('PDV_SAP', ''))
            cebe_val = str(row.get('CB', ''))
            
            filas_matriz = df_matriz_dtf[df_matriz_dtf['TRN'] == 6]
            if len(filas_matriz) == 0:
                filas_matriz = df_matriz_dtf
            
            pos_efectiva = 1
            for _, m_row in filas_matriz.iterrows():
                tipo_cta = str(m_row['TIPO CUENTA']).strip()
                cuenta_sap = int(m_row['CUENTA SAP'])
                cc_sap = int(m_row['CC SAP'])
                
                col_plano = None
                for k, v in mapa_columnas_vlr.items():
                    if k.lower() in tipo_cta.lower():
                        col_plano = v
                        break
                if not col_plano:
                    col_plano = 'VALOR TOTAL' if 'total' in tipo_cta.lower() else 'VALOR COMISION'
                
                val_raw = row.get(col_plano, 0) if col_plano in row else 0
                try:
                    valor_val = int(round(abs(float(val_raw))))
                except:
                    valor_val = 0
                
                if valor_val == 0:
                    continue
                
                texto_pos = f"{fecha_doc} PW {pdv_val}"
                
                p = {c: None for c in columnas_multiusos}
                p.update({
                    'ID': idx, 'FECHA DOC': fecha_doc, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                    'FECHA CONT': fecha_doc, 'FECHA REG': fecha_doc, 'MONEDA TR': 'COP',
                    'REFERENCIA': comercio_val, 'TEXTO CABECERA': f"PAYMENTS WAY",
                    'IDENTIFICADOR PI': idx, 'POSICION': pos_efectiva, 'CLAVE CONTABILIZACION': cc_sap,
                    'CUENTA DE MAYOR': cuenta_sap, 'VALOR TR': valor_val, 'CEBE': cebe_val,
                    'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_pos
                })
                filas.append(p)
                pos_efectiva += 1
            
        return pd.DataFrame(filas)[columnas_multiusos]

    # EXPORTADOR MULTI-PESTAÑA A EXCEL
    def generar_excel_multipestana(df_resumen_gen, df_cuentas, df_pi_edades, df_pi_full):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_cuentas.to_excel(writer, sheet_name='Recaudo x Cuenta', index=False)
            df_pi_edades.to_excel(writer, sheet_name='Edades Pendientes', index=False)
            df_pi_full.to_excel(writer, sheet_name='Partidas Por Identificar', index=False)
            df_resumen_gen.to_excel(writer, sheet_name='Extracto Base', index=False)
        return output.getvalue()

    # --- VERIFICACIÓN DE ARCHIVOS MAESTROS ---
    if codigo_sociedad is None:
        st.warning(f"🚧 La sociedad **{sociedad_seleccionada}** se encuentra en proceso de implementación.")
    elif not os.path.exists(nombre_archivo_base):
        st.error(f"⚠️ No se encontró el archivo maestro '{nombre_archivo_base}' en la raíz del repositorio.")
    elif not os.path.exists(nombre_archivo_matriz_dtf):
        st.error(f"⚠️ No se encontró el archivo '{nombre_archivo_matriz_dtf}' en la raíz del repositorio.")
    elif not os.path.exists(nombre_archivo_comercios):
        st.error(f"⚠️ No se encontró el archivo '{nombre_archivo_comercios}' en la raíz del repositorio.")
    else:
        df_base_tiendas = pd.read_excel(nombre_archivo_base, sheet_name='Hoja1')
        df_base_tiendas.columns = [str(c).strip().upper() for c in df_base_tiendas.columns]
        df_base_tiendas['TEXTO_CLEAN'] = df_base_tiendas['TEXTO MULTICAHS'].astype(str).str.strip().str.upper()
        
        mapa_multicash = {}
        for _, r in df_base_tiendas.iterrows():
            mapa_multicash[r['TEXTO_CLEAN']] = {
                'cb_sap': r.get('CB SAP', ''),
                'pdv_sap': r.get('PDV SAP', ''),
                'tipificacion': r.get('TIPIFICACION', '')
            }

        df_matriz_dtf = pd.read_excel(nombre_archivo_matriz_dtf)
        df_matriz_dtf.columns = [str(c).strip().upper() for c in df_matriz_dtf.columns]

        df_comercios_dtf = pd.read_excel(nombre_archivo_comercios)
        df_comercios_dtf.columns = [str(c).strip().upper() for c in df_comercios_dtf.columns]
        
        mapa_comercios = {}
        for _, r in df_comercios_dtf.iterrows():
            com_key = str(r.get('COMERCIO', '')).strip()
            term_key = str(r.get('TERMINAL', '')).strip()
            mapa_comercios[(com_key, term_key)] = {
                'pdv_sap': r.get('PDV SAP', ''),
                'cb': r.get('CB', '')
            }
            if com_key not in mapa_comercios:
                mapa_comercios[com_key] = {
                    'pdv_sap': r.get('PDV SAP', ''),
                    'cb': r.get('CB', '')
                }

        # ==========================================
        # 1. CARGA DEL EXTRACTO GENERAL Y RESUMEN
        # ==========================================
        st.markdown(f"### 📥 Carga de Multicash / Extracto Bancario General • {sociedad_seleccionada}")
        uploaded_multicash_gen = st.file_uploader("Sube el Extracto Multicash General para Diagnóstico y Resumen", type=["xlsx", "XLSX", "xls", "csv"], key="up_gen_global_v48")
        
        if uploaded_multicash_gen:
            try:
                if uploaded_multicash_gen.name.lower().endswith(('.xlsx', '.xls')):
                    df_ext_gen = pd.read_excel(uploaded_multicash_gen)
                else:
                    df_ext_gen = pd.read_csv(uploaded_multicash_gen, encoding='latin1')
                    
                df_ext_gen.columns = [str(c).strip().upper() for c in df_ext_gen.columns]
                cols_lower = [str(c).lower() for c in df_ext_gen.columns]
                col_val_gen = next((df_ext_gen.columns[i] for i, c in enumerate(cols_lower) if 'valor' in c or 'monto' in c or 'importe' in c or 'neto' in c), None)
                col_cta_gen = next((df_ext_gen.columns[i] for i, c in enumerate(cols_lower) if 'cuenta' in c or 'cta' in c or 'banco' in c), df_ext_gen.columns[1] if len(df_ext_gen.columns) > 1 else 'Cuenta')
                col_fec_gen = next((df_ext_gen.columns[i] for i, c in enumerate(cols_lower) if 'fecha' in c or 'date' in c), None)
                
                df_ext_gen['VALOR_LIMPIO'] = pd.to_numeric(df_ext_gen[col_val_gen], errors='coerce').fillna(0).abs() if col_val_gen else 0.0
                col_ref_gen = df_ext_gen.columns[min(9, len(df_ext_gen.columns) - 1)]
                
                def clasificar_gen(row):
                    ref_text = str(row.get(col_ref_gen, '')).strip().upper()
                    if ref_text in mapa_multicash:
                        info = mapa_multicash[ref_text]
                        return info['tipificacion'], info['pdv_sap'], info['cb_sap']
                    for k, info in mapa_multicash.items():
                        if k and k in ref_text:
                            return info['tipificacion'], info['pdv_sap'], info['cb_sap']
                    return 'POR IDENTIFICAR', '', ''

                res_gen = df_ext_gen.apply(clasificar_gen, axis=1)
                df_ext_gen['TIPO'] = [r[0] for r in res_gen]
                df_ext_gen['PDV_SAP'] = [r[1] for r in res_gen]
                df_ext_gen['CB_SAP'] = [r[2] for r in res_gen]
                
                tot_reg = len(df_ext_gen)
                tot_monto = df_ext_gen['VALOR_LIMPIO'].sum()
                
                df_c_gen = df_ext_gen[df_ext_gen['TIPO'] == 'Consignaciones']
                df_d_gen = df_ext_gen[df_ext_gen['TIPO'] == 'Datafonos']
                df_q_gen = df_ext_gen[df_ext_gen['TIPO'] == 'QR'] if maneja_qr else pd.DataFrame()
                df_p_gen = df_ext_gen[df_ext_gen['TIPO'] == 'POR IDENTIFICAR']

                tiendas_sin_cb = df_ext_gen[(df_ext_gen['TIPO'] != 'POR IDENTIFICAR') & (df_ext_gen['CB_SAP'] == '')]
                if len(tiendas_sin_cb) > 0:
                    st.warning(f"⚠️ **Alerta Interfaz SAP:** Se detectaron {len(tiendas_sin_cb)} registros tipificados sin Centro de Beneficio (CB). Revisa la parametrización para prevenir errores en SAP.")
                
                st.markdown("#### 📊 Diagnóstico General del Extracto")
                c1, c2, c3, c4, c5 = st.columns(5)
                
                with c1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">TOTAL EXTRACTO</div>
                            <div class="metric-val">{tot_reg} part.</div>
                            <div class="metric-sub">${tot_monto:,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">CONSIGNACIONES</div>
                            <div class="metric-val">{len(df_c_gen)} part.</div>
                            <div class="metric-sub">${df_c_gen['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">DATÁFONOS</div>
                            <div class="metric-val">{len(df_d_gen)} part.</div>
                            <div class="metric-sub">${df_d_gen['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c4:
                    if maneja_qr:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-title">QR</div>
                                <div class="metric-val">{len(df_q_gen)} part.</div>
                                <div class="metric-sub">${df_q_gen['VALOR_LIMPIO'].sum():,.2f}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="metric-card" style="opacity: 0.5;">
                                <div class="metric-title">QR</div>
                                <div class="metric-val">N/A</div>
                                <div class="metric-sub">No Aplica</div>
                            </div>
                        """, unsafe_allow_html=True)
                with c5:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">POR IDENTIFICAR</div>
                            <div class="metric-val">{len(df_p_gen)} part.</div>
                            <div class="metric-sub" style="color: #DC2626;">${df_p_gen['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col_chart1, col_chart2 = st.columns(2)

                with col_chart1:
                    st.markdown("#### 🏦 Recaudo por Cuenta Bancaria")
                    df_ext_gen['CUENTA_MOSTRAR'] = df_ext_gen[col_cta_gen].astype(str).str.strip()
                    df_cuentas = df_ext_gen.groupby('CUENTA_MOSTRAR').agg(
                        Partidas=('VALOR_LIMPIO', 'count'),
                        Monto_Total=('VALOR_LIMPIO', 'sum')
                    ).reset_index().sort_values(by='Monto_Total', ascending=False)

                    monto_global_cuentas = df_cuentas['Monto_Total'].sum()
                    if monto_global_cuentas > 0:
                        df_cuentas['% Participación'] = (df_cuentas['Monto_Total'] / monto_global_cuentas * 100).round(2).astype(str) + '%'
                    else:
                        df_cuentas['% Participación'] = '0%'

                    df_cuentas['Monto Recaudado'] = df_cuentas['Monto_Total'].apply(lambda x: f"${x:,.2f}")
                    df_cuentas_display = df_cuentas.rename(columns={'CUENTA_MOSTRAR': 'Cuenta Bancaria / ID'})

                    st.dataframe(
                        df_cuentas_display[['Cuenta Bancaria / ID', 'Partidas', 'Monto Recaudado', '% Participación']],
                        use_container_width=True,
                        height=280
                    )

                with col_chart2:
                    st.markdown("#### ⏳ Partidas Por Identificar por Edades (Semáforo)")
                    
                    if len(df_p_gen) > 0:
                        df_pi_edades = df_p_gen.copy()
                        
                        if col_fec_gen:
                            fec_series = pd.to_datetime(df_pi_edades[col_fec_gen], errors='coerce')
                            hoy_dt = pd.Timestamp(datetime.now())
                            df_pi_edades['DIAS_ANTIGUEDAD'] = (hoy_dt - fec_series).dt.days.fillna(0).astype(int)
                        else:
                            df_pi_edades['DIAS_ANTIGUEDAD'] = 15
                            
                        def categorizar_edad_semaforo(dias):
                            if dias <= 30:
                                return '🟢 01. 0 a 30 días (Al Día)'
                            elif dias <= 60:
                                return '🟡 02. 31 a 60 días (Seguimiento)'
                            elif dias <= 90:
                                return '🟠 03. 61 a 90 días (Crítico)'
                            else:
                                return '🔴 04. Más de 90 días (Alerta Roja)'
                                
                        df_pi_edades['RANGO_EDAD'] = df_pi_edades['DIAS_ANTIGUEDAD'].apply(categorizar_edad_semaforo)
                        
                        df_edades_resumen = df_pi_edades.groupby('RANGO_EDAD').agg(
                            Partidas=('VALOR_LIMPIO', 'count'),
                            Monto_Total=('VALOR_LIMPIO', 'sum')
                        ).reset_index().sort_values(by='RANGO_EDAD')
                        
                        bars_edades = alt.Chart(df_edades_resumen).mark_bar(
                            cornerRadiusTopRight=6, 
                            cornerRadiusBottomRight=6
                        ).encode(
                            x=alt.X('Monto_Total:Q', title=None, axis=alt.Axis(format="$,s", grid=False)),
                            y=alt.Y('RANGO_EDAD:N', title=None, sort=alt.EncodingSortField(field="RANGO_EDAD", order="ascending")),
                            color=alt.Color(
                                'RANGO_EDAD:N',
                                scale=alt.Scale(
                                    domain=['🟢 01. 0 a 30 días (Al Día)', '🟡 02. 31 a 60 días (Seguimiento)', '🟠 03. 61 a 90 días (Crítico)', '🔴 04. Más de 90 días (Alerta Roja)'],
                                    range=['#10B981', '#F59E0B', '#EF4444', '#991B1B']
                                ),
                                legend=None
                            ),
                            tooltip=[
                                alt.Tooltip('RANGO_EDAD', title="Rango Antigüedad"),
                                alt.Tooltip('Partidas', title="Cantidad Partidas"),
                                alt.Tooltip('Monto_Total', format="$,.2f", title="Monto Total")
                            ]
                        )
                        
                        text_edades = alt.Chart(df_edades_resumen).mark_text(
                            align='left',
                            baseline='middle',
                            dx=6,
                            fontSize=11,
                            fontWeight='bold',
                            color='#374151'
                        ).encode(
                            x=alt.X('Monto_Total:Q'),
                            y=alt.Y('RANGO_EDAD:N', sort=alt.EncodingSortField(field="RANGO_EDAD", order="ascending")),
                            text=alt.Text('Monto_Total:Q', format="$,.0f")
                        )
                        
                        chart_edades = (bars_edades + text_edades).properties(height=280).configure_view(strokeWidth=0)
                        st.altair_chart(chart_edades, use_container_width=True)
                    else:
                        st.success("🎉 ¡Excelente! No hay partidas pendientes por identificar en este extracto.")

                st.markdown("<br>", unsafe_allow_html=True)

                col_acc1, col_acc2, col_acc3 = st.columns(3)
                
                with col_acc1:
                    if st.button("💾 Guardar Cierre en Archivo Histórico", use_container_width=True):
                        registro_cierre = {
                            'Fecha Cierre': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'Sociedad': sociedad_seleccionada,
                            'Total Registros': tot_reg,
                            'Monto Total': tot_monto,
                            'Partidas Pendientes': len(df_p_gen),
                            'Monto Pendiente': df_p_gen['VALOR_LIMPIO'].sum() if len(df_p_gen) > 0 else 0
                        }
                        lista_hist = cargar_historico_excel()
                        lista_hist.append(registro_cierre)
                        pd.DataFrame(lista_hist).to_excel(ARCHIVO_HISTORICO, index=False)
                        st.success("✅ ¡Cierre guardado permanentemente en Excel!")
                        st.rerun()

                with col_acc2:
                    df_pi_export = df_p_gen.copy() if len(df_p_gen) > 0 else pd.DataFrame({'Estado': ['Sin Pendientes']})
                    excel_bytes = generar_excel_multipestana(df_ext_gen, df_cuentas, df_edades_resumen if len(df_p_gen) > 0 else pd.DataFrame(), df_pi_export)
                    
                    st.download_button(
                        label="📊 Descargar Informe Excel (.xlsx)",
                        data=excel_bytes,
                        file_name=f"Informe_Consolidado_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

                with col_acc3:
                    texto_reporte = f"""REPORTE EJECUTIVO DE CIERRE - CONTROL EFECTIVO POPSY
Sociedad: {sociedad_seleccionada}
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
--------------------------------------------------
Total Registros Extracto: {tot_reg}
Monto Total Recaudado: ${tot_monto:,.2f}
Consignaciones: {len(df_c_gen)} part. (${df_c_gen['VALOR_LIMPIO'].sum():,.2f})
Datáfonos: {len(df_d_gen)} part. (${df_d_gen['VALOR_LIMPIO'].sum():,.2f})
Partidas Por Identificar: {len(df_p_gen)} part. (${df_p_gen['VALOR_LIMPIO'].sum():,.2f})
--------------------------------------------------
Generado por Colaborador Popsy - Sistema Automático SAP
"""
                    st.download_button(
                        label="📄 Descargar Resumen (.txt)",
                        data=texto_reporte.encode('utf-8-sig'),
                        file_name=f"Reporte_Cierre_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                # GRÁFICA DE TENDENCIA LEYENDO DESDE EXCEL
                lista_hist_actual = cargar_historico_excel()
                if len(lista_hist_actual) > 0:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("📈 Ver Histórico y Gráfica de Tendencia Comparativa"):
                        df_hist = pd.DataFrame(lista_hist_actual)
                        
                        if len(df_hist) >= 2:
                            line_monto = alt.Chart(df_hist).mark_line(point=True, color='#C2185B').encode(
                                x=alt.X('Fecha Cierre:N', title='Fecha / Hora Cierre'),
                                y=alt.Y('Monto Total:Q', title='Monto Recaudado ($)'),
                                tooltip=['Fecha Cierre', 'Sociedad', 'Monto Total', 'Partidas Pendientes']
                            ).properties(height=240, title="Evolución del Recaudo Total")
                            
                            line_pi = alt.Chart(df_hist).mark_line(point=True, color='#DC2626').encode(
                                x=alt.X('Fecha Cierre:N', title='Fecha / Hora Cierre'),
                                y=alt.Y('Monto Pendiente:Q', title='Monto Pendiente ($)'),
                                tooltip=['Fecha Cierre', 'Monto Pendiente', 'Partidas Pendientes']
                            ).properties(height=240, title="Evolución de Partidas Por Identificar")
                            
                            c_h1, c_h2 = alt.hconcat() # o usar columnas de streamlit
                            c_h1, c_h2 = st.columns(2)
                            with c_h1:
                                st.altair_chart(line_monto, use_container_width=True)
                            with c_h2:
                                st.altair_chart(line_pi, use_container_width=True)
                        else:
                            st.info("ℹ️ Tienes 1 cierre guardado. Las gráficas de tendencia se activarán automáticamente cuando guardes un segundo cierre.")

                        st.markdown("#### 📋 Registro Detallado de Cierres Guardados")
                        st.dataframe(df_hist, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown("#### 📋 Detalle del Extracto General")
                st.dataframe(df_ext_gen, use_container_width=True)

                if len(df_p_gen) > 0:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### ⚠️ Partidas Por Identificar & Bitácora de Auditoría")
                    
                    filtro_texto_pi = st.text_input("🔍 Buscar en Partidas Por Identificar:", "", key="filtro_pi_texto")
                    
                    if filtro_texto_pi:
                        mask = df_p_gen.astype(str).apply(lambda col: col.str.contains(filtro_texto_pi, case=False)).any(axis=1)
                        df_p_view = df_p_gen[mask].copy()
                    else:
                        df_p_view = df_p_gen.copy()

                    df_p_view['Notas Auditoría'] = [st.session_state.notas_partidas.get(str(r), '') for r in df_p_view[col_ref_gen]]
                    st.dataframe(df_p_view, use_container_width=True)
                    
                    with st.expander("💬 Registrar / Actualizar Nota de Auditoría sobre Partida Pendiente"):
                        c_n1, c_n2 = st.columns([1, 2])
                        with c_n1:
                            ref_nota_select = st.selectbox("Selecciona la Referencia:", df_p_view[col_ref_gen].astype(str).unique())
                        with c_n2:
                            texto_nota_input = st.text_input("Ingresa el comentario de seguimiento:")
                            
                        if st.button("Guardar Nota de Auditoría"):
                            if ref_nota_select and texto_nota_input:
                                st.session_state.notas_partidas[str(ref_nota_select)] = texto_nota_input
                                st.success(f"✅ Nota registrada correctamente para la referencia {ref_nota_select}")
                                st.rerun()

                    csv_pi = df_p_view.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    st.download_button(
                        label="📥 Exportar Partidas Por Identificar con Notas (.csv)",
                        data=csv_pi,
                        file_name=f"Partidas_Por_Identificar_Notas_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        key="btn_dl_pi"
                    )
                    
            except Exception as e:
                st.error(f"Error procesando resumen general: {e}")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        # ==========================================
        # 2. PESTAÑAS INDEPENDIENTES Y PLANOS MULTIUSOS
        # ==========================================
        if maneja_qr:
            tab_cons, tab_dtf, tab_qr, tab_pw = st.tabs([
                "🏦 1. Consignaciones", 
                "💳 2. Datáfonos", 
                "📱 3. Códigos QR",
                "🚀 4. Payments Way"
            ])
        else:
            tab_cons, tab_dtf, tab_pw = st.tabs([
                "🏦 1. Consignaciones", 
                "💳 2. Datáfonos",
                "🚀 4. Payments Way"
            ])
            tab_qr = None

        # --- MÓDULO 1: CONSIGNACIONES ---
        with tab_cons:
            st.markdown(f"### 🏦 Módulo de Consignaciones • {sociedad_seleccionada}")
            st.markdown("Sube el **Extracto Bancario / Multicash** para procesar las consignaciones y descargar el Plano Multiusos SAP.")
            
            uploaded_cons = st.file_uploader("Sube el Extracto Bancario (Consignaciones)", type=["xlsx", "XLSX", "xls", "csv"], key="up_cons_final")
            
            if uploaded_cons:
                try:
                    if uploaded_cons.name.lower().endswith(('.xlsx', '.xls')):
                        df_c_raw = pd.read_excel(uploaded_cons)
                    else:
                        df_c_raw = pd.read_csv(uploaded_cons, encoding='latin1')
                        
                    df_c_raw.columns = [str(c).strip().upper() for c in df_c_raw.columns]
                    cols_lower = [str(c).lower() for c in df_c_raw.columns]
                    
                    col_val = next((df_c_raw.columns[i] for i, c in enumerate(cols_lower) if 'valor' in c or 'monto' in c or 'importe' in c or 'neto' in c), None)
                    col_ref = df_c_raw.columns[min(9, len(df_c_raw.columns) - 1)]
                    
                    df_c_raw['VALOR_LIMPIO'] = pd.to_numeric(df_c_raw[col_val], errors='coerce').fillna(0).abs() if col_val else 0.0
                    
                    def filtrar_c(row):
                        ref_text = str(row.get(col_ref, '')).strip().upper()
                        if ref_text in mapa_multicash and mapa_multicash[ref_text]['tipificacion'] == 'Consignaciones':
                            info = mapa_multicash[ref_text]
                            return 'SI', info['pdv_sap'], info['cb_sap']
                        return 'NO', '', ''

                    res = df_c_raw.apply(filtrar_c, axis=1)
                    df_c_raw['ES_C'] = [r[0] for r in res]
                    df_c_raw['PDV_SAP'] = [r[1] for r in res]
                    df_c_raw['CB_SAP'] = [r[2] for r in res]
                    
                    df_c_filtrado = df_c_raw[df_c_raw['ES_C'] == 'SI']
                    
                    st.metric("Total Consignaciones Detectadas", f"{len(df_c_filtrado)} registros", f"${df_c_filtrado['VALOR_LIMPIO'].sum():,.2f}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    filtro_pdv_c = st.text_input("🔍 Filtrar por Tienda / Referencia:", "", key="f_c")
                    if filtro_pdv_c:
                        df_c_view = df_c_filtrado[df_c_filtrado['PDV_SAP'].astype(str).str.contains(filtro_pdv_c, case=False) | df_c_filtrado[col_ref].astype(str).str.contains(filtro_pdv_c, case=False)]
                    else:
                        df_c_view = df_c_filtrado

                    plano_c = generar_plano_multiusos_consignaciones(df_c_view, codigo_sociedad)
                    
                    tot_deb = plano_c[plano_c['CLAVE CONTABILIZACION'] == 40]['VALOR TR'].sum()
                    tot_cred = plano_c[plano_c['CLAVE CONTABILIZACION'] == 50]['VALOR TR'].sum()
                    
                    st.markdown("#### ⚖️ Auditoría de Balance Contable SAP")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Débitos (Clave 40)", f"${tot_deb:,.2f}")
                    m2.metric("Total Créditos (Clave 50)", f"${tot_cred:,.2f}")
                    m3.metric("Diferencia / Cuadre", f"${abs(tot_deb - tot_cred):,.2f}", delta="OK Cuadrado" if tot_deb == tot_cred else "Descuadrado", delta_color="normal")

                    st.markdown("<br>", unsafe_allow_html=True)
                    col_d1, col_d2 = st.columns(2)
                    
                    csv_c = plano_c.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    txt_c = plano_c.to_csv(index=False, sep='|', encoding='utf-8-sig').encode('utf-8-sig')
                    
                    with col_d1:
                        st.download_button(
                            label="📥 Descargar Plano SAP (.csv)",
                            data=csv_c,
                            file_name=f"Multiusos_Consignaciones_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            key="btn_dl_cons_csv",
                            use_container_width=True
                        )
                    with col_d2:
                        st.download_button(
                            label="📄 Descargar Plano SAP Delimitado (.txt)",
                            data=txt_c,
                            file_name=f"Multiusos_Consignaciones_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="btn_dl_cons_txt",
                            use_container_width=True
                        )

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_c_view, use_container_width=True)
                except Exception as e:
                    st.error(f"Error procesando consignaciones: {e}")

        # --- MÓDULO 2: DATÁFONOS ---
        with tab_dtf:
            st.markdown(f"### 💳 Módulo de Datáfonos • {sociedad_seleccionada}")
            st.markdown(f"Sube el **Archivo Plano de Datáfonos** para procesarlo con la matriz específica de **{sociedad_seleccionada}**.")
            
            uploaded_dtf = st.file_uploader("Sube el Archivo Plano de Datáfonos", type=["xlsx", "XLSX", "xls", "csv"], key="up_dtf_final")
            
            if uploaded_dtf:
                try:
                    if uploaded_dtf.name.lower().endswith(('.xlsx', '.xls')):
                        df_d_raw = pd.read_excel(uploaded_dtf)
                    else:
                        df_d_raw = pd.read_csv(uploaded_dtf, encoding='latin1')
                        
                    df_d_raw.columns = [str(c).strip().upper() for c in df_d_raw.columns]
                    cols_lower = [str(c).lower() for c in df_d_raw.columns]
                    
                    col_val_tot = next((df_d_raw.columns[i] for i, c in enumerate(cols_lower) if 'vlr total' in c or 'valor total' in c or 'total' in c), None)
                    df_d_raw['VALOR_LIMPIO'] = pd.to_numeric(df_d_raw[col_val_tot], errors='coerce').fillna(0).abs() if col_val_tot else 0.0
                    
                    def mapear_comercio(row):
                        comercio = str(row.get('COMERCIO', '')).strip()
                        terminal = str(row.get('TERMINAL', '')).strip()
                        if (comercio, terminal) in mapa_comercios:
                            info = mapa_comercios[(comercio, terminal)]
                            return info['pdv_sap'], info['cb']
                        elif comercio in mapa_comercios:
                            info = mapa_comercios[comercio]
                            return info['pdv_sap'], info['cb']
                        return '', ''

                    res_d = df_d_raw.apply(mapear_comercio, axis=1)
                    df_d_raw['PDV_SAP'] = [r[0] for r in res_d]
                    df_d_raw['CB'] = [r[1] for r in res_d]
                    
                    st.metric("Total Transacciones Datáfonos", f"{len(df_d_raw)} registros", f"${df_d_raw['VALOR_LIMPIO'].sum():,.2f}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    filtro_pdv_d = st.text_input("🔍 Filtrar por PDV / Tienda o Comercio:", "", key="f_d")
                    if filtro_pdv_d:
                        df_d_view = df_d_raw[df_d_raw['PDV_SAP'].astype(str).str.contains(filtro_pdv_d, case=False) | df_d_raw['COMERCIO'].astype(str).str.contains(filtro_pdv_d, case=False)]
                    else:
                        df_d_view = df_d_raw

                    plano_d = generar_plano_multiusos_datafonos(df_d_view, df_matriz_dtf, codigo_sociedad)
                    
                    tot_deb = plano_d[plano_d['CLAVE CONTABILIZACION'] == 40]['VALOR TR'].sum()
                    tot_cred = plano_d[plano_d['CLAVE CONTABILIZACION'] == 50]['VALOR TR'].sum()
                    
                    st.markdown("#### ⚖️ Auditoría de Balance Contable SAP")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Débitos (Clave 40)", f"${tot_deb:,.2f}")
                    m2.metric("Total Créditos (Clave 50)", f"${tot_cred:,.2f}")
                    m3.metric("Diferencia / Cuadre", f"${abs(tot_deb - tot_cred):,.2f}", delta="OK Cuadrado" if tot_deb == tot_cred else "Descuadrado", delta_color="normal")

                    st.markdown("<br>", unsafe_allow_html=True)
                    col_d1, col_d2 = st.columns(2)
                    
                    csv_d = plano_d.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    txt_d = plano_d.to_csv(index=False, sep='|', encoding='utf-8-sig').encode('utf-8-sig')
                    
                    with col_d1:
                        st.download_button(
                            label="📥 Descargar Plano SAP (.csv)",
                            data=csv_d,
                            file_name=f"Multiusos_Datafonos_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            key="btn_dl_dtf_csv",
                            use_container_width=True
                        )
                    with col_d2:
                        st.download_button(
                            label="📄 Descargar Plano SAP Delimitado (.txt)",
                            data=txt_d,
                            file_name=f"Multiusos_Datafonos_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="btn_dl_dtf_txt",
                            use_container_width=True
                        )

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_d_view, use_container_width=True)
                except Exception as e:
                    st.error(f"Error procesando datáfonos: {e}")

        # --- MÓDULO 3: CÓDIGOS QR (SI APLICA) ---
        if maneja_qr and tab_qr is not None:
            with tab_qr:
                st.markdown(f"### 📱 Módulo de Códigos QR • {sociedad_seleccionada}")
                st.markdown("Sube el **Archivo Plano de Códigos QR (CSV con separador `|`)** para procesarlo con la matriz de cuentas y generar automáticamente el Plano Multiusos SAP.")
                
                uploaded_qr = st.file_uploader("Sube el Archivo Plano de Códigos QR", type=["csv", "txt"], key="up_qr_final")
                
                if uploaded_qr:
                    try:
                        df_q_raw = pd.read_csv(uploaded_qr, encoding='latin1', sep='|')
                            
                        df_q_raw.columns = [str(c).strip().upper() for c in df_q_raw.columns]
                        cols_lower = [str(c).lower() for c in df_q_raw.columns]
                        
                        col_val_qr = next((df_q_raw.columns[i] for i, c in enumerate(cols_lower) if 'valor total' in c or 'vlr total' in c or 'valor compra' in c or 'total' in c), None)
                        df_q_raw['VALOR_LIMPIO'] = pd.to_numeric(df_q_raw[col_val_qr], errors='coerce').fillna(0).abs() if col_val_qr else 0.0
                        
                        def mapear_comercio_qr(row):
                            comercio = str(row.get('CODIGO UNICO', '')).strip()
                            terminal = str(row.get('NUMERO DE TERMINAL', '')).strip()
                            if (comercio, terminal) in mapa_comercios:
                                info = mapa_comercios[(comercio, terminal)]
                                return info['pdv_sap'], info['cb']
                            elif comercio in mapa_comercios:
                                info = mapa_comercios[comercio]
                                return info['pdv_sap'], info['cb']
                            return '', ''

                        res_q = df_q_raw.apply(mapear_comercio_qr, axis=1)
                        df_q_raw['PDV_SAP'] = [r[0] for r in res_q]
                        df_q_raw['CB'] = [r[1] for r in res_q]

                        st.metric("Total Transacciones QR", f"{len(df_q_raw)} registros", f"${df_q_raw['VALOR_LIMPIO'].sum():,.2f}")
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        filtro_pdv_q = st.text_input("🔍 Filtrar por PDV / Tienda o Código Único:", "", key="f_q")
                        if filtro_pdv_q:
                            df_q_view = df_q_raw[df_q_raw['PDV_SAP'].astype(str).str.contains(filtro_pdv_q, case=False) | df_q_raw['CODIGO UNICO'].astype(str).str.contains(filtro_pdv_q, case=False)]
                        else:
                            df_q_view = df_q_raw

                        plano_q = generar_plano_multiusos_qr(df_q_view, df_matriz_dtf, codigo_sociedad)
                        
                        tot_deb = plano_q[plano_q['CLAVE CONTABILIZACION'] == 40]['VALOR TR'].sum()
                        tot_cred = plano_q[plano_q['CLAVE CONTABILIZACION'] == 50]['VALOR TR'].sum()
                        
                        st.markdown("#### ⚖️ Auditoría de Balance Contable SAP")
                        m1, m2, m3 = st.columns(3)
                        m1.metric("Total Débitos (Clave 40)", f"${tot_deb:,.2f}")
                        m2.metric("Total Créditos (Clave 50)", f"${tot_cred:,.2f}")
                        m3.metric("Diferencia / Cuadre", f"${abs(tot_deb - tot_cred):,.2f}", delta="OK Cuadrado" if tot_deb == tot_cred else "Descuadrado", delta_color="normal")

                        st.markdown("<br>", unsafe_allow_html=True)
                        col_q1, col_q2 = st.columns(2)
                        
                        csv_q = plano_q.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                        txt_q = plano_q.to_csv(index=False, sep='|', encoding='utf-8-sig').encode('utf-8-sig')
                        
                        with col_q1:
                            st.download_button(
                                label="📥 Descargar Plano SAP (.csv)",
                                data=csv_q,
                                file_name=f"Multiusos_QR_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                key="btn_dl_qr_csv",
                                use_container_width=True
                            )
                        with col_q2:
                            st.download_button(
                                label="📄 Descargar Plano SAP Delimitado (.txt)",
                                data=txt_q,
                                file_name=f"Multiusos_QR_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                key="btn_dl_qr_txt",
                                use_container_width=True
                            )

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.dataframe(df_q_view, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error procesando códigos QR: {e}")

        # --- MÓDULO 4: PAYMENTS WAY ---
        with tab_pw:
            st.markdown(f"### 🚀 Módulo Payments Way • {sociedad_seleccionada}")
            st.markdown("Sube el **Archivo Plano de Payments Way** para procesarlo con la matriz contable y generar automáticamente el Plano Multiusos SAP.")
            
            uploaded_pw = st.file_uploader("Sube el Archivo de Payments Way", type=["xlsx", "XLSX", "xls", "csv"], key="up_pw_final")
            
            if uploaded_pw:
                try:
                    if uploaded_pw.name.lower().endswith(('.xlsx', '.xls')):
                        df_pw_raw = pd.read_excel(uploaded_pw)
                    else:
                        df_pw_raw = pd.read_csv(uploaded_pw, encoding='latin1')
                        
                    df_pw_raw.columns = [str(c).strip().upper() for c in df_pw_raw.columns]
                    cols_lower = [str(c).lower() for c in df_pw_raw.columns]
                    
                    col_val_pw = next((df_pw_raw.columns[i] for i, c in enumerate(cols_lower) if 'total' in c or 'valor' in c or 'monto' in c), None)
                    df_pw_raw['VALOR_LIMPIO'] = pd.to_numeric(df_pw_raw[col_val_pw], errors='coerce').fillna(0).abs() if col_val_pw else 0.0
                    
                    def mapear_comercio_pw(row):
                        comercio = str(row.get('COMERCIO', row.get('REFERENCIA', ''))).strip()
                        if comercio in mapa_comercios:
                            info = mapa_comercios[comercio]
                            return info['pdv_sap'], info['cb']
                        return '', ''

                    res_pw = df_pw_raw.apply(mapear_comercio_pw, axis=1)
                    df_pw_raw['PDV_SAP'] = [r[0] for r in res_pw]
                    df_pw_raw['CB'] = [r[1] for r in res_pw]

                    st.metric("Total Transacciones Payments Way", f"{len(df_pw_raw)} registros", f"${df_pw_raw['VALOR_LIMPIO'].sum():,.2f}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    filtro_pdv_pw = st.text_input("🔍 Filtrar por PDV / Tienda o Comercio:", "", key="f_pw")
                    if filtro_pdv_pw:
                        df_pw_view = df_pw_raw[df_pw_raw['PDV_SAP'].astype(str).str.contains(filtro_pdv_pw, case=False)]
                    else:
                        df_pw_view = df_pw_raw

                    plano_pw = generar_plano_multiusos_payments_way(df_pw_view, df_matriz_dtf, codigo_sociedad)
                    
                    tot_deb = plano_pw[plano_pw['CLAVE CONTABILIZACION'] == 40]['VALOR TR'].sum()
                    tot_cred = plano_pw[plano_pw['CLAVE CONTABILIZACION'] == 50]['VALOR TR'].sum()
                    
                    st.markdown("#### ⚖️ Auditoría de Balance Contable SAP")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Débitos (Clave 40)", f"${tot_deb:,.2f}")
                    m2.metric("Total Créditos (Clave 50)", f"${tot_cred:,.2f}")
                    m3.metric("Diferencia / Cuadre", f"${abs(tot_deb - tot_cred):,.2f}", delta="OK Cuadrado" if tot_deb == tot_cred else "Descuadrado", delta_color="normal")

                    st.markdown("<br>", unsafe_allow_html=True)
                    col_p1, col_p2 = st.columns(2)
                    
                    csv_pw = plano_pw.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    txt_pw = plano_pw.to_csv(index=False, sep='|', encoding='utf-8-sig').encode('utf-8-sig')
                    
                    with col_p1:
                        st.download_button(
                            label="📥 Descargar Plano SAP (.csv)",
                            data=csv_pw,
                            file_name=f"Multiusos_PaymentsWay_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            key="btn_dl_pw_csv",
                            use_container_width=True
                        )
                    with col_p2:
                        st.download_button(
                            label="📄 Descargar Plano SAP Delimitado (.txt)",
                            data=txt_pw,
                            file_name=f"Multiusos_PaymentsWay_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="btn_dl_pw_txt",
                            use_container_width=True
                        )

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_pw_view, use_container_width=True)
                except Exception as e:
                    st.error(f"Error procesando Payments Way: {e}")
