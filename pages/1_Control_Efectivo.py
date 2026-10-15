import streamlit as st
import pandas as pd
from datetime import datetime
import os

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
            <div class="badge-tag">🍦 CONTROL EFECTIVO & PLANOS MULTIUSOS • {fecha_actual}</div>
            <h1 class="hero-title">¡Hola, {nombre_corto.split()[0]}! Diagnóstico y Planos Multiusos SAP</h1>
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
            ref_val = str(row.get('AUTORIZACION', row.get('COMPROBANTE', idx))).strip()
            
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
            
            for pos_i, (_, m_row) in enumerate(filas_matriz.iterrows(), start=1):
                tipo_cta = str(m_row['TIPO CUENTA']).strip()
                cuenta_sap = int(m_row['CUENTA SAP'])
                cc_sap = int(m_row['CC SAP'])
                
                col_plano = mapa_columnas_vlr.get(tipo_cta, None)
                val_raw = row.get(col_plano, 0) if col_plano else 0
                try:
                    valor_val = int(round(abs(float(val_raw))))
                except:
                    valor_val = 0
                
                texto_pos = f"{fecha_doc} DTF {pdv_val}"
                
                p = {c: None for c in columnas_multiusos}
                p.update({
                    'ID': idx, 'FECHA DOC': fecha_doc, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                    'FECHA CONT': fecha_doc, 'FECHA REG': fecha_doc, 'MONEDA TR': 'COP',
                    'REFERENCIA': ref_val, 'TEXTO CABECERA': f"DTF {ref_val}",
                    'IDENTIFICADOR PI': idx, 'POSICION': pos_i, 'CLAVE CONTABILIZACION': cc_sap,
                    'CUENTA DE MAYOR': cuenta_sap, 'VALOR TR': valor_val, 'CEBE': cebe_val,
                    'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_pos
                })
                filas.append(p)
            
        return pd.DataFrame(filas)[columnas_multiusos]

    # --- VERIFICACIÓN DE ARCHIVOS MAESTROS ---
    if codigo_sociedad is None:
        st.warning(f"🚧 La sociedad **{sociedad_seleccionada}** se encuentra en proceso de implementación.")
    elif not os.path.exists(nombre_archivo_base):
        st.error(f"⚠️ No se encontró el archivo maestro '{nombre_archivo_base}' en la raíz del repositorio.")
    elif not os.path.exists("base_datafonos.xlsx"):
        st.error(f"⚠️ No se encontró el archivo 'base_datafonos.xlsx' en la raíz del repositorio.")
    elif not os.path.exists("Comercio Datafonos.xlsx"):
        st.error(f"⚠️ No se encontró el archivo 'Comercio Datafonos.xlsx' en la raíz del repositorio.")
    else:
        # Cargar bases de referencia
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

        # Cargar matriz de datáfonos
        df_matriz_dtf = pd.read_excel('base_datafonos.xlsx')
        df_matriz_dtf.columns = [str(c).strip().upper() for c in df_matriz_dtf.columns]

        # Cargar maestro de comercios de datáfonos
        df_comercios_dtf = pd.read_excel('Comercio Datafonos.xlsx')
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
        uploaded_multicash_gen = st.file_uploader("Sube el Extracto Multicash General para Diagnóstico y Resumen", type=["xlsx", "XLSX", "xls", "csv"], key="up_gen_global_v10")
        
        if uploaded_multicash_gen:
            try:
                if uploaded_multicash_gen.name.lower().endswith(('.xlsx', '.xls')):
                    df_ext_gen = pd.read_excel(uploaded_multicash_gen)
                else:
                    df_ext_gen = pd.read_csv(uploaded_multicash_gen, encoding='latin1')
                    
                df_ext_gen.columns = [str(c).strip().upper() for c in df_ext_gen.columns]
                cols_lower = [str(c).lower() for c in df_ext_gen.columns]
                col_val_gen = next((df_ext_gen.columns[i] for i, c in enumerate(cols_lower) if 'valor' in c or 'monto' in c or 'importe' in c or 'neto' in c), None)
                
                df_ext_gen['VALOR_LIMPIO'] = pd.to_numeric(df_ext_gen[col_val_gen], errors='coerce').fillna(0) if col_val_gen else 0.0
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
                df_q_gen = df_ext_gen[df_ext_gen['TIPO'] == 'QR']
                df_p_gen = df_ext_gen[df_ext_gen['TIPO'] == 'POR IDENTIFICAR']
                
                st.markdown("#### 📊 Diagnóstico General del Extracto")
                c1, c2, c3, c4, c5 = st.columns(5)
                
                with c1:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">Total Extracto</div>
                            <div class="metric-val">{tot_reg} part.</div>
                            <div class="metric-sub">${tot_monto:,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">Consignaciones</div>
                            <div class="metric-val">{len(df_c_gen)} part.</div>
                            <div class="metric-sub">${df_c_gen['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">Datáfonos</div>
                            <div class="metric-val">{len(df_d_gen)} part.</div>
                            <div class="metric-sub">${df_d_gen['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">QR</div>
                            <div class="metric-val">{len(df_q_gen)} part.</div>
                            <div class="metric-sub">${df_q_gen['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c5:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">Por Identificar</div>
                            <div class="metric-val">{len(df_p_gen)} part.</div>
                            <div class="metric-sub" style="color: #DC2626;">${df_p_gen['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error procesando resumen general: {e}")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        # ==========================================
        # 2. PESTAÑAS INDEPENDIENTES Y PLANOS MULTIUSOS
        # ==========================================
        tab_cons, tab_dtf, tab_qr = st.tabs([
            "🏦 1. Consignaciones", 
            "💳 2. Datáfonos", 
            "📱 3. Códigos QR"
        ])

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
                    
                    df_c_raw['VALOR_LIMPIO'] = pd.to_numeric(df_c_raw[col_val], errors='coerce').fillna(0) if col_val else 0.0
                    
                    def filtrar_c(row):
                        ref_text = str(row.get(col_ref, '')).strip().upper()
                        if ref_text in mapa_multicash and mapa_multicash[ref_text]['tipificacion'] == 'Consignaciones':
                            return 'SI', mapa_multicash[ref_text]['pdv_sap'], mapa_multicash[ref_text]['cb_sap']
                        return 'NO', '', ''

                    res = df_c_raw.apply(filtrar_c, axis=1)
                    df_c_raw['ES_C'] = [r[0] for r in res]
                    df_c_raw['PDV_SAP'] = [r[1] for r in res]
                    df_c_raw['CB_SAP'] = [r[2] for r in res]
                    
                    df_c_filtrado = df_c_raw[df_c_raw['ES_C'] == 'SI']
                    
                    st.metric("Total Consignaciones Detectadas", f"{len(df_c_filtrado)} registros", f"${df_c_filtrado['VALOR_LIMPIO'].sum():,.2f}")
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    plano_c = generar_plano_multiusos_consignaciones(df_c_filtrado, codigo_sociedad)
                    csv_c = plano_c.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    
                    st.download_button(
                        label="📥 Descargar Plano Multiusos SAP - Consignaciones (.csv)",
                        data=csv_c,
                        file_name=f"Multiusos_Consignaciones_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="btn_dl_cons_final_csv",
                        use_container_width=True
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_c_filtrado, use_container_width=True)
                except Exception as e:
                    st.error(f"Error procesando consignaciones: {e}")

        # --- MÓDULO 2: DATÁFONOS ---
        with tab_dtf:
            st.markdown(f"### 💳 Módulo de Datáfonos • {sociedad_seleccionada}")
            st.markdown("Sube el **Archivo Plano de Datáfonos** para procesarlo y generar automáticamente el Plano Multiusos SAP con sus múltiples líneas.")
            
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
                    df_d_raw['VALOR_LIMPIO'] = pd.to_numeric(df_d_raw[col_val_tot], errors='coerce').fillna(0) if col_val_tot else 0.0
                    
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
                    
                    with st.spinner("Generando el Plano Multiusos SAP de Datáfonos... Por favor espera un momento ⏳"):
                        plano_d = generar_plano_multiusos_datafonos(df_d_raw, df_matriz_dtf, codigo_sociedad)
                        csv_d = plano_d.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                    
                    st.success(f"¡Plano generado con éxito! Total de posiciones contables creadas: {len(plano_d):,}")
                    
                    st.download_button(
                        label="📥 Descargar Plano Multiusos SAP - Datáfonos (.csv)",
                        data=csv_d,
                        file_name=f"Multiusos_Datafonos_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        key="btn_dl_dtf_final_csv",
                        use_container_width=True
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_d_raw, use_container_width=True)
                except Exception as e:
                    st.error(f"Error procesando datáfonos: {e}")

        # --- MÓDULO 3: CÓDIGOS QR ---
        with tab_qr:
            st.markdown(f"### 📱 Módulo de Códigos QR • {sociedad_seleccionada}")
            st.markdown("Próximamente disponible con la misma estructura multi-línea automatizada.")
