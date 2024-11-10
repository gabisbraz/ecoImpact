import streamlit as st
import time
import sys
from pathlib import Path

DIR_ROOT = str(Path(__file__).parents[0])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from app_pages.home import home_page
from app_pages.sobre_nos import sobre_nos_page
from app_pages.eletrodomesticos import eletrodomesticos_page
from utils.navbar import navbar_page
from app_pages.analise import analise_page
from utils.get_data import get_data


st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

page = navbar_page()

if page == "Home":
    home_page()

elif page == "Sobre o Projeto":
    sobre_nos_page()


elif page == "Visão Geral":
    df, _ = get_data()
    analise_page(df, key_aux="1")

elif page == "Análise Personalizada":
    st.write("\n")
    st.write("\n")
    df = eletrodomesticos_page()

    if st.session_state.get("btn_get_analise", False) and not df.empty:
        progress_text = "Gerando relatório personalizado"
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)

        st.session_state["ver_relatorio"] = True

    if st.session_state.get("ver_relatorio", False) and not df.empty:
        st.markdown("---")
        analise_page(df, key_aux="2")
