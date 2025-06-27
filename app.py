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
    response = supabase.table("respuestas").insert(data).execute()
    return response

def obtener_respuestas():
    response = supabase.table("respuestas").select("*").execute()
    return response.data if response.data else []

def actualizar_respuesta(id_respuesta: int, nuevos_datos: dict):
    response = supabase.table("respuestas").update(nuevos_datos).eq("id", id_respuesta).execute()
    return response

def eliminar_respuesta(id_respuesta: int):
    response = supabase.table("respuestas").delete().eq("id", id_respuesta).execute()
    return response

# -----------------------------------------
# ⚙️ CONFIG STREAMLIT Y LISTA BASE
# -----------------------------------------
st.set_page_config(page_title="Seguimiento Delegaciones", layout="wide")
st.title("📋 Seguimiento de Líneas de Acción por Delegación")

# Lista de delegaciones válidas
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

# Inicialización de estados de edición
if "modo_edicion" not in st.session_state:
    st.session_state["modo_edicion"] = False
if "respuesta_editando" not in st.session_state:
    st.session_state["respuesta_editando"] = None
# -----------------------------------------
# 📝 REGISTRO DE LÍNEAS DE ACCIÓN
# -----------------------------------------
st.markdown("### ✏️ Registrar evaluación por delegación")

delegacion = st.selectbox("Selecciona una delegación", delegaciones)

if delegacion:
    tipo_lineas = st.multiselect(
        "Selecciona el/los tipo(s) de línea de acción",
        ["Fuerza Pública", "Gobierno Local"]
    )

    for tipo in tipo_lineas:
        st.markdown(f"---\n#### 🛡️ Evaluación para: {tipo}")

        lineas = st.multiselect(
            f"Número(s) de línea de acción para {tipo} (1-10)",
            list(range(1, 11)),
            key=f"lineas_{tipo}"
        )

        for linea_num in lineas:
            with st.expander(f"📄 Línea de Acción #{linea_num} - {tipo}"):
                with st.form(key=f"form_{tipo}_{linea_num}"):

                    accion = st.radio("¿Cumple Acción Estratégica?", ["Sí", "No"], key=f"accion_{tipo}_{linea_num}")
                    indicador = st.radio("¿Cumple Indicador?", ["Sí", "No"], key=f"indicador_{tipo}_{linea_num}")
                    meta = st.radio("¿Cumple Meta?", ["Sí", "No"], key=f"meta_{tipo}_{linea_num}")
                    lider = st.radio("¿Líder Estratégico Asignado?", ["Sí", "No"], key=f"lider_{tipo}_{linea_num}")
                    cogestores = st.radio("¿Hay Cogestores Identificados?", ["Sí", "No"], key=f"cogestores_{tipo}_{linea_num}")

                    observacion = st.text_area("📝 Observación general", key=f"observacion_{tipo}_{linea_num}")

                    submitted = st.form_submit_button("Guardar Evaluación")

                    if submitted:
                        # Evaluar estado final
                        if meta == "No":
                            estado = "❌ Incompleto"
                        elif accion == "Sí" and indicador == "Sí" and lider == "Sí" and cogestores == "Sí":
                            estado = "✅ Completo"
                        else:
                            estado = "🕗 Pendiente"

                        # Preparar registro
                        nuevo_registro = {
                            "delegacion": delegacion,
                            "tipo": tipo,
                            "linea": linea_num,
                            "accion": accion,
                            "indicador": indicador,
                            "meta": meta,
                            "lider": lider,
                            "cogestores": cogestores,
                            "observacion": observacion,
                            "estado": estado,
                            "fecha": datetime.now().isoformat()
                        }

                        insertar_respuesta(nuevo_registro)

                        st.success(f"✅ Evaluación registrada para Línea #{linea_num} - {tipo}")

                        # Limpiar los campos del formulario
                        st.session_state[f"accion_{tipo}_{linea_num}"] = None
                        st.session_state[f"indicador_{tipo}_{linea_num}"] = None
                        st.session_state[f"meta_{tipo}_{linea_num}"] = None
                        st.session_state[f"lider_{tipo}_{linea_num}"] = None
                        st.session_state[f"cogestores_{tipo}_{linea_num}"] = None
                        st.session_state[f"observacion_{tipo}_{linea_num}"] = ""
# -----------------------------------------
# 📊 VISUALIZACIÓN Y GESTIÓN DE RESPUESTAS
# -----------------------------------------
st.markdown("---")
st.subheader("📁 Respuestas guardadas")

respuestas = obtener_respuestas()

