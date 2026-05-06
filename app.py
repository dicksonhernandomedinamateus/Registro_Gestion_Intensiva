import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Gestión Fiscalización Intensiva", layout="wide", page_icon="📊")

# --- LISTAS DE DATOS ---
SISTEMAS = ["Gestor", "Integra", "Otro"]

TIPOS_ACTOS = [
    "Declaración de Renta",
    "Declaración de IVA",
    "Declaración de Retención en la Fuente",
    "Formulario de Pago (490)",
    "Requerimiento Especial",
    "Liquidación Oficial",
    "Otro"
]

CONCEPTOS_PAGO = [
    "71 - Impuesto", "72 - Sanción", "73 - Intereses de Mora", "74 - Anticipo", "Otro"
]

CONCEPTOS_SANCION = [
    "N/A (No aplica)", "Extemporaneidad", "Inexactitud", "Corrección", "No declarar",
    "No enviar información / Medios Magnéticos", "Facturación",
    "Omisión de activos / Pasivos inexistentes", "Otro"
]

CONCEPTOS_GESTION = [
    "Correcciones- contingencias Gestor", "Declaraciones presentadas-contingencias Gestor",
    "Correcciones- contingencias Integra", "Declaraciones presentadas-contingencias Integra",
    "Correcciones- Gestor", "Correcciones- Integra", "Declaraciones presentadas- Gestor",
    "Declaraciones presentadas- Integra", "Derivada de otras investigaciones Gestor",
    "Derivada de otras investigaciones Integra", "Fiscalizacion", "Fiscalizacion Persuasiva",
    "Gestion Obtenidad por la SGFT", "Liquidaciones Oficiales Ejecutoriadas",
    "Liquidaciones Provisionales Ejecutoriadas", "Gestion por Impacto Fiscalizador",
    "Resolucion Sancion por Contingencias", "Resolucion Sancion Aceptada", "Resolucion Sancion Plena",
    "RS Cambio de cierre a Pecuniaria", "Intereses de Mora pagados Integra",
    "Intereses de Mora pagados Gestor", "Normalización", "Incremento en la tributación por control INC",
    "Incremento en la tributación por control VENTAS", "Incremento en la tributación por control RENTA",
    "Terminación por Mutuo Acuerdo", "Reclasificacion de nuevos responsables"
]

ORIGENES_INVESTIGACION = [
    "Programas nivel central", "Acciones de Control Nivel central", "Acciones de Control Nivel local",
    "Denuncias y Derivados", "Devoluciones", "sin expediente", "Manual"
]

IMPUESTOS = [
    "Renta", "Ventas", "Retención", "Renta CREE", "Retención CREE", "Consumo", "Patrimonio", "GMF",
    "Facturación", "Riqueza", "Liquidacion Provisional ejecutoriada", "Normalización", 
    "Diferencial de Participación", "Contribución Artes Escenicas", "Obligaciones Formales", "Otro"
]

ARCHIVO_SALIDA = 'SOPORTE_GESTION_INTENSIVA.csv'

# --- MANEJO DE ESTADO ---
if 'mensaje_exito' not in st.session_state:
    st.session_state['mensaje_exito'] = ""

# --- CABECERA PRINCIPAL ---
st.title("⚖️ Sistema de Gestión - Fiscalización Intensiva")
st.markdown("Herramienta oficial para la consolidación de gestión de la **División 262**.")
st.divider()

if st.session_state['mensaje_exito']:
    st.success(st.session_state['mensaje_exito'], icon="✅")
    st.session_state['mensaje_exito'] = ""

# --- NAVEGACIÓN POR PESTAÑAS (ESTILO CLAUDE) ---
tab1, tab2 = st.tabs(["📝 Ingresar Nueva Gestión", "📊 Panel de Datos y Reportes"])

