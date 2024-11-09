import streamlit as st
import pandas as pd


@st.cache_data(show_spinner=False)
def get_data():
    df = pd.read_excel("data/output/BASE_FINAL.xlsx")
    df.columns = [
        "Marca",
        "Modelo",
        "Produto",
        "Classificação Energética",
        "Tipo de Gás",
        "Consumo de Energia Mensal (kWh)",
        "Consumo de Água Mensal (L)",
        "Fluído Refrigerante",
    ]
    return df, pd.DataFrame(columns=list(df.columns))
