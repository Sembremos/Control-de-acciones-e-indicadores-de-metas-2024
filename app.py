import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# -----------------------------------------
# 🔧 CONFIGURACIÓN SUPABASE
# -----------------------------------------
SUPABASE_URL = "https://zutgkfioubpepebjraid.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1dGdrZmlvdWJwZXBlYmpyYWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwNTA4MDksImV4cCI6MjA2NjYyNjgwOX0.dUzaSY2YC9Jp1oQEClKTDvaRZMNEzmwd486XY-ibPS8"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------------------
# 🧱 FUNCIONES BASE DE DATOS
# -----------------------------------------
def insertar_respuesta(data: dict):
    try:
        return supabase.table("respuestas").insert(data).execute()
    except Exception as e:
        st.error("❌ Error al guardar los datos en Supabase.")
        st.exception(e)
        return None

def obtener_respuestas():
    response = supabase.table("respuestas").select("*").execute()
    return response.data if response.data else []

def actualizar_respuesta(id_respuesta: int, nuevos_datos: dict):
    return supabase.table("respuestas").update(nuevos_datos).eq("id", id_respuesta).execute()

def eliminar_respuesta(id_respuesta: int):
    return supabase.table("respuestas").delete().eq("id", id_respuesta).execute()

# -----------------------------------------
# ⚙️ CONFIG STREAMLIT Y LISTA BASE
# -----------------------------------------
st.set_page_config(page_title="Seguimiento Delegaciones", layout="wide")
st.title("📋 Seguimiento de Líneas de Acción por Delegación")

# Lista completa de delegaciones
delegaciones = sorted([
    'D01 - Carmen', 'D02 - Merced', 'D03 - Hospital', 'D04 - Catedral', 'D05 - San Sebastián',
    'D06 - Hatillo', 'D07 - Zapote / San Francisco', 'D08 - Pavas', 'D09 - Uruca',
    'D10 - Curridabat', 'D11 - Montes de Oca', 'D12 - Goicoechea', 'D13 - Moravia', 'D14 - Tibás',
    'D16 - Desamparados Norte', 'D17 - Desamparados Sur', 'D18 - Aserrí', 'D19 - Acosta',
    'D20 - Alajuelita', 'D21 - Escazú', 'D22 - Santa Ana', 'D23 - Mora', 'D24 - Puriscal',
    'D25 - Turrubares', 'D26 - Alajuela Sur', 'D27 - Alajuela Norte', 'D28 - San Ramón',
    'D29 - Grecia', 'D30 - San Mateo', 'D31 - Atenas', 'D32 - Naranjo', 'D33 - Palmares',
    'D34 - Poás', 'D35 - Orotina', 'D36 - Sarchí', 'D37 - Cartago', 'D38 - Paraíso',
    'D39 - La Unión', 'D40 - Jiménez', 'D41 - Turrialba', 'D42 - Alvarado', 'D43 - Oreamuno',
    'D44 - El Guarco', 'D45 - Tarrazú', 'D46 - Dota', 'D47 - León Cortéz', 'D48 - Guadalupe',
    'D49 - Heredia', 'D50 - Barva', 'D51 - Santo Domingo', 'D52 - Santa Bárbara', 'D53 - San Rafael',
    'D54 - San Isidro', 'D55 - Belén', 'D56 - Flores', 'D57 - San Pablo', 'D58 - Sarapiquí',
    'D59 - Colorado', 'D60 - Liberia', 'D61 - Nicoya', 'D62 - Santa Cruz', 'D63 - Bagaces',
    'D64 - Carrillo', 'D65 - Cañas', 'D66 - Abangares', 'D67 - Tilarán', 'D68 - Nandayure',
    'D69 - Hojancha', 'D70 - La Cruz', 'D71 - Puntarenas', 'D72 - Esparza', 'D73 - Montes de Oro',
    'D74 - Quepos', 'D75 - Parrita', 'D76 - Garabito', 'D77 - Paquera', 'D78 - Judas de Chomes',
    'D79 - Pérez Zeledón', 'D80 - Buenos Aires', 'D81 - Osa', 'D82E - San Carlos Este',
    'D82O - San Carlos Oeste', 'D83 - Zarcero', 'D84 - Upala', 'D85 - Los Chiles',
    'D86 - Guatuso', 'D87 - Río Cuarto', 'D88 - Limón', 'D89 - Pococí', 'D90 - Siquirres',
    'D91 - Talamanca', 'D92 - Matina', 'D93 - Guácimo', 'D94 - Golfito', 'D95 - Coto Brus',
    'D96 - Corredores', 'D97 - Puerto Jiménez'
])

