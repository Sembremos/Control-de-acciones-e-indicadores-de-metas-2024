import streamlit as st
import pandas as pd

# ---------------------------------------------
# 📌 PARTE 1: Configuración inicial y delegaciones
# ---------------------------------------------
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

if "resultados" not in st.session_state:
    st.session_state["resultados"] = []

# ---------------------------------------------
# 📌 PARTE 2: Formulario de evaluación por línea
# ---------------------------------------------
delegacion = st.selectbox("Selecciona una delegación", delegaciones)

if delegacion:
    st.subheader("Tipo de línea de acción")
    tipo_lineas = st.multiselect("Puede seleccionar uno o ambos tipos", ["Fuerza Pública", "Gobierno Local"])

    for tipo in tipo_lineas:
        st.markdown(f"---\n### 🛡️ Registro para: {tipo}")
        lineas = st.multiselect(f"Números de línea de acción para {tipo} (1-10)", list(range(1, 11)), key=f"lineas_{tipo}")

        for linea_num in lineas:
            with st.expander(f"📄 Línea de Acción #{linea_num} - {tipo}"):
                with st.form(key=f"form_{tipo}_{linea_num}"):
                    accion_estrategica = st.radio("", ["Sí", "No"], key=f"val_ae_{tipo}_{linea_num}")
                    indicador = st.radio("", ["Sí", "No"], key=f"val_ind_{tipo}_{linea_num}")
                    meta = st.radio("", ["Sí", "No"], key=f"val_meta_{tipo}_{linea_num}")
                    lider = st.text_input("Líder Estratégico", key=f"lider_{tipo}_{linea_num}")
                    cogestores = st.text_area("Cogestores (separados por coma)", key=f"cog_{tipo}_{linea_num}")
                    observacion = st.text_area("📝 Observación general", key=f"obs_{tipo}_{linea_num}")

                    submitted = st.form_submit_button("Guardar Evaluación")
                    if submitted:
                        ae_ok = accion_estrategica == "Sí"
                        ind_ok = indicador == "Sí"
                        meta_ok = meta == "Sí"

                        if not meta_ok:
                            estado = "❌ Rechazado"
                        elif not ae_ok or not ind_ok:
                            estado = "🕓 Pendiente"
                        else:
                            estado = "✅ Completo"

                        resultado = {
                            "Delegación": delegacion,
                            "Tipo de Línea": tipo,
                            "Línea": linea_num,
                            "Líder": lider,
                            "Cogestores": cogestores,
                            "Observación": observacion,
                            "Estado": estado
                        }
                        st.session_state["resultados"].append(resultado)
                        st.success(f"Evaluación guardada para Línea #{linea_num} - {tipo}")

# ---------------------------------------------
# 📌 PARTE 3: Resumen y exportación
# ---------------------------------------------
if st.session_state["resultados"]:
    st.markdown("---")
    st.subheader("📊 Resumen de Estados por Delegación")

    df_resultados = pd.DataFrame(st.session_state["resultados"])

    for estado in sorted(df_resultados["Estado"].unique()):
        with st.expander(f"{estado} - Ver detalles"):
            st.dataframe(df_resultados[df_resultados["Estado"] == estado], use_container_width=True)

    st.download_button(
        label="📥 Descargar resumen en Excel",
        data=df_resultados.to_excel(index=False, engine='openpyxl'),
        file_name="resumen_evaluacion.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )



            
