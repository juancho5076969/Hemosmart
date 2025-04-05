
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configurar la conexión con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Subir tu archivo JSON de credenciales como secrets.json en Streamlit Cloud
credentials = ServiceAccountCredentials.from_json_keyfile_name('secrets.json', scope)
client = gspread.authorize(credentials)
sheet = client.open("registro_hemodialisis").sheet1

# Interfaz de usuario
st.title("Calculadora de Hemodiálisis")
st.write("Por favor ingrese los datos del paciente:")

nombre = st.text_input("Nombre del paciente")
edad = st.number_input("Edad del paciente", min_value=0, max_value=120)
peso_seco = st.number_input("Peso seco (kg)", min_value=0.0, format="%.2f")
peso_actual = st.number_input("Peso actual (kg)", min_value=0.0, format="%.2f")

# Tasa de ultrafiltración fija (10 mL/kg/h)
uf_rate = 10.0

if st.button("Calcular y Guardar"):
    if peso_actual > peso_seco:
        uf = peso_actual - peso_seco
        tasa_uf_lh = (uf_rate * peso_seco) / 1000
        tiempo = round(uf / tasa_uf_lh, 2)

        st.success(f"Volumen a extraer: {uf:.2f} L")
        st.success(f"Tasa UF: {tasa_uf_lh:.2f} L/h")
        st.success(f"Tiempo estimado de hemodiálisis: {tiempo} horas")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fila = [fecha, nombre, edad, peso_seco, peso_actual, uf_rate, uf, tasa_uf_lh, tiempo]
        sheet.append_row(fila)
        st.info("Datos guardados en Google Sheets exitosamente.")
    else:
        st.warning("El peso actual debe ser mayor al peso seco para calcular.")
