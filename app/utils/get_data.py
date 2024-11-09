import sys
from pathlib import Path
import streamlit as st
import pandas as pd


DIR_ROOT = str(Path(__file__).parents[1])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)


@st.cache_data(show_spinner=False)
def get_data():
    df = pd.read_excel(Path(DIR_ROOT, "data/output/BASE_FINAL.xlsx"))
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
