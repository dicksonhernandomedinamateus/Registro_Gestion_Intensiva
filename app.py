import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Gestión Fiscalización Intensiva", layout="wide")

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
    "71 - Impuesto",
    "72 - Sanción",
    "73 - Intereses de Mora",
    "74 - Anticipo",
    "Otro"
]

# NUEVA LISTA: Conceptos de Sanción (CS)
CONCEPTOS_SANCION = [
    "N/A (No aplica)",
    "Extemporaneidad",
    "Inexactitud",
    "Corrección",
    "No declarar",
    "No enviar información / Medios Magnéticos",
    "Facturación",
    "Omisión de activos / Pasivos inexistentes",
    "Otro"
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

# --- BARRA LATERAL: DESCARGA DE BASE DE DATOS EXCEL ---
with st.sidebar:
    st.header("📥 Base de Datos")
    st.write("Descarga el consolidado de la gestión registrada.")
    
    if os.path.exists(ARCHIVO_SALIDA):
        df_descarga = pd.read_csv(ARCHIVO_SALIDA)
        
        # Convertir a Excel en memoria
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_descarga.to_excel(writer, index=False, sheet_name='Gestión Intensiva')
        
        st.download_button(
            label="Descargar Base en Excel (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"Base_Gestion_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
        st.success(f"Hay {len(df_descarga)} registros guardados.")
    else:
        st.info("Aún no hay registros en la base de datos.")

# --- INTERFAZ GRÁFICA PRINCIPAL ---
st.title("📊 Registro de Gestión - Fiscalización Intensiva")
st.markdown("Diligencie el formulario. El sistema asigna por defecto la **División 262**.")

with st.form("registro_form"):
    st.header("1. Datos Básicos")
    col1, col2, col3 = st.columns(3)
    with col1:
        cc_funcionario = st.text_input("C.C. del Funcionario Auditor")
    with col2:
        nombre_funcionario = st.text_input("Nombre del Funcionario")
    with col3:
        concepto_sistema = st.selectbox("Concepto y/o Sistema", options=SISTEMAS)

    # Asignación automática de la dependencia
    st.text_input("Dependencia", value="262 - División Fiscalización y Liquidación Tributaria Intensiva", disabled=True)
    
    st.header("2. Datos del Contribuyente y Acto")
    col4, col5 = st.columns(2)
    with col4:
        nit = st.text_input("NIT del contribuyente")
        razon_social = st.text_input("Nombre o Razón Social")
    
    with col5:
        tipo_acto = st.selectbox("Tipo de Acto", options=TIPOS_ACTOS)
        fecha_acto = st.date_input("Fecha del Acto")
        no_acto = st.text_input("No. del Acto")
        
    st.header("3. Parámetros Tributarios")
    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        cp = st.selectbox("CP (Concepto de Pago)", options=CONCEPTOS_PAGO)
    with col7:
        ag = st.text_input("AG (Año Gravable)")
    with col8:
        ac = st.text_input("AC (Año Calendario/Acto)")
    with col9:
        # Mejora: Ahora es un menú desplegable
        cs = st.selectbox("CS (Concepto Sanción)", options=CONCEPTOS_SANCION)
    with col10:
        periodo = st.text_input("Periodo (1-6)")
        
    impuesto = st.selectbox("Tipo de Impuesto", options=IMPUESTOS)
    origen = st.selectbox("Origen de la Investigación", options=ORIGENES_INVESTIGACION)
    concepto_gestion = st.selectbox("Concepto de Gestión", options=CONCEPTOS_GESTION)

    st.header("4. Valores de Gestión Recuperada")
    col11, col12 = st.columns(2)
    with col11:
        v1 = st.number_input("1. Mayor valor a pagar (impuesto + sanciones)", min_value=0.0, format="%.2f", step=1000.0)
        v2 = st.number_input("2. Menor saldo a favor", min_value=0.0, format="%.2f", step=1000.0)
        v3 = st.number_input("3. Sanciones Aceptadas (pliegos, resolución, voluntarias)", min_value=0.0, format="%.2f", step=1000.0)
    with col12:
        v4 = st.number_input("4. Intereses pagados (corrección, inicial, reintegro)", min_value=0.0, format="%.2f", step=1000.0)
        v5 = st.number_input("5. Resoluciones sanción plenas ejecutoriadas", min_value=0.0, format="%.2f", step=1000.0)
        v6 = st.number_input("6. Liquidaciones oficiales ejecutoriadas", min_value=0.0, format="%.2f", step=1000.0)
    
    observaciones = st.text_area("Observaciones adicionales (Opcional)")

    submit_button = st.form_submit_button(label="💾 Guardar Registro de Gestión")

# --- LÓGICA DE GUARDADO ---
if submit_button:
    if not cc_funcionario or not nit:
        st.warning("⚠️ Por favor, diligencie al menos la C.C. del Funcionario y el NIT del contribuyente.")
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
            archivo_existe = os.path.isfile(ARCHIVO_SALIDA)
            
            if archivo_existe:
                df_existente = pd.read_csv(ARCHIVO_SALIDA)
                nuevo_registro["No."] = len(df_existente) + 1
                df_nuevo = pd.DataFrame([nuevo_registro])
                df_nuevo.to_csv(ARCHIVO_SALIDA, mode='a', header=False, index=False, encoding='utf-8')
            else:
                nuevo_registro["No."] = 1
                df_nuevo = pd.DataFrame([nuevo_registro])
                cols = ["No."] + [col for col in df_nuevo.columns if col != "No."]
                df_nuevo = df_nuevo[cols]
                df_nuevo.to_csv(ARCHIVO_SALIDA, index=False, encoding='utf-8')

            st.success(f"✅ ¡Gestión registrada! Total: **${total_gestion:,.2f}**")
            st.rerun() 
            
        except Exception as e:
            st.error(f"❌ Error al guardar: {e}")