# ==========================================
# PESTAÑA 1: FORMULARIO DE REGISTRO
# ==========================================
with tab1:
    with st.form("registro_form", clear_on_submit=False):
        
        # Bloque 1: Funcionario
        with st.container(border=True):
            st.subheader("👤 1. Información del Funcionario")
            col1, col2, col3 = st.columns(3)
            with col1:
                cc_funcionario = st.text_input("C.C. Auditor")
            with col2:
                nombre_funcionario = st.text_input("Nombre del Auditor")
            with col3:
                concepto_sistema = st.selectbox("Sistema de Origen", options=SISTEMAS)
            st.text_input("Dependencia", value="262 - División Fiscalización y Liquidación Tributaria Intensiva", disabled=True)
        
        # Bloque 2: Acto y Contribuyente
        with st.container(border=True):
            st.subheader("📄 2. Datos del Acto y Contribuyente")
            col4, col5 = st.columns(2)
            with col4:
                nit = st.text_input("NIT")
                razon_social = st.text_input("Razón Social")
            with col5:
                tipo_acto = st.selectbox("Tipo de Acto", options=TIPOS_ACTOS)
                col_f, col_n = st.columns(2)
                with col_f:
                    fecha_acto = st.date_input("Fecha")
                with col_n:
                    no_acto = st.text_input("No. de Acto")
            
        # Bloque 3: Parámetros Técnicos
        with st.container(border=True):
            st.subheader("⚙️ 3. Clasificación Tributaria")
            col6, col7, col8, col9, col10 = st.columns(5)
            with col6: cp = st.selectbox("CP", options=CONCEPTOS_PAGO)
            with col7: ag = st.text_input("AG")
            with col8: ac = st.text_input("AC")
            with col9: cs = st.selectbox("CS", options=CONCEPTOS_SANCION)
            with col10: periodo = st.text_input("Periodo")
            
            c_imp, c_ori, c_ges = st.columns(3)
            with c_imp: impuesto = st.selectbox("Impuesto", options=IMPUESTOS)
            with c_ori: origen = st.selectbox("Origen de Investigación", options=ORIGENES_INVESTIGACION)
            with c_ges: concepto_gestion = st.selectbox("Concepto Gestión", options=CONCEPTOS_GESTION)

        # Bloque 4: Cifras
        with st.container(border=True):
            st.subheader("💰 4. Valores Recuperados / Auditados")
            col11, col12 = st.columns(2)
            with col11:
                v1 = st.number_input("1. Mayor valor a pagar", min_value=0.0, format="%.2f", step=1000.0)
                v2 = st.number_input("2. Menor saldo a favor", min_value=0.0, format="%.2f", step=1000.0)
                v3 = st.number_input("3. Sanciones Aceptadas", min_value=0.0, format="%.2f", step=1000.0)
            with col12:
                v4 = st.number_input("4. Intereses pagados", min_value=0.0, format="%.2f", step=1000.0)
                v5 = st.number_input("5. Res. sanción ejecutoriadas", min_value=0.0, format="%.2f", step=1000.0)
                v6 = st.number_input("6. Liq. oficiales ejecutoriadas", min_value=0.0, format="%.2f", step=1000.0)
            
            observaciones = st.text_area("Observaciones (Opcional)")

        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.form_submit_button(label="💾 GUARDAR REGISTRO OFICIAL", use_container_width=True, type="primary")

    # LÓGICA DE GUARDADO
    if submit_button:
        if not cc_funcionario.strip() or not nit.strip():
            st.error("⚠️ Faltan datos clave: C.C. del Funcionario y NIT son obligatorios.")
        else:
            total_gestion = v1 + v2 + v3 + v4 + v5 + v6
            
            nuevo_registro = {
                "Fecha del Reporte": datetime.now().strftime("%Y-%m-%d"),
                "Concepto y/o Sistema": concepto_sistema,
                " Cod. Dependencia": "262",
                "NIT": nit,
                "Nombre o Razón Social": razon_social,
                "Tipo de Acto": tipo_acto,
                "Fecha del Acto ": fecha_acto.strftime("%Y-%m-%d"),
                "No. del Acto": no_acto,
                "CP": cp,
                "AG": ag,
                "AC": ac,
                "CS": cs,
                "Periodo": periodo,
                "Impuesto": impuesto,
                "Origen de la Investigación": origen,
                "Conceptos de Gestión": concepto_gestion,
                "Valor Gestión por mayor valor a pagar": v1,
                "Valor Gestión por menor saldo a favor ": v2,
                "Valor gestión por sanciones Aceptadas": v3,
                "Valor intereses pagados": v4,
                "Valor de Gestión por resoluciones sanción plenas ejecutoriadas": v5,
                "Valor de Gestión por Liquidaciones oficiales ejecutoriadas": v6,
                "Total Gestión Aceptada": total_gestion,
                "C.C. Funcionario ": cc_funcionario,
                "Nombre Funcionario ": nombre_funcionario,
                "Observaciones": observaciones
            }

            try:
                archivo_existe = os.path.exists(ARCHIVO_SALIDA) and os.path.getsize(ARCHIVO_SALIDA) > 0
                df_nuevo = pd.DataFrame([nuevo_registro])
                
                if archivo_existe:
                    df_existente = pd.read_csv(ARCHIVO_SALIDA)
                    df_nuevo["No."] = len(df_existente) + 1
                    cols = ["No."] + [col for col in df_nuevo.columns if col != "No."]
                    df_nuevo = df_nuevo[cols]
                    df_nuevo.to_csv(ARCHIVO_SALIDA, mode='a', header=False, index=False, encoding='utf-8-sig')
                else:
                    df_nuevo["No."] = 1
                    cols = ["No."] + [col for col in df_nuevo.columns if col != "No."]
                    df_nuevo = df_nuevo[cols]
                    df_nuevo.to_csv(ARCHIVO_SALIDA, index=False, encoding='utf-8-sig')

                st.session_state['mensaje_exito'] = f"Gestión registrada correctamente con un total de: ${total_gestion:,.0f}"
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error al guardar: {str(e)}")

# ==========================================
# PESTAÑA 2: DASHBOARD Y BASE DE DATOS
# ==========================================
with tab2:
    if os.path.exists(ARCHIVO_SALIDA) and os.path.getsize(ARCHIVO_SALIDA) > 0:
        try:
            df_descarga = pd.read_csv(ARCHIVO_SALIDA)
            
            # --- DASHBOARD MÉTRICAS ---
            st.subheader("📈 Resumen de Gestión")
            total_registros = len(df_descarga)
            total_dinero = df_descarga['Total Gestión Aceptada'].sum()
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Total Registros Realizados", f"{total_registros}")
            col_m2.metric("Total Gestión Recuperada", f"${total_dinero:,.0f} COP")
            st.divider()

            # --- PREVISUALIZACIÓN ---
            st.subheader("📋 Previsualización de Datos")
            st.dataframe(df_descarga, use_container_width=True, height=300)
            
            # --- DESCARGA EXCEL ---
            st.markdown("### 📥 Exportar")
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_descarga.to_excel(writer, index=False, sheet_name='Gestión Intensiva')
            
            st.download_button(
                label="📁 Descargar Base de Datos Completa (.xlsx)",
                data=buffer.getvalue(),
                file_name=f"Base_Gestion_262_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )
        except Exception as e:
            st.error("Error cargando la base de datos para visualización.")
    else:
        st.info("📭 La base de datos está vacía. Registre la primera gestión para habilitar el panel.")
