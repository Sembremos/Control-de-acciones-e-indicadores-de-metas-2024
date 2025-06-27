# -----------------------------------------------------------
# app.py — Seguimiento de Indicadores y Metas por Delegación
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# -------------------------------
# 🔌 Conexión a Supabase
# -------------------------------
SUPABASE_URL = "https://zutgkfioubpepebjraid.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1dGdrZmlvdWJwZXBlYmpyYWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwNTA4MDksImV4cCI6MjA2NjYyNjgwOX0.dUzaSY2YC9Jp1oQEClKTDvaRZMNEzmwd486XY-ibPS8"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------
# ⚙️ Configuración general
# -------------------------------
st.set_page_config(page_title="Control de Indicadores", layout="wide")
st.title("📋 Seguimiento de Líneas de Acción por Delegación")

# -------------------------------
# 🗂️ Lista de delegaciones válidas
# -------------------------------
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
# ---------------------------------------
# 📝 Registro de Evaluación
# ---------------------------------------

delegacion = st.selectbox("Selecciona una delegación", delegaciones)

if delegacion:
    tipo_lineas = st.multiselect(
        "Selecciona el tipo de línea de acción",
        ["Fuerza Pública", "Gobierno Local"]
    )

    for tipo in tipo_lineas:
        st.markdown(f"---\n### 🛡️ Evaluación para: {tipo}")

        lineas = st.multiselect(
            f"Líneas de acción del {tipo} (1-10)",
            list(range(1, 11)),
            key=f"lineas_{tipo}"
        )

        for linea_num in lineas:
            with st.expander(f"📄 Línea de Acción #{linea_num} - {tipo}"):
                with st.form(key=f"form_{tipo}_{linea_num}"):
                    st.write("**¿Cumple con la Acción Estratégica?**")
                    accion_estrategica = st.radio("", ["Sí", "No"], key=f"accion_{tipo}_{linea_num}")

                    st.write("**¿Cumple con el Indicador?**")
                    indicador = st.radio("", ["Sí", "No"], key=f"indicador_{tipo}_{linea_num}")

                    st.write("**¿Cumple con la Meta?**")
                    meta = st.radio("", ["Sí", "No"], key=f"meta_{tipo}_{linea_num}")

                    lider = st.text_input("Líder Estratégico", key=f"lider_{tipo}_{linea_num}")
                    cogestores = st.text_area("Cogestores (separados por coma)", key=f"cog_{tipo}_{linea_num}")
                    observacion = st.text_area("📝 Observación general", key=f"obs_{tipo}_{linea_num}")

                    guardar = st.form_submit_button("Guardar Evaluación")

                    if guardar:
                        # Determinar estado final
                        if meta == "No":
                            estado = "❌ No Cumple"
                        elif meta == "Sí" and (accion_estrategica == "No" or indicador == "No"):
                            estado = "🟡 Pendiente"
                        else:
                            estado = "✅ Completo"

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
                        st.success("✅ Evaluación guardada correctamente")

                        # Reinicio de campos tras guardar
                        for campo in [
                            f"accion_{tipo}_{linea_num}", f"indicador_{tipo}_{linea_num}", f"meta_{tipo}_{linea_num}",
                            f"lider_{tipo}_{linea_num}", f"cog_{tipo}_{linea_num}", f"obs_{tipo}_{linea_num}"
                        ]:
                            if campo in st.session_state:
                                del st.session_state[campo]
# ---------------------------------------
# 📊 Resumen de Evaluaciones Guardadas
# ---------------------------------------

st.markdown("---")
st.subheader("📁 Historial de Evaluaciones")

# Obtener datos desde Supabase
respuestas = obtener_respuestas()

if respuestas:
    df = pd.DataFrame(respuestas)

    # Formatear fecha a dd/mm/yyyy
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%d/%m/%Y")

    # Filtro por delegación
    delegaciones_filtradas = df["delegacion"].unique()
    seleccion = st.selectbox("Filtrar por delegación", ["Todas"] + sorted(delegaciones_filtradas))

    if seleccion != "Todas":
        df = df[df["delegacion"] == seleccion]

    # Mostrar tabla
    st.dataframe(df, use_container_width=True)

    # Selección para edición
    st.markdown("### ✏️ Editar Evaluación")
    id_editar = st.selectbox("Selecciona el ID a editar", df["id"].astype(str), index=0)
    registro = df[df["id"].astype(str) == id_editar].iloc[0]

    with st.form("editar_formulario"):
        nuevo_estado = st.selectbox("Nuevo estado", ["✅ Completo", "🟡 Pendiente", "❌ No Cumple"],
                                    index=["✅ Completo", "🟡 Pendiente", "❌ No Cumple"].index(registro["estado"]))
        nueva_obs = st.text_area("Nueva observación general", value=registro["observacion"])

        if st.form_submit_button("Actualizar Evaluación"):
            actualizar_respuesta(registro["id"], nuevo_estado, nueva_obs)
            st.success("✅ Evaluación actualizada")
            st.experimental_rerun()

    # Botón de eliminación
    st.markdown("### 🗑️ Eliminar Evaluación")
    if st.button("Eliminar evaluación seleccionada"):
        eliminar_respuesta(registro["id"])
        st.warning("⚠️ Evaluación eliminada correctamente")
        st.experimental_rerun()

    # Botón de descarga
    st.markdown("### 💾 Descargar Excel")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Descargar archivo CSV", csv, "evaluaciones.csv", "text/csv")
else:
    st.info("Aún no se han registrado evaluaciones.")
# ---------------------------------------
# 🛠️ Funciones CRUD con Supabase
# ---------------------------------------

def insertar_respuesta(data: dict):
    """Insertar nueva evaluación en la tabla 'respuestas'."""
    supabase.table("respuestas").insert(data).execute()

def obtener_respuestas():
    """Obtener todas las evaluaciones guardadas."""
    response = supabase.table("respuestas").select("*").order("fecha", desc=True).execute()
    return response.data if response.data else []

def eliminar_respuesta(respuesta_id: int):
    """Eliminar evaluación por ID."""
    supabase.table("respuestas").delete().eq("id", respuesta_id).execute()

def actualizar_respuesta(respuesta_id: int, estado: str, observacion: str):
    """Actualizar el estado y observación de una evaluación."""
    supabase.table("respuestas").update({
        "estado": estado,
        "observacion": observacion,
        "fecha": datetime.utcnow().isoformat()
    }).eq("id", respuesta_id).execute()





