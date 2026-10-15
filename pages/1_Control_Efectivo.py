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

    def aplicar_estilos_excel_bytes(wb):
        NAVY_HEADER = "003366"
        WHITE_TEXT = "FFFFFF"
        ZEBRA_FILL = "F2F5F9"
        BORDER_COLOR = "D9D9D9"
        
        thin_border = Border(
            left=Side(style='thin', color=BORDER_COLOR), right=Side(style='thin', color=BORDER_COLOR),
            top=Side(style='thin', color=BORDER_COLOR), bottom=Side(style='thin', color=BORDER_COLOR)
        )
        
        for sheetname in wb.sheetnames:
            ws = wb[sheetname]
            ws.views.sheetView[0].showGridLines = True
            
            if ws.max_row > 0:
                ws.row_dimensions[1].height = 26
                for col in range(1, ws.max_column + 1):
                    cell = ws.cell(row=1, column=col)
                    cell.font = Font(name='Segoe UI', size=10, bold=True, color=WHITE_TEXT)
                    cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    cell.border = thin_border
                    
                for row in range(2, ws.max_row + 1):
                    ws.row_dimensions[row].height = 20
                    for col in range(1, ws.max_column + 1):
                        cell = ws.cell(row=row, column=col)
                        cell.font = Font(name='Segoe UI', size=10)
                        cell.border = thin_border
                        if row % 2 == 0:
                            cell.fill = PatternFill(start_color=ZEBRA_FILL, end_color=ZEBRA_FILL, fill_type="solid")
                            
                for col in ws.columns:
                    max_len = max(len(str(cell.value or '')) for cell in col)
                    col_letter = get_column_letter(col[0].column)
                    ws.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 40)
        return wb

    def generar_plano_multiusos(df_filtrado, tipo_prefijo, codigo_sociedad):
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
        cuenta_banco_default = '11100511'
        cuenta_ingreso_default = '11050502'
        nit_corporativo = "8600538311"
        
        for idx, (_, row) in enumerate(df_filtrado.iterrows(), start=1):
            ref_val = str(row.get('TEXTO MULTICAHS', row.get('REFERENCIA', row.iloc[0]))).strip()
            cebe_val = str(row.get('CB_SAP', ''))
            pdv_val = str(row.get('PDV_SAP', ''))
            
            val_raw = row.get('VALOR_LIMPIO', row.get('VALOR', row.get('VALOR TR', 0)))
            try:
                valor_val = abs(float(val_raw))
            except:
                valor_val = 0.0
                
            texto_pos = f"{fecha_hoy} {tipo_prefijo} {pdv_val}"
            
            p1 = {c: None for c in columnas_multiusos}
            p1.update({
                'ID': idx, 'FECHA DOC': fecha_hoy, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                'FECHA CONT': fecha_hoy, 'FECHA REG': fecha_hoy, 'MONEDA TR': 'COP',
                'REFERENCIA': ref_val, 'TEXTO CABECERA': f"{tipo_prefijo} {ref_val}",
                'IDENTIFICADOR PI': idx, 'POSICION': 1, 'CLAVE CONTABILIZACION': 50,
                'CUENTA DE MAYOR': int(cuenta_banco_default), 'VALOR TR': valor_val, 'CEBE': cebe_val,
                'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_pos
            })
            
            p2 = {c: None for c in columnas_multiusos}
            p2.update({
                'ID': idx, 'FECHA DOC': fecha_hoy, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                'FECHA CONT': fecha_hoy, 'FECHA REG': fecha_hoy, 'MONEDA TR': 'COP',
                'REFERENCIA': ref_val, 'TEXTO CABECERA': f"{tipo_prefijo} {ref_val}",
                'IDENTIFICADOR PI': idx, 'POSICION': 2, 'CLAVE CONTABILIZACION': 40,
                'CUENTA DE MAYOR': int(cuenta_ingreso_default), 'VALOR TR': valor_val, 'CEBE': cebe_val,
                'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_pos
            })
            
            filas.append(p1)
            filas.append(p2)
            
        return pd.DataFrame(filas)[columnas_multiusos]

    if codigo_sociedad is None:
        st.warning(f"🚧 La sociedad **{sociedad_seleccionada}** se encuentra en proceso de implementación.")
    elif not os.path.exists(nombre_archivo_base):
        st.error(f"⚠️ No se encontró el archivo maestro '{nombre_archivo_base}' en la raíz del repositorio.")
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

        # ==========================================
        # 1. CARGA DEL EXTRACTO GENERAL Y RESUMEN
        # ==========================================
        st.markdown(f"### 📥 Carga de Multicash / Extracto Bancario General • {sociedad_seleccionada}")
        uploaded_multicash_gen = st.file_uploader("Sube el Extracto Multicash General para Diagnóstico y Resumen", type=["xlsx", "XLSX", "xls", "csv"], key="up_gen_global")
        
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

        # MÓDULO 1: CONSIGNACIONES
        with tab_cons:
            st.markdown(f"### 🏦 Módulo de Consignaciones • {sociedad_seleccionada}")
            st.markdown("Sube el **Extracto Bancario / Multicash** para procesar las consignaciones y descargar el Plano Multiusos SAP.")
            
            uploaded_cons = st.file_uploader("Sube el Extracto Bancario (Consignaciones)", type=["xlsx", "XLSX", "xls", "csv"], key="up_cons_tab")
            
            if uploaded_cons:
                try:
                    if uploaded_cons.name.lower().endswith(('.xlsx', '.xls')):
                        df_c_raw = pd.read_excel(uploaded_cons)
                    else:
                        df_c_raw = pd.read_csv(uploaded_cons, encoding='latin1')
                        
                    df_c_raw.columns = [str(c).strip().upper() for c in df_c_raw.columns]
                    cols_lower = [str(c).lower() for c in df_c_raw.columns]
                    col_val = next((df_c_raw.columns[i] for i, c in enumerate(cols_lower) if 'valor' in c or 'monto' in c or 'importe' in c or 'neto' in c), None)
                    
                    df_c_raw['VALOR_LIMPIO'] = pd.to_numeric(df_c_raw[col_val], errors='coerce').fillna(0) if col_val else 0.0
                    col_ref = df_c_raw.columns[min(9, len(df_c_raw.columns) - 1)]
                    
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
                    
                    plano_c = generar_plano_multiusos(df_c_filtrado, "CG", codigo_sociedad)
                    out_c = io.BytesIO()
                    with pd.ExcelWriter(out_c, engine='openpyxl') as w:
                        plano_c.to_excel(w, sheet_name='Multiusos_Consignaciones', index=False)
                    out_c.seek(0)
                    wb_c = openpyxl.load_workbook(out_c)
                    wb_c_est = aplicar_estilos_excel_bytes(wb_c)
                    final_c = io.BytesIO()
                    wb_c_est.save(final_c)
                    final_c.seek(0)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 Descargar Plano Multiusos SAP - Consignaciones (.xlsx)",
                        data=final_c,
                        file_name=f"Multiusos_Consignaciones_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="btn_dl_cons_final",
                        use_container_width=True
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_c_filtrado, use_container_width=True)
                except Exception as e:
                    st.error(f"Error procesando consignaciones: {e}")

        # MÓDULO 2: DATÁFONOS
        with tab_dtf:
            st.markdown(f"### 💳 Módulo de Datáfonos • {sociedad_seleccionada}")
            st.markdown("Sube el **Archivo de Datáfonos / Pasarelas** independiente para procesarlo y descargar su Plano Multiusos SAP.")
            
            uploaded_dtf = st.file_uploader("Sube el Archivo de Datáfonos", type=["xlsx", "XLSX", "xls", "csv"], key="up_dtf_tab")
            
            if uploaded_dtf:
                try:
                    if uploaded_dtf.name.lower().endswith(('.xlsx', '.xls')):
                        df_d_raw = pd.read_excel(uploaded_dtf)
                    else:
                        df_d_raw = pd.read_csv(uploaded_dtf, encoding='latin1')
                        
                    df_d_raw.columns = [str(c).strip().upper() for c in df_d_raw.columns]
                    cols_lower = [str(c).lower() for c in df_d_raw.columns]
                    col_val = next((df_d_raw.columns[i] for i, c in enumerate(cols_lower) if 'valor' in c or 'monto' in c or 'importe' in c or 'neto' in c), None)
                    
                    df_d_raw['VALOR_LIMPIO'] = pd.to_numeric(df_d_raw[col_val], errors='coerce').fillna(0) if col_val else 0.0
                    col_ref = df_d_raw.columns[min(9, len(df_d_raw.columns) - 1)]
                    
                    def filtrar_d(row):
                        ref_text = str(row.get(col_ref, '')).strip().upper()
                        if ref_text in mapa_multicash and mapa_multicash[ref_text]['tipificacion'] == 'Datafonos':
                            return 'SI', mapa_multicash[ref_text]['pdv_sap'], mapa_multicash[ref_text]['cb_sap']
                        return 'NO', '', ''

                    res = df_d_raw.apply(filtrar_d, axis=1)
                    df_d_raw['ES_D'] = [r[0] for r in res]
                    df_d_raw['PDV_SAP'] = [r[1] for r in res]
                    df_d_raw['CB_SAP'] = [r[2] for r in res]
                    
                    df_d_filtrado = df_d_raw[df_d_raw['ES_D'] == 'SI']
                    
                    st.metric("Total Datáfonos Detectados", f"{len(df_d_filtrado)} registros", f"${df_d_filtrado['VALOR_LIMPIO'].sum():,.2f}")
                    
                    plano_d = generar_plano_multiusos(df_d_filtrado, "DTF", codigo_sociedad)
                    out_d = io.BytesIO()
                    with pd.ExcelWriter(out_d, engine='openpyxl') as w:
                        plano_d.to_excel(w, sheet_name='Multiusos_Datafonos', index=False)
                    out_d.seek(0)
                    wb_d = openpyxl.load_workbook(out_d)
                    wb_d_est = aplicar_estilos_excel_bytes(wb_d)
                    final_d = io.BytesIO()
                    wb_d_est.save(final_d)
                    final_d.seek(0)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 Descargar Plano Multiusos SAP - Datáfonos (.xlsx)",
                        data=final_d,
                        file_name=f"Multiusos_Datafonos_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="btn_dl_dtf_final",
                        use_container_width=True
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_d_filtrado, use_container_width=True)
                except Exception as e:
                    st.error(f"Error procesando datáfonos: {e}")

        # MÓDULO 3: CÓDIGOS QR
        with tab_qr:
            st.markdown(f"### 📱 Módulo de Códigos QR • {sociedad_seleccionada}")
            st.markdown("Sube el **Archivo de Códigos QR** independiente para procesarlo y descargar su Plano Multiusos SAP.")
            
            uploaded_qr = st.file_uploader("Sube el Archivo de Códigos QR", type=["xlsx", "XLSX", "xls", "csv"], key="up_qr_tab")
            
            if uploaded_qr:
                try:
                    if uploaded_qr.name.lower().endswith(('.xlsx', '.xls')):
                        df_q_raw = pd.read_excel(uploaded_qr)
                    else:
                        df_q_raw = pd.read_csv(uploaded_qr, encoding='latin1')
                        
                    df_q_raw.columns = [str(c).strip().upper() for c in df_q_raw.columns]
                    cols_lower = [str(c).lower() for c in df_q_raw.columns]
                    col_val = next((df_q_raw.columns[i] for i, c in enumerate(cols_lower) if 'valor' in c or 'monto' in c or 'importe' in c or 'neto' in c), None)
                    
                    df_q_raw['VALOR_LIMPIO'] = pd.to_numeric(df_q_raw[col_val], errors='coerce').fillna(0) if col_val else 0.0
                    col_ref = df_q_raw.columns[min(9, len(df_q_raw.columns) - 1)]
                    
                    def filtrar_q(row):
                        ref_text = str(row.get(col_ref, '')).strip().upper()
                        if ref_text in mapa_multicash and mapa_multicash[ref_text]['tipificacion'] == 'QR':
                            return 'SI', mapa_multicash[ref_text]['pdv_sap'], mapa_multicash[ref_text]['cb_sap']
                        return 'NO', '', ''

                    res = df_q_raw.apply(filtrar_q, axis=1)
                    df_q_raw['ES_Q'] = [r[0] for r in res]
                    df_q_raw['PDV_SAP'] = [r[1] for r in res]
                    df_q_raw['CB_SAP'] = [r[2] for r in res]
                    
                    df_q_filtrado = df_q_raw[df_q_raw['ES_Q'] == 'SI']
                    
                    st.metric("Total QR Detectados", f"{len(df_q_filtrado)} registros", f"${df_q_filtrado['VALOR_LIMPIO'].sum():,.2f}")
                    
                    plano_q = generar_plano_multiusos(df_q_filtrado, "QR", codigo_sociedad)
                    out_q = io.BytesIO()
                    with pd.ExcelWriter(out_q, engine='openpyxl') as w:
                        plano_q.to_excel(w, sheet_name='Multiusos_QR', index=False)
                    out_q.seek(0)
                    wb_q = openpyxl.load_workbook(out_q)
                    wb_q_est = aplicar_estilos_excel_bytes(wb_q)
                    final_q = io.BytesIO()
                    wb_q_est.save(final_q)
                    final_q.seek(0)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 Descargar Plano Multiusos SAP - Códigos QR (.xlsx)",
                        data=final_q,
                        file_name=f"Multiusos_QR_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="btn_dl_qr_final",
                        use_container_width=True
                    )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_q_filtrado, use_container_width=True)
                except Exception as e:
                    st.error(f"Error procesando códigos QR: {e}")
