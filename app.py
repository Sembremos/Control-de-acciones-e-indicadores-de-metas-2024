import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# ---------------------------------------------
# 📌 PARTE 1: Configuración inicial y Supabase
# ---------------------------------------------

# Conexión a Supabase
SUPABASE_URL = "https://zutgkfioubpepebjraid.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1dGdrZmlvdWJwZXBlYmpyYWlkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwNTA4MDksImV4cCI6MjA2NjYyNjgwOX0.dUzaSY2YC9Jp1oQEClKTDvaRZMNEzmwd486XY-ibPS8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inicializar la app
st.set_page_config(page_title="Seguimiento Delegaciones", layout="wide")
st.title("📋 Seguimiento de Líneas de Acción por Delegación")

# Lista de delegaciones
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
# ---------------------------------------------
# 📌 PARTE 2: Formulario de Evaluación y Guardado en Supabase
# ---------------------------------------------

delegacion = st.selectbox("Selecciona una delegación", delegaciones)

if delegacion:
    st.subheader("Tipo de línea de acción")
    tipo_lineas = st.multiselect("Puede seleccionar uno o ambos tipos", ["Fuerza Pública", "Gobierno Local"])

    for tipo in tipo_lineas:
        st.markdown(f"---\n### 🛡️ Registro para: {tipo}")
        lineas = st.multiselect(
            f"Números de línea de acción para {tipo} (1-10)",
            list(range(1, 11)),
            key=f"lineas_{tipo}"
        )

        for linea_num in lineas:
            with st.expander(f"📄 Línea de Acción #{linea_num} - {tipo}"):
                with st.form(key=f"form_{tipo}_{linea_num}"):

                    st.markdown("**Acción Estratégica**")
                    accion_estrategica = st.radio("", ["Sí", "No"], key=f"val_ae_{tipo}_{linea_num}")

                    st.markdown("**Indicador**")
                    indicador = st.radio("", ["Sí", "No"], key=f"val_ind_{tipo}_{linea_num}")

                    st.markdown("**Meta**")
                    meta = st.radio("", ["Sí", "No"], key=f"val_meta_{tipo}_{linea_num}")

                    st.markdown("**Líder Estratégico**")
                    lider = st.radio("", ["Sí", "No"], key=f"val_lider_{tipo}_{linea_num}")

                    st.markdown("**Cogestores**")
                    cogestores = st.radio("", ["Sí", "No"], key=f"val_cog_{tipo}_{linea_num}")

                    observacion = st.text_area("📝 Observación general", key=f"obs_{tipo}_{linea_num}")

                    submitted = st.form_submit_button("Guardar Evaluación")

                    if submitted:
                        ae_ok = accion_estrategica == "Sí"
                        ind_ok = indicador == "Sí"
                        meta_ok = meta == "Sí"
                        lider_ok = lider == "Sí"
                        cog_ok = cogestores == "Sí"

                        if not meta_ok:
                            estado = "❌ Rechazado"
                        elif not (ae_ok and ind_ok and lider_ok and cog_ok):
                            estado = "🕓 Pendiente"
                        else:
                            estado = "✅ Completo"

                        # Guardar en Supabase
                        data = {
                            "delegacion": delegacion,
                            "tipo_linea": tipo,
                            "linea_num": linea_num,
                            "accion_estrategica": accion_estrategica,
                            "indicador": indicador,
                            "meta": meta,
                            "lider": lider,
                            "cogestores": cogestores,
                            "observacion": observacion,
                            "estado": estado
                        }

                        supabase.table("evaluaciones").insert(data).execute()
                        st.success(f"✅ Evaluación guardada para Línea #{linea_num} - {tipo}")

                        st.experimental_rerun()  # Reiniciar el formulario automáticamente
# ---------------------------------------------
# 📌 PARTE 3: Ver, editar, eliminar y exportar datos
# ---------------------------------------------

st.markdown("---")
st.subheader("📊 Evaluaciones Guardadas")

# Obtener todos los datos desde Supabase
respuesta = supabase.table("evaluaciones").select("*").order("fecha_registro", desc=True).execute()
registros = respuesta.data