# Inicializar estado de edición
if "modo_edicion" not in st.session_state:
    st.session_state["modo_edicion"] = False
if "respuesta_editando" not in st.session_state:
    st.session_state["respuesta_editando"] = None
# -----------------------------------------
# 📝 REGISTRO DE LÍNEAS DE ACCIÓN
# -----------------------------------------
st.markdown("### ✏️ Registro de líneas de acción estratégicas")

delegacion = st.selectbox("📍 Selecciona una delegación", delegaciones)

tipo_lider = st.selectbox(
    "👤 Tipo de liderazgo estratégico",
    ["Fuerza Pública", "Gobierno Local", "Fuerza Pública y Gobierno Local"]
)

# Lista COMPLETA de líneas de acción
lineas_accion = [
    "ABANDONO DE PERSONAS (MENOR DE EDAD, ADULTO MAYOR O CON CAPACIDADES DIFERENTES)",
    "ABIGEATO (ROBO Y DESTACE DE GANADO)",
    "ABORTO",
    "ABUSO DE AUTORIDAD",
    "ACCIDENTES DE TRANSITO",
    "ACCIONAMIENTO DE ARMA DE FUEGO (BALACERAS)",
    "ACOSO ESCOLAR (BULLYING)",
    "ACOSO LABORAL (MOBBING)",
    "ACOSO SEXUAL CALLEJERO",
    "ACTOS OBSCENOS EN VIA PUBLICA",
    "ADMINISTRACION FRAUDULENTA, APROPIACIONES INDEBIDAS O ENRIQUECIMIENTO ILICITO",
    "AGRESION CON ARMAS",
    "AGRUPACIONES DELINCUENCIALES NO ORGANIZADAS",
    "ALTERACIÓN DE DATOS Y SABOTAJE INFORMÁTICO",
    "AMBIENTE LABORAL INADECUADO",
    "AMENAZAS",
    "ANALFABETISMO",
    "ASALTO (A PERSONAS, COMERCIO, VIVIENDA, TRANSPORTE PÚBLICO)",
    "BAJOS SALARIOS",
    "BARES CLANDESTINOS",
    "BARRAS DE FUTBOL",
    "BUNKER (VENTA Y CONSUMO DE DROGAS)",
    "CALUMNIA",
    "CAZA ILEGAL",
    "CONDUCCION TEMERARIA",
    "CONSUMO DE ALCOHOL EN VÍA PÚBLICA",
    "CONSUMO DE DROGAS",
    "CONTAMINACION SONICA",
    "CONTRABANDO",
    "CORRUPCION",
    "CORRUPCION POLICIAL",
    "CULTIVO DE DROGA (MARIHUANA)",
    "DAÑO AMBIENTAL",
    "DAÑOS/VANDALISMO",
    "DEFICENCIA EN LA INFRAESTRUCTURA VIAL",
    "DEFICIENCIA EN LA LINEA 9-1-1",
    "DEFICIENCIAS EN EL ALUMBRADO PUBLICO",
    "DELICUENCIA ORGANIZADA",
    "DELITOS CONTRA EL AMBITO DE INTIMIDAD (VIOLACIÓN DE SECRETOS (CORRESPONDENCIA Y COMUNICACIONES ELECTRONICAS))",
    "DELITOS CONTRA LA VIDA (HOMICIDIOS, HERIDOS)",
    "DELITOS SEXUALES",
    "DESAPARICION DE PERSONAS",
    "DESARTICULACION INTERINSTITUCIONAL",
    "DESOBEDIENCIA",
    "DESORDENES EN VIA PUBLICA",
    "DESVINCULACIÓN ESTUDIANTIL",
    "DISTURBIOS (RIÑAS)",
    "ENFRENTAMIENTOS ESTUDIANTILES",
    "ESTAFA O DEFRAUDACION",
    "ESTUPRO (DELITOS SEXUALES CONTRA MENOR DE EDAD)",
    "EVASIÓN Y QUEBRANTAMIENTO DE PENA",
    "EXPLOSIVOS",
    "EXPLOTACIÓN LABORAL INFANTIL",
    "EXPLOTACIÓN SEXUAL INFANTIL",
    "EXTORSION",
    "FABRICACIÓN, PRODUCCIÓN O REPRODUCCIÓN DE PORNOGRAFÍA",
    "FACILISMO ECONOMICO",
    "FALSIFICACION DE MONEDA Y OTROS VALORES.",
    "FALTA DE CAMARAS DE SEGURIDAD",
    "FALTA DE CAPACITACION POLICIAL",
    "FALTA DE CONTROL A PATENTES",
    "FALTA DE CONTROL FRONTERIZO",
    "FALTA DE CORRESPONSABILIDAD EN SEGURIDAD",
    "FALTA DE CULTURA VIAL",
    "FALTA DE CULTURA Y COMPROMISO CIUDADANO",
    "FALTA DE EDUCACION FAMILIAR",
    "FALTA DE INCENTIVOS",
    "FALTA DE INVERSION SOCIAL",
    "FALTA DE LEGISLACION DE EXTINCION DE DOMINIO",
    "FALTA DE OPORTUNIDADES LABORALES",
    "FALTA DE PERSONAL ADMINISTRATIVO",
    "FALTA DE PERSONAL POLICIAL",
    "FALTA DE POLICIAS DE TRANSITO",
    "FALTA DE POLITICAS PUBLICAS EN SEGURIDAD",
    "FALTA DE PRESENCIA POLICIAL",
    "FALTA DE SALUBRIDAD PUBLICA",
    "FAMILIAS DISFUNCIONALES",
    "FEMICIDIO",
    "FRAUDE INFORMATICO",
    "GROOMING",
    "HACINAMIENTO CARCELARIO",
    "HACINAMIENTO POLICIAL",
    "HOMICIDIO",
    "HOSPEDAJES ILEGALES (CUARTERIAS)",
    "HURTO",
    "INADECUADO USO DEL RECURSO POLICIAL",
    "INCUMPLIMIENTO AL PLAN REGULADOR DE LA MUNICIPALIDAD",
    "INCUMPLIMIENTO DEL  DEBER ALIMENTARIO",
    "INDIFERENCIA SOCIAL",
    "INEFECTIVIDAD EN EL SERVICIO DE POLICIA",
    "INEFICIENCIA EN LA ADMINISTRACION DE JUSTICIA",
    "INFRAESTRUCTURA INADECUADA",
    "INTOLERANCIA SOCIAL",
    "IRRESPETO A LA JEFATURA",
    "IRRESPETO AL SUBALTERNO",
    "JORNADAS LABORALES EXTENSAS",
    "LAVADO DE ACTIVOS",
    "LESIONES",
    "LEY DE ARMAS Y EXPLOSIVOS N° 7530",
    "LEY DE CONTROL DE TABACO (LEY 9028)",
    "LOTES BALDIOS",
    "MALTRATO ANIMAL",
    "MENORES EN VULNERABILIDAD",
    "MINERIA ILEGAL",
    "NARCOTRAFICO",
    "NECESIDADES BASICAS INSATISFECHAS",
    "PERCEPCION DE INSEGURIDAD",
    "PERDIDA DE ESPACIOS PUBLICOS",
    "PERSONAS CON EXCESO DE TIEMPO DE OCIO",
    "PERSONAS EN ESTADO MIGRATORIO IRREGULAR",
    "PERSONAS EN SITUACION DE CALLE",
    "PESCA ILEGAL",
    "PORTACION ILEGAL DE ARMAS",
    "PRESENCIA MULTICULTURAL",
    "PRESION POR RESULTADOS OPERATIVOS",
    "PRIVACIÓN DE LIBERTAD SIN ÁNIMO DE LUCRO",
    "PROBLEMAS VECINALES",
    "RECEPTACION",
    "RELACIONES IMPROPIAS",
    "RESISTENCIA (IRRESPETO A LA AUTORIDAD)",
    "ROBO A COMERCIO (INTIMIDACION)",
    "ROBO A COMERCIO (TACHA)",
    "ROBO A EDIFICACIÓN (TACHA)",
    "ROBO A EMBARCACIONES (TACHA)",
    "ROBO A PERSONAS",
    "ROBO A TRANSPORTE COMERCIAL",
    "ROBO A TRANSPORTE PÚBLICO CON INTIMIDACIÓN",
    "ROBO A VEHICULOS (TACHA)",
    "ROBO A VIVIENDA (INTIMIDACION)",
    "ROBO A VIVIENDA\n(TACHA)",
    "ROBO DE BICICLETA",
    "ROBO DE CABLE",
    "ROBO DE COMBUSTIBLE",
    "ROBO DE CULTIVOS",
    "ROBO DE EMBARCACIONES",
    "ROBO DE EQUIPO AGRICOLA",
    "ROBO DE GANADO Y AGRÍCOLA",
    "ROBO DE MOTOCICLETAS/VEHICULOS(BAJONAZO)",
    "ROBO DE VEHICULOS",
    "SECUESTRO",
    "SIMULACION DE DELITO",
    "SISTEMA JURIDICO DESACTUALIZADO",
    "SUICIDIO",
    "SUSTRACCION DE UNA PERSONA MENOR DE EDAD O INCAPAZ.",
    "TALA ILEGAL",
    "TENDENCIA SOCIAL HACIA EL DELITO (PAUTAS DE CRIANZA VIOLENTA)",
    "TENENCIA DE DROGA",
    "TENTATIVA DE HOMICIDIO",
    "TERRORISMO",
    "TRABAJO INFORMAL",
    "TRAFICO DE ARMAS",
    "TRAFICO DE INFLUENCIAS",
    "TRÁFICO ILEGAL DE PERSONAS",
    "TRANSPORTE INFORMAL (UBER, PORTEADORES, PIRATAS)",
    "TRATA DE PERSONAS",
    "TURBACIÓN DE ACTOS RELIGIOSOS Y PROFANACIONES",
    "USO ILEGAL DE UNIFORMES, INSIGNIAS O DISPOSITIVOS POLICIALES",
    "USURPACION DE TERRENOS (PRECARIOS)",
    "VENTA DE DROGAS",
    "VENTA Y CONSUMO DE DROGAS EN VÍA PÚBLICA",
    "VENTAS INFORMALES (AMBULANTES)",
    "VIGILANCIA INFORMAL",
    "VIOLACIÓN DE DOMICILIO",
    "VIOLACIÓN DE LA CUSTODIA DE LAS COSAS",
    "VIOLACIÓN DE SELLOS",
    "VIOLENCIA DE GENERO",
    "VIOLENCIA INTRAFAMILIAR",
    "XENOFOBIA",
    "ZONAS DE PROSTITUCION",
    "ZONAS VULNERABLES"
]

