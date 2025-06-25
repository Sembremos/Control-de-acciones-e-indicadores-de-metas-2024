import streamlit as st
import pandas as pd

# Configuración de la app
st.set_page_config(page_title="Seguimiento Delegaciones", layout="wide")

# Lista completa de delegaciones en formato DXX - Nombre
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

st.title("📋 Seguimiento de Líneas de Acción por Delegación")

# Buscador de delegaciones
delegacion = st.selectbox("Selecciona una delegación", delegaciones)

if delegacion:
    tipo_linea = st.radio("Tipo de línea de acción", ["Fuerza Pública", "Gobierno Local"])

    with st.form("form_linea_accion"):
        st.subheader("📝 Información de la Línea de Acción")

        linea_num = st.number_input("Número de línea de acción (1-10)", min_value=1, max_value=10, step=1)

        accion_estrategica = st.text_input("Acción Estratégica")
        ejemplo_ae = st.text_area("¿Hubo un ejemplo para la Acción Estratégica?", placeholder="Describa el ejemplo si aplica")

        indicador = st.text_input("Indicador")
        ejemplo_ind = st.text_area("¿Hubo un ejemplo para el Indicador?", placeholder="Describa el ejemplo si aplica")

        meta = st.text_input("Meta")
        ejemplo_meta = st.text_area("¿Hubo un ejemplo para la Meta?", placeholder="Describa el ejemplo si aplica")

        lider = st.text_input("Líder Estratégico")
        cogestores = st.text_area("Cogestores", placeholder="Ingrese los nombres separados por coma")

        submitted = st.form_submit_button("Guardar Evaluación")

        if submitted:
            estado = "terminado"

            # Validación de la meta
            meta_invalida = meta.strip().lower() in ["", "no aplica", "mal", "falta", "n/a"]
            if meta_invalida:
                estado = "pendiente"

            resultado = {
                "Delegación": delegacion,
                "Tipo de Línea": tipo_linea,
                "Línea de Acción": linea_num,
                "Acción Estratégica": accion_estrategica,
                "Ejemplo AE": ejemplo_ae,
                "Indicador": indicador,
                "Ejemplo Indicador": ejemplo_ind,
                "Meta": meta,
                "Ejemplo Meta": ejemplo_meta,
                "Líder Estratégico": lider,
                "Cogestores": cogestores,
                "Estado": estado
            }

            st.success(f"✅ Evaluación guardada como '{estado.upper()}' para {delegacion}")
            st.json(resultado)

            # Aquí se podrá conectar con Google Sheets o guardar respaldo en Excel más adelante