if registros:
    df = pd.DataFrame(registros)

    delegaciones_disponibles = df["delegacion"].unique().tolist()
    delegacion_filtro = st.selectbox("Filtrar por delegación", ["Todas"] + delegaciones_disponibles)

    if delegacion_filtro != "Todas":
        df = df[df["delegacion"] == delegacion_filtro]

    for estado in ["✅ Completo", "🕓 Pendiente", "❌ Rechazado"]:
        df_estado = df[df["estado"] == estado]

        if not df_estado.empty:
            with st.expander(f"{estado} - {len(df_estado)} registro(s)", expanded=False):
                for _, row in df_estado.iterrows():
                    col1, col2, col3 = st.columns([5, 2, 2])
                    with col1:
                        st.markdown(f"**Delegación:** {row['delegacion']}  \n"
                                    f"**Tipo:** {row['tipo_linea']}  \n"
                                    f"**Línea:** {row['linea_num']}  \n"
                                    f"**Estado:** {row['estado']}")
                    with col2:
                        if st.button("✏️ Editar", key=f"edit_{row['id']}"):
                            st.warning("🔧 Funcionalidad de edición será implementada aquí.")
                    with col3:
                        if st.button("🗑️ Eliminar", key=f"delete_{row['id']}"):
                            supabase.table("evaluaciones").delete().eq("id", row["id"]).execute()
                            st.success("Registro eliminado correctamente.")
                            st.experimental_rerun()

    # Descarga a Excel
    st.markdown("---")
    st.subheader("📥 Exportar a Excel")
    df_export = pd.DataFrame(registros)
    df_export = df_export.drop(columns=["id"])
    st.download_button("📁 Descargar todas las evaluaciones", data=df_export.to_csv(index=False).encode("utf-8"),
                       file_name="evaluaciones.csv", mime="text/csv")
else:
    st.info("No hay evaluaciones registradas aún.")
# ---------------------------------------------
# 🛠️ Edición de registros seleccionados
# ---------------------------------------------
if "editar_id" not in st.session_state:
    st.session_state.editar_id = None

# Al hacer clic en "Editar", se guarda el ID
for row in registros:
    if st.session_state.get(f"edit_{row['id']}", False):
        st.session_state.editar_id = row["id"]

# Mostrar formulario si hay un registro en modo edición
if st.session_state.editar_id:
    editar_data = next((r for r in registros if r["id"] == st.session_state.editar_id), None)

    if editar_data:
        st.markdown("---")
        st.subheader(f"✏️ Editar Evaluación: {editar_data['delegacion']} - Línea #{editar_data['linea_num']}")

        with st.form("editar_form"):
            accion_estrategica = st.radio("Acción Estratégica", ["Sí", "No"], index=0 if editar_data["accion_estrategica"] == "Sí" else 1)
            indicador = st.radio("Indicador", ["Sí", "No"], index=0 if editar_data["indicador"] == "Sí" else 1)
            meta = st.radio("Meta", ["Sí", "No"], index=0 if editar_data["meta"] == "Sí" else 1)
            lider = st.radio("Líder Estratégico", ["Sí", "No"], index=0 if editar_data["lider"] == "Sí" else 1)
            cogestores = st.radio("Cogestores", ["Sí", "No"], index=0 if editar_data["cogestores"] == "Sí" else 1)
            observacion = st.text_area("📝 Observación general", value=editar_data["observacion"] or "")

            guardar_cambios = st.form_submit_button("💾 Guardar cambios")

            if guardar_cambios:
                # Recalcular estado
                ae_ok = accion_estrategica == "Sí"
                ind_ok = indicador == "Sí"
                meta_ok = meta == "Sí"
                lider_ok = lider == "Sí"
                cog_ok = cogestores == "Sí"

                if not meta_ok:
                    estado = "❌ Rechazado"
                elif not (ae_ok and ind_ok and lider_ok and cog_ok):
                    estado = "🕓 Pendiente"
                else:
                    estado = "✅ Completo"

                # Actualizar en Supabase
                supabase.table("evaluaciones").update({
                    "accion_estrategica": accion_estrategica,
                    "indicador": indicador,
                    "meta": meta,
                    "lider": lider,
                    "cogestores": cogestores,
                    "observacion": observacion,
                    "estado": estado
                }).eq("id", editar_data["id"]).execute()

                st.success("✅ Cambios guardados correctamente.")
                st.session_state.editar_id = None
                st.experimental_rerun()
