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
    page_title="Control Efectivo POPSY",
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
    .stButton>button {
        background-color: #C2185B !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
    }
    .stButton>button:hover {
        background-color: #8E0038 !important;
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
            <div class="badge-tag">🍦 CONTROL EFECTIVO POPSY • {fecha_actual}</div>
            <h1 class="hero-title">¡Hola, {nombre_corto.split()[0]}! Bienvenido al Portal de Control Efectivo</h1>
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

    # --- SELECCIÓN DE MÓDULO ---
    st.markdown("### 📂 Módulos del Sistema")
    modulo_seleccionado = st.radio(
        "Selecciona el tipo de informe a procesar:",
        ["🏦 1. Consignaciones Bancarias", "💳 2. Datáfonos & Pasarelas", "📱 3. Pagos Código QR"],
        horizontal=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    def aplicar_estilos_excel_bytes(wb):
        NAVY_HEADER = "003366"
        WHITE_TEXT = "FFFFFF"
        ZEBRA_FILL = "F2F5F9"
        BORDER_COLOR = "D9D9D9"
        ACCENT_BLUE = "D9E1F2"
        
        thin_border = Border(
            left=Side(style='thin', color=BORDER_COLOR), right=Side(style='thin', color=BORDER_COLOR),
            top=Side(style='thin', color=BORDER_COLOR), bottom=Side(style='thin', color=BORDER_COLOR)
        )
        
        for sheetname in wb.sheetnames:
            ws = wb[sheetname]
            ws.views.sheetView[0].showGridLines = True
            
            if sheetname == 'Resumen_Diario':
                ws.column_dimensions['A'].width = 32
                ws.column_dimensions['B'].width = 25
                ws.merge_cells('A1:B1')
                title_cell = ws['A1']
                title_cell.value = "INFORME EJECUTIVO DE CONTROL EFECTIVO DIARIO"
                title_cell.font = Font(name='Segoe UI', size=13, bold=True, color=WHITE_TEXT)
                title_cell.fill = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
                title_cell.alignment = Alignment(horizontal='center', vertical='center')
                ws.row_dimensions[1].height = 35
                
                for row in range(3, ws.max_row + 1):
                    cell_a, cell_b = ws[f'A{row}'], ws[f'B{row}']
                    cell_a.font = Font(name='Segoe UI', size=11, bold=(row == ws.max_row))
                    cell_b.font = Font(name='Segoe UI', size=11, bold=(row == ws.max_row))
                    cell_a.border, cell_b.border = thin_border, thin_border
                    cell_b.alignment = Alignment(horizontal='right')
                    if row % 2 == 0:
                        cell_a.fill = cell_b.fill = PatternFill(start_color=ZEBRA_FILL, end_color=ZEBRA_FILL, fill_type="solid")
                    if row == ws.max_row:
                        cell_a.fill = cell_b.fill = PatternFill(start_color=ACCENT_BLUE, end_color=ACCENT_BLUE, fill_type="solid")
            else:
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

    def registrar_historial(usuario, sociedad, total_extracto, total_consolidados, total_pendientes):
        archivo_historial = "historial_depuracion.xlsx"
        nuevo_registro = {
            "Fecha y Hora": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Usuario": usuario,
            "Sociedad": sociedad,
            "Partidas Extracto": total_extracto,
            "Consolidadas": total_consolidados,
            "Pendientes Banco": total_pendientes
        }
        
        if os.path.exists(archivo_historial):
            try:
                df_hist = pd.read_excel(archivo_historial)
                df_hist = pd.concat([df_hist, pd.DataFrame([nuevo_registro])], ignore_index=True)
            except:
                df_hist = pd.DataFrame([nuevo_registro])
        else:
            df_hist = pd.DataFrame([nuevo_registro])
            
        df_hist.to_excel(archivo_historial, index=False)

    def generar_multiusos(df_conciliados, columna_clave_extracto, df_base, columna_clave_base, df_cuentas, codigo_sociedad):
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
        
        df_base.columns = [str(c).strip().upper() for c in df_base.columns]
        col_cb_sap = next((c for c in df_base.columns if 'CB SAP' in c), None)
        col_pdv_sap = next((c for c in df_base.columns if 'PDV SAP' in c), None)
        
        mapa_maestro = {}
        for _, r in df_base.iterrows():
            k = str(r.get(columna_clave_base, '')).strip().upper().lstrip('0')
            if k:
                mapa_maestro[k] = {
                    'cb_sap': str(r.get(col_cb_sap, '')) if col_cb_sap else '',
                    'pdv_sap': str(r.get(col_pdv_sap, '')) if col_pdv_sap else ''
                }

        df_cuentas.columns = [str(c).strip().upper() for c in df_cuentas.columns]
        col_sap = next((c for c in df_cuentas.columns if 'SAP' in c), df_cuentas.columns[min(3, len(df_cuentas.columns)-1)])
        col_cta_maestro = next((c for c in df_cuentas.columns if 'CUENTA' in c), df_cuentas.columns[0])
        col_empresa = next((c for c in df_cuentas.columns if 'EMPRESA' in c), codigo_sociedad)
        
        mapa_cuentas = {}
        for _, r in df_cuentas.iterrows():
            key = str(r.get(col_cta_maestro)).strip().upper()
            mapa_cuentas[key] = {
                'cuenta_sap': str(r.get(col_sap)),
                'empresa': str(r.get(col_empresa, codigo_sociedad))
            }

        filas = []
        fecha_hoy = datetime.now().strftime('%d.%m.%Y')
        
        cols_lower = [str(c).lower() for c in df_conciliados.columns]
        col_valor_name = next((df_conciliados.columns[i] for i, c in enumerate(cols_lower) if 'valor' in c or 'monto' in c or 'importe' in c), df_conciliados.columns[min(5, len(df_conciliados.columns)-1)])
        col_cuenta_ext = next((df_conciliados.columns[i] for i, c in enumerate(cols_lower) if 'cuenta' in c or 'banco' in c), None)
        col_fecha_ext = next((df_conciliados.columns[i] for i, c in enumerate(cols_lower) if 'fecha' in c), None)

        cuenta_caja_default = '11050502'
        nit_corporativo = "8600538311"

        for idx, (_, row) in enumerate(df_conciliados.iterrows(), start=1):
            ref_raw = str(row.get(columna_clave_extracto, '')).strip()
            ref_clean = ref_raw.upper().lstrip('0')
            
            valor_raw = row.get(col_valor_name, 0)
            try:
                valor_val = abs(float(valor_raw))
            except:
                valor_val = 0
            
            fecha_doc_val = fecha_hoy
            if col_fecha_ext:
                f_val = row.get(col_fecha_ext)
                if pd.notnull(f_val):
                    if isinstance(f_val, datetime):
                        fecha_doc_val = f_val.strftime('%d.%m.%Y')
                    else:
                        f_str = str(f_val).strip()
                        if len(f_str) >= 10:
                            try:
                                fecha_doc_val = pd.to_datetime(f_str).strftime('%d.%m.%Y')
                            except:
                                pass
                                
            cebe_val = ""
            pdv_val = f"REF {ref_raw}"
            if ref_clean in mapa_maestro:
                cebe_val = mapa_maestro[ref_clean]['cb_sap']
                pdv_val = mapa_maestro[ref_clean]['pdv_sap'] or f"REF {ref_raw}"
                
            texto_posicion = f"{fecha_doc_val} CG {pdv_val}"
            cuenta_sap_asignada = "11100511"
            
            if col_cuenta_ext:
                val_cta_ext = str(row.get(col_cuenta_ext)).strip().upper()
                if val_cta_ext in mapa_cuentas:
                    cuenta_sap_asignada = mapa_cuentas[val_cta_ext]['cuenta_sap']

            p1 = {c: None for c in columnas_multiusos}
            p1.update({
                'ID': idx, 'FECHA DOC': fecha_doc_val, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                'FECHA CONT': fecha_doc_val, 'FECHA REG': fecha_doc_val, 'MONEDA TR': 'COP',
                'REFERENCIA': ref_raw, 'TEXTO CABECERA': f"CG REF {ref_raw}",
                'IDENTIFICADOR PI': idx, 'POSICION': 1, 'CLAVE CONTABILIZACION': 50,
                'CUENTA DE MAYOR': int(cuenta_caja_default), 'VALOR TR': valor_val, 'CEBE': cebe_val,
                'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_posicion
            })
            
            p2 = {c: None for c in columnas_multiusos}
            p2.update({
                'ID': idx, 'FECHA DOC': fecha_doc_val, 'CLASE DOCUMENTO': 'SB', 'SOCIEDAD': codigo_sociedad,
                'FECHA CONT': fecha_doc_val, 'FECHA REG': fecha_doc_val, 'MONEDA TR': 'COP',
                'REFERENCIA': ref_raw, 'TEXTO CABECERA': f"CG REF {ref_raw}",
                'IDENTIFICADOR PI': idx, 'POSICION': 2, 'CLAVE CONTABILIZACION': 40,
                'CUENTA DE MAYOR': int(cuenta_sap_asignada), 'VALOR TR': valor_val, 'CEBE': cebe_val,
                'ASIGNACION': nit_corporativo, 'TEXTO POSICION': texto_posicion
            })
            
            filas.append(p1)
            filas.append(p2)
            
        return pd.DataFrame(filas)[columnas_multiusos]

    # --- MÓDULO 1: CONSIGNACIONES BANCARIAS ---
    if "Consignaciones" in modulo_seleccionado:
        st.markdown(f"#### 🏦 Módulo de Consignaciones Bancarias • {sociedad_seleccionada}")
        
        if codigo_sociedad is None:
            st.warning(f"🚧 La sociedad **{sociedad_seleccionada}** se encuentra en proceso de implementación.")
        else:
            if not os.path.exists(nombre_archivo_base):
                st.error(f"⚠️ No se encontró el archivo maestro '{nombre_archivo_base}' en la raíz del repositorio.")
            else:
                st.success(f"📁 Archivo maestro cargado automáticamente: **{nombre_archivo_base}** (Sociedad: {codigo_sociedad})")
                
                uploaded_extracto = st.file_uploader(f"Sube el Extracto Bancario para {sociedad_seleccionada}", type=["xlsx"], key=f"m1_ext_{codigo_sociedad}")

                if uploaded_extracto:
                    try:
                        df_base = pd.read_excel(nombre_archivo_base, sheet_name=0)
                        df_cuentas = pd.read_excel(nombre_archivo_base, sheet_name='Cuentas_Bancos')
                        df_extracto = pd.read_excel(uploaded_extracto)
                        
                        total_partidas_extracto = len(df_extracto)
                        
                        # Columna A de la base (índice 0) y Columna J del extracto (índice 9)
                        columna_clave_base = df_base.columns[0]
                        columna_clave_extracto = df_extracto.columns[min(9, len(df_extracto.columns) - 1)]
                        
                        df_base['ref_clean'] = df_base[columna_clave_base].astype(str).str.strip().str.upper().str.lstrip('0')
                        df_extracto['ref_clean'] = df_extracto[columna_clave_extracto].astype(str).str.strip().str.upper().str.lstrip('0')
                        
                        df_cruce = pd.merge(
                            df_base, df_extracto,
                            on='ref_clean',
                            how='outer', indicator=True, suffixes=('_base', '_extracto')
                        )
                        
                        pendientes_banco = df_cruce[df_cruce['_merge'] == 'right_only'].copy()
                        por_contabilizar = df_cruce[df_cruce['_merge'] == 'left_only'].copy()
                        conciliados = df_cruce[df_cruce['_merge'] == 'both'].copy()
                        
                        for df in [pendientes_banco, por_contabilizar, conciliados]:
                            if '_merge' in df.columns:
                                df.drop(columns=['_merge'], inplace=True)
                            if 'ref_clean' in df.columns:
                                df.drop(columns=['ref_clean'], inplace=True)
                        
                        registrar_historial(
                            usuario=st.session_state.get('usuario_nombre', st.session_state.correo_usuario),
                            sociedad=codigo_sociedad,
                            total_extracto=total_partidas_extracto,
                            total_consolidados=len(conciliados),
                            total_pendientes=len(pendientes_banco)
                        )
                        
                        plano_multiusos = generar_multiusos(conciliados, columna_clave_extracto, df_base, columna_clave_base, df_cuentas, codigo_sociedad)
                        total_abiertas = len(pendientes_banco) + len(por_contabilizar)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # --- MÉTRICAS VISUALES ---
                        c1, c2, c3, c4, c5 = st.columns(5)
                        c1.metric("📄 Partidas Extracto", total_partidas_extracto)
                        c2.metric("✅ Consolidadas", len(conciliados))
                        c3.metric("⏳ Pendientes Banco", len(pendientes_banco))
                        c4.metric("📥 Por Contabilizar", len(por_contabilizar))
                        c5.metric("📊 Total Abiertas", total_abiertas)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # --- TABLAS EN PESTAÑAS ---
                        t1, t2, t3, t4 = st.tabs(["✅ Consolidados", "⏳ Pendientes Banco", "📥 Por Contabilizar", "📋 Plano Multiusos SAP"])
                        
                        with t1:
                            st.dataframe(conciliados, use_container_width=True)
                        with t2:
                            st.markdown(f"##### Registros en el Extracto sin cruce en la Base ({len(pendientes_banco)} registros)")
                            st.dataframe(pendientes_banco, use_container_width=True)
                        with t3:
                            st.markdown(f"##### Registros en la Base sin cruce en el Extracto ({len(por_contabilizar)} registros)")
                            st.dataframe(por_contabilizar, use_container_width=True)
                        with t4:
                            st.markdown(f"##### Plano Multiusos SAP generado para la sociedad {codigo_sociedad}")
                            st.dataframe(plano_multiusos, use_container_width=True)
                            
                        # --- EXPORTAR EXCEL ---
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            pd.DataFrame({
                                "Métrica Contable": ["Sociedad", "Fecha y Hora Proceso", "Total Partidas Extracto", "Transacciones Consolidadas", "Pendientes en Banco", "Por Contabilizar", "Total Partidas Abiertas"],
                                "Cantidad / Valor": [codigo_sociedad, datetime.now().strftime('%Y-%m-%d %H:%M'), total_partidas_extracto, len(conciliados), len(pendientes_banco), len(por_contabilizar), total_abiertas]
                            }).to_excel(writer, sheet_name='Resumen_Diario', index=False, startrow=1)
                            
                            conciliados.to_excel(writer, sheet_name='Consolidados', index=False)
                            pendientes_banco.to_excel(writer, sheet_name='Pendientes_Banco', index=False)
                            por_contabilizar.to_excel(writer, sheet_name='Por_Contabilizar', index=False)
                            plano_multiusos.to_excel(writer, sheet_name='Plano_Multiusos', index=False)
                            
                        output.seek(0)
                        wb = openpyxl.load_workbook(output)
                        wb_estilizado = aplicar_estilos_excel_bytes(wb)
                        
                        final_output = io.BytesIO()
                        wb_estilizado.save(final_output)
                        final_output.seek(0)
                        
                        st.markdown("---")
                        st.download_button(
                            label=f"📥 Descargar Informe {codigo_sociedad} y Plano SAP Estilizado (.xlsx)",
                            data=final_output,
                            file_name=f"Informe_Consignaciones_{codigo_sociedad}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                        
                    except Exception as e:
                        st.error(f"Error procesando archivos para {codigo_sociedad}: {e}")
                else:
                    st.info(f"💡 Sube tu extracto bancario diario para **{sociedad_seleccionada}** para procesar el control efectivo y generar el plano SAP.")

    # --- MÓDULO 2: DATÁFONOS Y PASARELAS ---
    elif "Datáfonos" in modulo_seleccionado:
        st.markdown("#### 💳 Módulo de Datáfonos & Pasarelas de Pago")
        st.info("🚧 Módulo preparado para cargar reportes de Redeban, Credibancolombia, Bold o TuCompra.")

    # --- MÓDULO 3: CÓDIGO QR ---
    else:
        st.markdown("#### 📱 Módulo de Pagos Código QR")
        st.info("🚧 Módulo preparado para procesar transferencias QR de Bancolombia, Daviplata y Nequi.")