lineas_seleccionadas = st.multiselect("📚 Selecciona una o más líneas de acción", lineas_accion)

if delegacion and tipo_lider and lineas_seleccionadas:
    for linea in lineas_seleccionadas:
        with st.expander(f"📄 Línea de Acción: {linea}"):
            with st.form(key=f"form_{linea}"):
                tipo_indicador = st.text_input("🧭 Tipo de Indicador", key=f"indicador_{linea}")
                meta = st.text_input("🎯 Meta (puede ser texto o número)", key=f"meta_{linea}")
                estado = st.selectbox(
                    "📈 Estado actual",
                    ["", "Completa", "Con actividades", "Sin actividades"],
                    index=0,
                    key=f"estado_{linea}"
                )

                col1, col2, col3, col4 = st.columns(4)
                t1 = col1.number_input("T1", min_value=0, step=1, key=f"t1_{linea}")
                t2 = col2.number_input("T2", min_value=0, step=1, key=f"t2_{linea}")
                t3 = col3.number_input("T3", min_value=0, step=1, key=f"t3_{linea}")
                t4 = col4.number_input("T4", min_value=0, step=1, key=f"t4_{linea}")

                detalle = st.text_area("📝 Detalle del cumplimiento", key=f"detalle_{linea}")

                submit = st.form_submit_button("💾 Guardar registro")

                if submit:
                    datos = {
                        "delegacion": delegacion,
                        "tipo": tipo_lider,
                        "linea": linea,
                        "indicador": tipo_indicador or None,
                        "meta": meta or None,
                        "estado": estado or None,
                        "trimestre1": t1,
                        "trimestre2": t2,
                        "trimestre3": t3,
                        "trimestre4": t4,
                        "detalle": detalle or None
                    }
                    respuesta = insertar_respuesta(datos)
                    if respuesta:
                        st.success(f"✅ Registro guardado para: {linea}")
                        st.rerun()
