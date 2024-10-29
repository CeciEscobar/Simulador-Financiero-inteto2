import streamlit as st
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Configuración del layout
st.set_page_config(layout="wide")

# Personalización de colores
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff;  /* Color de fondo azul claro */
    }
    h1 {
        color: #4a90e2;  /* Color del título principal */
    }
    h2 {
        color: #d9534f;  /* Color de subtítulos */
    }
    .stNumberInput, .stSelectbox {
        background-color: #e6f7ff; /* Fondo de los widgets */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Lista de ETFs
ETFs_Data = [
    {"nombre": "AZ QQQ NASDAQ 100", "descripcion": "ETF que sigue el rendimiento del índice NASDAQ 100.", "simbolo": "QQQ"},
    {"nombre": "AZ SPDR S&P 500 ETF TRUST", "descripcion": "ETF que sigue el rendimiento del índice S&P 500.", "simbolo": "SPY"},
    {"nombre": "AZ SPDR DJIA TRUST", "descripcion": "ETF que sigue el rendimiento del índice Dow Jones.", "simbolo": "DIA"},
    {"nombre": "AZ VANGUARD EMERGING MARKET ETF", "descripcion": "ETF que sigue el rendimiento de mercados emergentes.", "simbolo": "VWO"},
    {"nombre": "AZ FINANCIAL SELECT SECTOR SPDR", "descripcion": "ETF que sigue el rendimiento del sector financiero.", "simbolo": "XLF"},
    {"nombre": "AZ HEALTH CARE SELECT SECTOR", "descripcion": "ETF que sigue el rendimiento del sector salud.", "simbolo": "XLV"},
    {"nombre": "AZ DJ US HOME CONSTRUCT", "descripcion": "ETF que sigue el rendimiento del sector de construcción de viviendas.", "simbolo": "ITB"},
    {"nombre": "AZ SILVER TRUST", "descripcion": "ETF que sigue el precio de la plata.", "simbolo": "SLV"},
    {"nombre": "AZ MSCI TAIWAN INDEX FD", "descripcion": "ETF que sigue el rendimiento del índice MSCI Taiwan.", "simbolo": "EWT"},
    {"nombre": "AZ MSCI UNITED KINGDOM", "descripcion": "ETF que sigue el rendimiento del índice MSCI UK.", "simbolo": "EWU"},
    {"nombre": "AZ MSCI SOUTH KOREA IND", "descripcion": "ETF que sigue el rendimiento del índice MSCI South Korea.", "simbolo": "EWY"},
    {"nombre": "AZ MSCI EMU", "descripcion": "ETF que sigue el rendimiento del índice MSCI EMU.", "simbolo": "EZU"},
    {"nombre": "AZ MSCI JAPAN INDEX FD", "descripcion": "ETF que sigue el rendimiento del índice MSCI Japan.", "simbolo": "EWJ"},
    {"nombre": "AZ MSCI CANADA", "descripcion": "ETF que sigue el rendimiento del índice MSCI Canada.", "simbolo": "EWC"},
    {"nombre": "AZ MSCI GERMANY INDEX", "descripcion": "ETF que sigue el rendimiento del índice MSCI Germany.", "simbolo": "EWG"},
    {"nombre": "AZ MSCI AUSTRALIA INDEX", "descripcion": "ETF que sigue el rendimiento del índice MSCI Australia.", "simbolo": "EWA"},
    {"nombre": "AZ BARCLAYS AGGREGATE", "descripcion": "ETF que sigue el rendimiento del índice de bonos Barclays.", "simbolo": "AGG"}
]

# Título de la aplicación
st.title("Análisis de ETFs")
st.write("Análisis de los ETFs mas relevantes de Allianz Patrimonial")


# Selector de ETFs
etfs_seleccionados = st.multiselect(
    "Selecciona uno o más ETFs para ver los detalles:",
    options=[etf['nombre'] for etf in ETFs_Data],
    default=[]
)

# Verificar si hay ETFs seleccionados
if etfs_seleccionados:
    st.write("### Detalles de los ETFs Seleccionados:")
    
    # Asegúrate de que siempre se pase al menos 1 como valor
    num_cols = max(1, len(etfs_seleccionados))  # Asegúrate de que sea al menos 1
    cols = st.columns(num_cols)  # Crear columnas dinámicamente

    for idx, etf_name in enumerate(etfs_seleccionados):
        etf_info = next((etf for etf in ETFs_Data if etf['nombre'] == etf_name), None)
        if etf_info:
            simbolo = etf_info["simbolo"]
            
            with cols[idx % len(cols)]:
                st.subheader(etf_info['nombre'])
                st.write(f"**Descripción**: {etf_info['descripcion']}")
                st.write(f"**Símbolo**: {simbolo}")
                
                # Obtener información de Yahoo Finance
                ticker = yf.Ticker(simbolo)
                info = ticker.info

                # Mostrar datos financieros clave
                st.write("#### Datos Financieros Clave")
                st.markdown(f"""
                - **Precio de Cierre**: {info.get('previousClose')} USD
                - **Precio de Apertura**: {info.get('open')} USD
                - **Rango Diario**: {info.get('dayLow')} - {info.get('dayHigh')} USD
                - **Rango 52 Semanas**: {info.get('fiftyTwoWeekLow')} - {info.get('fiftyTwoWeekHigh')} USD
                - **Volumen**: {info.get('volume')}
                - **Volumen Promedio**: {info.get('averageVolume')}
                - **Activos Netos**: {info.get('totalAssets')}
                - **Retorno Total YTD**: {info.get('ytdReturn'):.2%}
                """)
                
                st.markdown("---")
                
                # Descargar datos históricos de los últimos 10 años
                historical_data = ticker.history(period="10y")
                
                # Calcular rendimiento anualizado, riesgo y ratio rendimiento-riesgo
                rendimiento_anualizado = (historical_data['Close'][-1] / historical_data['Close'][0]) ** (1 / 10) - 1
                riesgo = np.std(historical_data['Close'].pct_change()) * np.sqrt(252)  # Desviación estándar anualizada
                ratio_rendimiento_riesgo = rendimiento_anualizado / riesgo if riesgo != 0 else np.nan
                
                # Sección de rendimiento y riesgo
                st.subheader("Rendimiento y Riesgo")
                st.markdown(f"""
                - **Rendimiento Anualizado**: {rendimiento_anualizado:.2%}
                - **Riesgo (Desviación Estándar Anualizada)**: {riesgo:.2%}
                - **Ratio Rendimiento-Riesgo**: {ratio_rendimiento_riesgo:.2f}
                """)
                
                # Título para el gráfico
                st.subheader("Desempeño Histórico de Precios ETF")
                
                # Graficar precios de cierre
                plt.figure(figsize=(8, 4))  # Tamaño de la gráfica ajustado
                plt.plot(historical_data.index, historical_data['Close'], label='Precio de Cierre', color='#4a90e2')
                plt.title(f'Precios Históricos de {etf_info["nombre"]} ({simbolo}) - Últimos 10 Años')
                plt.xlabel('Fecha')
                plt.ylabel('Precio (USD)')
                plt.legend()
                plt.grid()
                
                # Mostrar gráfico
                st.pyplot(plt)
                plt.clf()  # Limpiar la figura para evitar superposición de gráficos

# Apartado de Cálculo Financiero
st.write("---")
st.subheader("Cálculo Financiero")
st.write("Cálculo Financiero para conocer el rendimiento, riesgo y otros indicadores de el/los ETFs seleccionados.")

# Selector de período de tiempo
period_options = ["1mo", "3mo", "6mo", "1y", "YTD", "3y", "5y", "10y", "Especifico"]
selected_period = st.selectbox("Selecciona un período de tiempo:", period_options)

# Variables para las fechas específicas
start_date = None
end_date = None

# Si se selecciona "Especifico", se muestran los selectores de fecha
if selected_period == "Especifico":
    start_date = st.date_input("Fecha de inicio:", value=datetime.today())
    end_date = st.date_input("Fecha de fin:", value=datetime.today())
    
# Caja para ingresar la cantidad invertida
cantidad_invertida = st.number_input("Cantidad invertida (USD):", min_value=0.0, step=100.0)

if cantidad_invertida > 0:
    rendimientos = []
    valores_finales = []
    riesgos = []
    etiquetas = []
    tiempos_recuperacion = []  # Lista para almacenar el tiempo de recuperación

    # Crear columnas para mostrar resultados
    cols = st.columns(len(etfs_seleccionados))

    for idx, etf_name in enumerate(etfs_seleccionados):
        etf_info = next((etf for etf in ETFs_Data if etf['nombre'] == etf_name), None)
        if etf_info:
            simbolo = etf_info["simbolo"]
            ticker = yf.Ticker(simbolo)

            # Descargar datos históricos según el período seleccionado
            if selected_period == "Especifico":
                historical_data_selected = ticker.history(start=start_date, end=end_date)
            else:
                historical_data_selected = ticker.history(period=selected_period)

            # Verificar si hay datos disponibles
            if not historical_data_selected.empty:
                # Calcular rendimiento, riesgo y ratio rendimiento-riesgo
                rendimiento = (historical_data_selected['Close'][-1] / historical_data_selected['Close'][0]) - 1
                riesgo_periodo = np.std(historical_data_selected['Close'].pct_change()) * np.sqrt(252)  # Desviación estándar anualizada
                ratio_rendimiento_riesgo_periodo = rendimiento / riesgo_periodo if riesgo_periodo != 0 else np.nan

                # Calcular valor final de la inversión
                valor_final = cantidad_invertida * (1 + rendimiento)

                # Calcular el tiempo para recuperar la inversión
                tiempo_recuperacion = 1 / rendimiento if rendimiento > 0 else np.inf  # Tiempo aproximado en años

                # Agregar datos a listas para los gráficos
                rendimientos.append(rendimiento)
                valores_finales.append(valor_final)
                riesgos.append(riesgo_periodo)
                tiempos_recuperacion.append(tiempo_recuperacion)  # Agregar tiempo a la lista
                etiquetas.append(f"{etf_info['nombre']} ({simbolo})")

                # Mostrar resultados en columnas
                with cols[idx]:
                    st.markdown(f"### {etf_info['nombre']} ({simbolo})")
                    st.markdown(f"""
                    - **Rendimiento**: {rendimiento:.2%}
                    - **Riesgo**: {riesgo_periodo:.2%}
                    - **Ratio Rendimiento-Riesgo**: {ratio_rendimiento_riesgo_periodo:.2f}
                    - **Valor Final**: ${valor_final:.2f}
                    - **Tiempo para Recuperar Inversión (años)**: {tiempo_recuperacion:.2f}
                    """)
            else:
                with cols[idx]:
                    st.warning(f"No hay datos disponibles para el período seleccionado para {etf_info['nombre']} ({simbolo}).")

    # Crear columnas para gráficos
    st.write("---")
    st.subheader("Gráficos de Riesgo y Valor Final")
    graph_cols = st.columns(2)

    # Gráfico de Riesgo
    with graph_cols[0]:
        plt.figure(figsize=(4, 4))  # Tamaño ajustado
        plt.bar(etiquetas, riesgos, color='#ffcc00')
        plt.title('Riesgo de ETFs', fontsize=10)
        plt.xlabel('ETFs')
        plt.ylabel('Riesgo (Desviación Estándar)')
        plt.axhline(0, color='red', linewidth=0.8, linestyle='--')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        st.pyplot(plt)
        plt.clf()

    # Gráfico de Valor Final
    with graph_cols[1]:
        plt.figure(figsize=(4, 4))  # Tamaño ajustado
        plt.bar(etiquetas, valores_finales, color='#5cb85c')
        plt.title('Valor Final de la Inversión en ETFs', fontsize=10)
        plt.xlabel('ETFs')
        plt.ylabel('Valor Final (USD)')
        plt.axhline(cantidad_invertida, color='red', linewidth=0.8, linestyle='--', label='Cantidad Invertida')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(axis='y')
        st.pyplot(plt)
        plt.clf()

    # Leyenda Comparativa
    st.write("---")
    st.subheader("Comparativa de Rendimientos y Valores Finales")
    comparativa_df = pd.DataFrame({
        "ETF": etiquetas,
        "Rendimiento (%)": [r * 100 for r in rendimientos],
        "Valor Final (USD)": valores_finales,
        "Tiempo para Recuperar Inversión (años)": tiempos_recuperacion
    })

    st.table(comparativa_df)
