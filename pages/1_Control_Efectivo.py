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
                valor_val = float(val_raw)
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
        # CARGA ÚNICA DEL EXTRACTO MULTICASH
        # ==========================================
        st.markdown(f"### 📥 Carga de Multicash / Extracto Bancario • {sociedad_seleccionada}")
        uploaded_multicash = st.file_uploader("Sube el Extracto Multicash General", type=["xlsx", "XLSX", "xls", "csv"], key="up_multicash_unico")
        
        if uploaded_multicash:
            try:
                if uploaded_multicash.name.lower().endswith(('.xlsx', '.xls')):
                    df_ext = pd.read_excel(uploaded_multicash)
                else:
                    df_ext = pd.read_csv(uploaded_multicash, encoding='latin1')
                    
                df_ext.columns = [str(c).strip().upper() for c in df_ext.columns]
                cols_lower = [str(c).lower() for c in df_ext.columns]
                col_val = next((df_ext.columns[i] for i, c in enumerate(cols_lower) if 'valor' in c or 'monto' in c or 'importe' in c or 'neto' in c), None)
                
                df_ext['VALOR_LIMPIO'] = pd.to_numeric(df_ext[col_val], errors='coerce').fillna(0) if col_val else 0.0
                col_ref = df_ext.columns[min(9, len(df_ext.columns) - 1)]
                
                def clasificar(row):
                    ref_text = str(row.get(col_ref, '')).strip().upper()
                    if ref_text in mapa_multicash:
                        info = mapa_multicash[ref_text]
                        return info['tipificacion'], info['pdv_sap'], info['cb_sap']
                    for k, info in mapa_multicash.items():
                        if k and k in ref_text:
                            return info['tipificacion'], info['pdv_sap'], info['cb_sap']
                    return 'POR IDENTIFICAR', '', ''

                res = df_ext.apply(clasificar, axis=1)
                df_ext['TIPO'] = [r[0] for r in res]
                df_ext['PDV_SAP'] = [r[1] for r in res]
                df_ext['CB_SAP'] = [r[2] for r in res]
                
                tot_reg = len(df_ext)
                tot_monto = df_ext['VALOR_LIMPIO'].sum()
                
                df_c = df_ext[df_ext['TIPO'] == 'Consignaciones']
                df_d = df_ext[df_ext['TIPO'] == 'Datafonos']
                df_q = df_ext[df_ext['TIPO'] == 'QR']
                df_p = df_ext[df_ext['TIPO'] == 'POR IDENTIFICAR']
                
                # --- RESUMEN EJECUTIVO ---
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
                            <div class="metric-val">{len(df_c)} part.</div>
                            <div class="metric-sub">${df_c['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">Datáfonos</div>
                            <div class="metric-val">{len(df_d)} part.</div>
                            <div class="metric-sub">${df_d['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">QR</div>
                            <div class="metric-val">{len(df_q)} part.</div>
                            <div class="metric-sub">${df_q['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with c5:
                    st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-title">Por Identificar</div>
                            <div class="metric-val">{len(df_p)} part.</div>
                            <div class="metric-sub" style="color: #DC2626;">${df_p['VALOR_LIMPIO'].sum():,.2f}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown("<br><hr><br>", unsafe_allow_html=True)

                # --- PESTAÑAS DE DETALLE Y DESCARGA MULTIUSOS ---
                tab_cons, tab_dtf, tab_qr, tab_pend = st.tabs([
                    f"🏦 Consignaciones ({len(df_c)})", 
                    f"💳 Datáfonos ({len(df_d)})", 
                    f"📱 Códigos QR ({len(df_q)})", 
                    f"❓ Por Identificar ({len(df_p)})"
                ])

                # PESTAÑA 1: CONSIGNACIONES
                with tab_cons:
                    st.markdown(f"### 🏦 Plano Multiusos • Consignaciones")
                    st.metric("Total Consignaciones Detectadas", f"{len(df_c)} registros", f"${df_c['VALOR_LIMPIO'].sum():,.2f}")
                    
                    if len(df_c) > 0:
                        plano_c = generar_plano_multiusos(df_c, "CG", codigo_sociedad)
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
                            key="dl_c_btn_new",
                            use_container_width=True
                        )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_c, use_container_width=True)

                # PESTAÑA 2: DATÁFONOS
                with tab_dtf:
                    st.markdown(f"### 💳 Plano Multiusos • Datáfonos")
                    st.metric("Total Datáfonos Detectados", f"{len(df_d)} registros", f"${df_d['VALOR_LIMPIO'].sum():,.2f}")
                    
                    if len(df_d) > 0:
                        plano_d = generar_plano_multiusos(df_d, "DTF", codigo_sociedad)
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
                            key="dl_d_btn_new",
                            use_container_width=True
                        )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_d, use_container_width=True)

                # PESTAÑA 3: CÓDIGOS QR
                with tab_qr:
                    st.markdown(f"### 📱 Plano Multiusos • Códigos QR")
                    st.metric("Total Códigos QR Detectados", f"{len(df_q)} registros", f"${df_q['VALOR_LIMPIO'].sum():,.2f}")
                    
                    if len(df_q) > 0:
                        plano_q = generar_plano_multiusos(df_q, "QR", codigo_sociedad)
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
                            key="dl_q_btn_new",
                            use_container_width=True
                        )
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.dataframe(df_q, use_container_width=True)

                # PESTAÑA 4: POR IDENTIFICAR
                with tab_pend:
                    st.markdown(f"### ❓ Partidas Por Identificar ({len(df_p)})")
                    st.dataframe(df_p, use_container_width=True)

            except Exception as e:
                st.error(f"Error procesando el archivo Multicash: {e}")