# -----------------------------------------
# 📊 VISUALIZACIÓN Y GESTIÓN DE RESPUESTAS
# -----------------------------------------
st.markdown("---")
st.subheader("📁 Respuestas guardadas")

respuestas = obtener_respuestas()

if respuestas:
    df = pd.DataFrame(respuestas)

    # Asegurarse de que la fecha esté bien formateada
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%d/%m/%Y")

    # Filtros dinámicos
    col1, col2, col3 = st.columns(3)

    delegaciones_disponibles = sorted(df["delegacion"].dropna().unique())
    tipos_disponibles = sorted(df["tipo"].dropna().unique())
    trimestres = ["Todos", "1", "2", "3", "4"]

    filtro_delegacion = col1.selectbox("📍 Filtrar por delegación", ["Todas"] + delegaciones_disponibles)
    filtro_tipo = col2.selectbox("👤 Filtrar por tipo de liderazgo", ["Todos"] + tipos_disponibles)
    filtro_trimestre = col3.selectbox("📅 Filtrar por trimestre", trimestres)

    df_filtrado = df.copy()

    if filtro_delegacion != "Todas":
        df_filtrado = df_filtrado[df_filtrado["delegacion"] == filtro_delegacion]
    if filtro_tipo != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tipo"] == filtro_tipo]
    if filtro_trimestre in ["1", "2", "3", "4"]:
        df_filtrado = df_filtrado[df_filtrado[f"trimestre{filtro_trimestre}"] > 0]

    df_filtrado = df_filtrado.sort_values(by=["delegacion", "tipo", "linea"])

    st.markdown("### 📌 Detalles por línea de acción")

    for _, fila in df_filtrado.iterrows():
        with st.expander(f"🗂️ {fila['delegacion']} - {fila['linea']} ({fila['tipo']}) [{fila.get('estado', '')}]"):
            st.write(f"**Tipo de Indicador:** {fila.get('indicador', '')}")
            st.write(f"**Meta:** {fila.get('meta', '')}")
            st.write(f"**Trimestre 1:** {fila.get('trimestre1', 0)}")
            st.write(f"**Trimestre 2:** {fila.get('trimestre2', 0)}")
            st.write(f"**Trimestre 3:** {fila.get('trimestre3', 0)}")
            st.write(f"**Trimestre 4:** {fila.get('trimestre4', 0)}")
            st.write(f"**Detalle:** {fila.get('detalle', '')}")
            st.write(f"**Fecha:** {fila.get('fecha', '')}")

            col_edit, col_del = st.columns(2)
            if col_edit.button("✏️ Editar", key=f"editar_{fila['id']}"):
                st.session_state["modo_edicion"] = True
                st.session_state["respuesta_editando"] = fila.to_dict()
                st.rerun()

            if col_del.button("🗑️ Eliminar", key=f"eliminar_{fila['id']}"):
                eliminar_respuesta(fila["id"])
                st.success("✅ Registro eliminado correctamente.")
                st.rerun()
