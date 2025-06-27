import streamlit as st
import pandas as pd

# ---------------------------------------------
# 📌 PARTE 1: Configuración inicial y delegaciones
# ---------------------------------------------

# Configura la interfaz de Streamlit
st.set_page_config(page_title="Seguimiento Delegaciones", layout="wide")
st.title("📋 Seguimiento de Líneas de Acción por Delegación")

# Lista completa y ordenada de delegaciones oficiales
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

# Inicializa la lista de resultados si no existe
if "resultados" not in st.session_state:
    st.session_state["resultados"] = []

# Selección de delegación activa
delegacion = st.selectbox("Selecciona una delegación", delegaciones)
# ---------------------------------------------
# 📌 PARTE 2: Selección de tipo de línea y formulario de evaluación
# ---------------------------------------------

if delegacion:
    st.subheader("Tipo de línea de acción")
    tipo_lineas = st.multiselect(
        "Puede seleccionar uno o ambos tipos",
        ["Fuerza Pública", "Gobierno Local"]
    )

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

                    # -------------------
                    # Campos de evaluación SÍ/NO
                    # -------------------
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

                    # -------------------
                    # Observación final general
                    # -------------------
                    observacion = st.text_area("📝 Observación general", key=f"obs_{tipo}_{linea_num}")

                    submitted = st.form_submit_button("Guardar Evaluación")

                    if submitted:
                        # Evaluar estado final
                        ae_ok = accion_estrategica == "Sí"
                        ind_ok = indicador == "Sí"
                        meta_ok = meta == "Sí"
                        lider_ok = lider == "Sí"
                        cog_ok = cogestores == "Sí"

                        if not meta_ok:
                            estado = "❌ Rechazado"
                        elif meta_ok and (not ae_ok or not ind_ok or not lider_ok or not cog_ok):
                            estado = "🕓 Pendiente"
                        else:
                            estado = "✅ Completo"

                        resultado = {
                            "Delegación": delegacion,
                            "Tipo de Línea": tipo,
                            "Línea": linea_num,
                            "Acción Estratégica": accion_estrategica,
                            "Indicador": indicador,
                            "Meta": meta,
                            "Líder Estratégico": lider,
                            "Cogestores": cogestores,
                            "Observación": observacion,
                            "Estado": estado
                        }

                        st.session_state["resultados"].append(resultado)
                        st.success(f"✅ Evaluación guardada para Línea #{linea_num} - {tipo}")
# ---------------------------------------------
# 📌 PARTE 3: Mostrar resumen agrupado por estado
# ---------------------------------------------

if st.session_state["resultados"]:
    st.markdown("---")
    st.subheader("📊 Resumen de Evaluaciones por Estado")

    df_resultados = pd.DataFrame(st.session_state["resultados"])

    # Agrupar por estado
    for estado in ["✅ Completo", "🕓 Pendiente", "❌ Rechazado"]:
        df_estado = df_resultados[df_resultados["Estado"] == estado]

        if not df_estado.empty:
            with st.expander(f"{estado} - {len(df_estado)} registro(s)", expanded=False):
                st.dataframe(df_estado.reset_index(drop=True), use_container_width=True)