if respuestas:
    df = pd.DataFrame(respuestas)
    df = df.sort_values(by=["delegacion", "tipo", "linea"])

    # Convertir fecha al formato dd/mm/yyyy
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%d/%m/%Y")

    st.dataframe(df, use_container_width=True)

    # Agrupador por delegación
    delegaciones_disponibles = df["delegacion"].unique().tolist()
    delegacion_filtro = st.selectbox("🔍 Filtrar por delegación", ["Todas"] + delegaciones_disponibles)

    if delegacion_filtro != "Todas":
        df_filtrado = df[df["delegacion"] == delegacion_filtro]
    else:
        df_filtrado = df

    st.markdown("### 📌 Detalles por delegación")
    for idx, fila in df_filtrado.iterrows():
        with st.expander(f"🗂️ {fila['delegacion']} - Línea {fila['linea']} ({fila['tipo']}) [{fila['estado']}]"):
            st.write(f"**Acción Estratégica:** {fila['accion']}")
            st.write(f"**Indicador:** {fila['indicador']}")
            st.write(f"**Meta:** {fila['meta']}")
            st.write(f"**Líder Estratégico:** {fila['lider']}")
            st.write(f"**Cogestores:** {fila['cogestores']}")
            st.write(f"**Observación:** {fila['observacion']}")
            st.write(f"**Fecha:** {fila['fecha']}")

            col1, col2 = st.columns(2)
            if col1.button("✏️ Editar", key=f"editar_{fila['id']}"):
                st.session_state["modo_edicion"] = True
                st.session_state["respuesta_editando"] = fila.to_dict()  # ← CORREGIDO

            if col2.button("🗑️ Eliminar", key=f"eliminar_{fila['id']}"):
                eliminar_respuesta(fila["id"])
                st.success("🗑️ Respuesta eliminada correctamente.")
                st.experimental_rerun()

    # Botón de descarga
    st.markdown("### 📥 Descargar todas las respuestas")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📄 Descargar en CSV", csv, "respuestas_delegaciones.csv", "text/csv")

else:
    st.info("Aún no hay respuestas registradas.")
# -----------------------------------------
# ✏️ MODO EDICIÓN DE RESPUESTA
# -----------------------------------------
respuesta_editando = st.session_state.get("respuesta_editando")
modo_edicion = st.session_state.get("modo_edicion")

if modo_edicion and isinstance(respuesta_editando, dict):
    st.markdown("---")
    st.subheader("✏️ Editar respuesta registrada")

    fila = respuesta_editando

    with st.form("form_editar_respuesta"):
        accion = st.radio("¿Cumple Acción Estratégica?", ["Sí", "No"], index=0 if fila["accion"] == "Sí" else 1)
        indicador = st.radio("¿Cumple Indicador?", ["Sí", "No"], index=0 if fila["indicador"] == "Sí" else 1)
        meta = st.radio("¿Cumple Meta?", ["Sí", "No"], index=0 if fila["meta"] == "Sí" else 1)
        lider = st.radio("¿Líder Estratégico Asignado?", ["Sí", "No"], index=0 if fila["lider"] == "Sí" else 1)
        cogestores = st.radio("¿Hay Cogestores Identificados?", ["Sí", "No"], index=0 if fila["cogestores"] == "Sí" else 1)
        observacion = st.text_area("📝 Observación general", value=fila["observacion"])

        col1, col2 = st.columns(2)
        guardar = col1.form_submit_button("💾 Guardar Cambios")
        cancelar = col2.form_submit_button("❌ Cancelar")

        if guardar:
            # Evaluar nuevo estado
            if meta == "No":
                estado = "❌ Incompleto"
            elif accion == "Sí" and indicador == "Sí" and lider == "Sí" and cogestores == "Sí":
                estado = "✅ Completo"
            else:
                estado = "🕗 Pendiente"

            nuevos_datos = {
                "accion": accion,
                "indicador": indicador,
                "meta": meta,
                "lider": lider,
                "cogestores": cogestores,
                "observacion": observacion,
                "estado": estado,
                "fecha": datetime.now().isoformat()
            }

            actualizar_respuesta(fila["id"], nuevos_datos)
            st.success("✅ Respuesta actualizada correctamente.")
            st.session_state["modo_edicion"] = False
            st.session_state["respuesta_editando"] = None
            st.experimental_rerun()

        if cancelar:
            st.session_state["modo_edicion"] = False
            st.session_state["respuesta_editando"] = None
            st.warning("⚠️ Edición cancelada.")



