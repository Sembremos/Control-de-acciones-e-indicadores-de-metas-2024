# -------------------------------------------
# app.py — Pestaña 1: Registro de Evaluaciones
# -------------------------------------------

import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# ---------- Conexión Supabase ----------
SUPABASE_URL = "https://zutgkfioubpepebjraid.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1dGdrZmlvdWJwZXBlYmpyYWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwNTA4MDksImV4cCI6MjA2NjYyNjgwOX0.dUzaSY2YC9Jp1oQEClKTDvaRZMNEzmwd486XY-ibPS8"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- Funciones ----------
def insertar_respuesta(data):
    response = supabase.table("respuestas").insert(data).execute()
    return response

def obtener_respuestas():
    response = supabase.table("respuestas").select("*").execute()
    return response.data if response.data else []

def eliminar_respuesta(respuesta_id):
    supabase.table("respuestas").delete().eq("id", respuesta_id).execute()

# ---------- Configuración ----------
st.set_page_config(page_title="Control de Indicadores", layout="wide")
st.title("📋 Registro de Evaluación por Delegación")

# ---------- Lista de delegaciones ----------
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
# ---------- Evaluación por delegación ----------

delegacion = st.selectbox("Selecciona una delegación", delegaciones)

if delegacion:
    st.subheader("Tipo de línea de acción")
    tipo_lineas = st.multiselect(
        "Puede seleccionar uno o ambos tipos",
        ["Fuerza Pública", "Gobierno Local"]
    )

    for tipo in tipo_lineas:
        st.markdown(f"---\n### 🛡️ Registro para: {tipo}")

        lineas = st.multiselect(
            f"Líneas de acción del {tipo} (1-10)",
            list(range(1, 11)),
            key=f"lineas_{tipo}"
        )

        for linea_num in lineas:
            with st.expander(f"📄 Línea de Acción #{linea_num} - {tipo}"):
                with st.form(key=f"form_{tipo}_{linea_num}"):
                    st.write("**Acción Estratégica**")
                    accion_estrategica = st.radio("", ["Sí", "No"], key=f"accion_{tipo}_{linea_num}")

                    st.write("**Indicador**")
                    indicador = st.radio("", ["Sí", "No"], key=f"indicador_{tipo}_{linea_num}")

                    st.write("**Meta**")
                    meta = st.radio("", ["Sí", "No"], key=f"meta_{tipo}_{linea_num}")

                    lider = st.text_input("Líder Estratégico", key=f"lider_{tipo}_{linea_num}")
                    cogestores = st.text_area("Cogestores (separados por coma)", key=f"cogestores_{tipo}_{linea_num}")
                    observacion = st.text_area("📝 Observación general", key=f"obs_{tipo}_{linea_num}")

                    submitted = st.form_submit_button("Guardar Evaluación")

                    if submitted:
                        # Definición de estado
                        if meta == "No":
                            estado = "❌ No Cumple"
                        elif meta == "Sí" and (accion_estrategica == "No" or indicador == "No"):
                            estado = "🟡 Pendiente"
                        else:
                            estado = "✅ Completo"

                        # Construcción del diccionario
                        datos = {
                            "delegacion": delegacion,
                            "tipo_linea": tipo,
                            "linea": linea_num,
                            "accion_estrategica": accion_estrategica,
                            "indicador": indicador,
                            "meta": meta,
                            "lider": lider,
                            "cogestores": cogestores,
                            "observacion": observacion,
                            "estado": estado,
                            "fecha": datetime.utcnow().isoformat()
                        }

                        insertar_respuesta(datos)
                        st.success("✅ Evaluación guardada exitosamente")

                        # Reinicio de campos
                        for campo in [f"accion_{tipo}_{linea_num}", f"indicador_{tipo}_{linea_num}", f"meta_{tipo}_{linea_num}",
                                      f"lider_{tipo}_{linea_num}", f"cogestores_{tipo}_{linea_num}", f"obs_{tipo}_{linea_num}"]:
                            if campo in st.session_state:
                                del st.session_state[campo]
# ---------- Visualización de respuestas guardadas ----------

st.markdown("---")
st.subheader("📊 Resumen de Estados por Delegación")

respuestas = obtener_respuestas()

if respuestas:
    df = pd.DataFrame(respuestas)

    # Formateo de fecha
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%d/%m/%Y")

    # Agrupamiento por delegación
    delegaciones_disponibles = df["delegacion"].unique()
    seleccion_delegacion = st.selectbox("Filtrar por delegación", ["Todas"] + list(delegaciones_disponibles))

    if seleccion_delegacion != "Todas":
        df = df[df["delegacion"] == seleccion_delegacion]

    # Mostrar tabla
    st.dataframe(df, use_container_width=True)

    # Opcional: selección para edición
    st.markdown("### ✏️ Editar una respuesta")
    seleccion_id = st.selectbox("Selecciona el ID de la respuesta a editar", df["id"].astype(str), index=0)
    respuesta_seleccionada = df[df["id"].astype(str) == seleccion_id].iloc[0]

    with st.form("editar_formulario"):
        nuevo_estado = st.selectbox("Nuevo estado", ["✅ Completo", "🟡 Pendiente", "❌ No Cumple"],
                                     index=["✅ Completo", "🟡 Pendiente", "❌ No Cumple"].index(respuesta_seleccionada["estado"]))
        nueva_observacion = st.text_area("Nueva observación general", value=respuesta_seleccionada["observacion"])

        if st.form_submit_button("Actualizar"):
            actualizar_respuesta(respuesta_seleccionada["id"], nuevo_estado, nueva_observacion)
            st.success("✅ Respuesta actualizada correctamente")
            st.experimental_rerun()

    # Botón de eliminación
    st.markdown("### 🗑️ Eliminar una respuesta")
    if st.button("Eliminar respuesta seleccionada"):
        eliminar_respuesta(respuesta_seleccionada["id"])
        st.warning("❌ Respuesta eliminada")
        st.experimental_rerun()

    # Botón de descarga
    st.markdown("### 💾 Descargar información")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar Excel (CSV)", csv, "respuestas.csv", "text/csv")
else:
    st.info("No hay respuestas guardadas aún.")
# --------------------------------------------------------
# 📦 Funciones CRUD para Supabase (Insertar, Obtener, Editar, Eliminar)
# --------------------------------------------------------

def insertar_respuesta(data):
    try:
        supabase.table("respuestas").insert(data).execute()
    except Exception as e:
        st.error(f"Error al insertar datos: {e}")

def obtener_respuestas():
    try:
        response = supabase.table("respuestas").select("*").order("fecha", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error al obtener respuestas: {e}")
        return []

def eliminar_respuesta(respuesta_id):
    try:
        supabase.table("respuestas").delete().eq("id", respuesta_id).execute()
    except Exception as e:
        st.error(f"Error al eliminar la respuesta: {e}")

def actualizar_respuesta(respuesta_id, nuevo_estado, nueva_observacion):
    try:
        supabase.table("respuestas").update({
            "estado": nuevo_estado,
            "observacion": nueva_observacion,
            "fecha": datetime.utcnow().isoformat()
        }).eq("id", respuesta_id).execute()
    except Exception as e:
        st.error(f"Error al actualizar la respuesta: {e}")