else:
    st.info("Aún no hay respuestas registradas.")
# -----------------------------------------
# ✏️ MODO EDICIÓN DE RESPUESTA
# -----------------------------------------
respuesta_editando = st.session_state.get("respuesta_editando")
modo_edicion = st.session_state.get("modo_edicion")

if modo_edicion and isinstance(respuesta_editando, dict):
    st.markdown("---")
    st.subheader("✏️ Editar registro existente")

    fila = respuesta_editando

    with st.form("form_editar_respuesta"):
        st.write(f"🗂️ **Delegación:** {fila['delegacion']}")
        st.write(f"👤 **Tipo de liderazgo:** {fila['tipo']}")
        st.write(f"📚 **Línea de acción:** {fila['linea']}")

        tipo_indicador = st.text_input("🧭 Tipo de Indicador", value=fila.get("indicador", "") or "")
        meta = st.text_input("🎯 Meta", value=fila.get("meta", "") or "")

        estado_opciones = ["Completa", "Con actividades", "Sin actividades"]
        estado_actual = fila.get("estado", "")
        estado_index = estado_opciones.index(estado_actual) if estado_actual in estado_opciones else 0
        estado = st.selectbox("📈 Estado", [""] + estado_opciones, index=estado_index + 1 if estado_actual in estado_opciones else 0)

        col1, col2, col3, col4 = st.columns(4)
        t1 = col1.number_input("T1", min_value=0, step=1, value=int(fila.get("trimestre1", 0)))
        t2 = col2.number_input("T2", min_value=0, step=1, value=int(fila.get("trimestre2", 0)))
        t3 = col3.number_input("T3", min_value=0, step=1, value=int(fila.get("trimestre3", 0)))
        t4 = col4.number_input("T4", min_value=0, step=1, value=int(fila.get("trimestre4", 0)))

        detalle = st.text_area("📝 Detalle del cumplimiento", value=fila.get("detalle", "") or "")

        col_guardar, col_cancelar = st.columns(2)
        guardar = col_guardar.form_submit_button("💾 Guardar Cambios")
        cancelar = col_cancelar.form_submit_button("❌ Cancelar")

        if guardar:
            nuevos_datos = {
                "indicador": tipo_indicador or None,
                "meta": meta or None,
                "estado": estado or None,
                "trimestre1": t1,
                "trimestre2": t2,
                "trimestre3": t3,
                "trimestre4": t4,
                "detalle": detalle or None
            }
            actualizar_respuesta(fila["id"], nuevos_datos)
            st.success("✅ Registro actualizado correctamente.")
            st.session_state["modo_edicion"] = False
            st.session_state["respuesta_editando"] = None
            st.rerun()

        if cancelar:
            st.warning("❌ Edición cancelada.")
            st.session_state["modo_edicion"] = False
            st.session_state["respuesta_editando"] = None
            st.rerun()
# -----------------------------------------
# 📥 DESCARGA DE RESPALDO EN EXCEL (CSV)
# -----------------------------------------
st.markdown("---")
st.subheader("📤 Descargar respaldo de información")

if respuestas:
    df_exportar = pd.DataFrame(respuestas)

    # Orden lógico de columnas esperadas
    columnas_ordenadas = [
        "delegacion", "tipo", "linea", "indicador", "meta", "estado",
        "trimestre1", "trimestre2", "trimestre3", "trimestre4",
        "detalle", "fecha"
    ]
    columnas_existentes = [col for col in columnas_ordenadas if col in df_exportar.columns]
    df_exportar = df_exportar[columnas_existentes].copy()

    # Formato legible para la fecha
    if "fecha" in df_exportar.columns:
        df_exportar["fecha"] = pd.to_datetime(df_exportar["fecha"]).dt.strftime("%d/%m/%Y")

    # Renombrar columnas para presentación en Excel
    df_exportar.rename(columns={
        "delegacion": "Delegación",
        "tipo": "Tipo de Liderazgo",
        "linea": "Línea de Acción",
        "indicador": "Tipo de Indicador",
        "meta": "Meta",
        "estado": "Estado",
        "trimestre1": "Trimestre 1",
        "trimestre2": "Trimestre 2",
        "trimestre3": "Trimestre 3",
        "trimestre4": "Trimestre 4",
        "detalle": "Detalle del Cumplimiento",
        "fecha": "Fecha de Registro"
    }, inplace=True)

    # Generar archivo CSV
    csv = df_exportar.to_csv(index=False).encode("utf-8")

    # Botón de descarga
    st.download_button(
        label="📄 Descargar en Excel (CSV)",
        data=csv,
        file_name="respuestas_seguimiento.csv",
        mime="text/csv"
    )
else:
    st.info("No hay información disponible para descargar.")



