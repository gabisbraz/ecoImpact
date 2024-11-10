import streamlit as st
import pandas as pd

import sys
from pathlib import Path

DIR_ROOT = str(Path(__file__).parents[1])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from utils.get_data import get_data
from utils.dynamic_filter import DynamicFilters


def eletrodomesticos_page():

    # Função para carregar os dados iniciais
    df, df_user = get_data()

    def generate_google_link(marca, modelo):
        query = f"{marca} {modelo}"
        google_search_link = (
            f"https://www.google.com/search?q={query.replace(' ', '+')}"
        )
        return google_search_link

    # Cria a coluna 'LINK' com os hyperlinks
    df["LINK"] = df.apply(
        lambda row: generate_google_link(row["Marca"], row["Modelo"]), axis=1
    )
    df_user["LINK"] = df_user.apply(
        lambda row: generate_google_link(row["Marca"], row["Modelo"]), axis=1
    )

    # Inicializa df_user no estado da sessão, se ainda não estiver presente
    if "df_user" not in st.session_state:
        st.session_state["df_user"] = df_user

    # Seção de filtro para selecionar eletrodomésticos
    st.markdown(
        "# 1. Utilize os filtros para selecionar os eletrodomésticos que deseja analisar"
    )

    # Cria filtros dinâmicos para o DataFrame original
    dynamic_filters = DynamicFilters(
        df,
        filters=["Produto", "Marca", "Modelo"],
        filters_name="selected",
    )

    # Exibe os filtros
    dynamic_filters.display_filters(location="columns", num_columns=3)
    df_index = dynamic_filters.display_df(
        use_container_width=True,
        hide_index=True,
        on_select="rerun",  # Aciona a atualização do estado ao selecionar
        selection_mode=["multi-row"],  # Permite selecionar múltiplas linhas
        column_config={
            "LINK": st.column_config.LinkColumn("LINK", display_text="Saiba Mais"),
        },
    )

    # Botão para adicionar a seleção ao DataFrame de análise
    col_btn = st.columns([1, 1, 1])

    if len(df_index.get("selection", {}).get("rows", [])) != 0:
        # Captura as linhas selecionadas no df_index
        selected_rows = df_index.get("selection", {}).get("rows", [])
        df_selected = df_index.iloc[selected_rows]

        with col_btn[2]:
            if st.button(
                "Adicionar na lista", use_container_width=True, type="primary"
            ):
                if not df_selected.empty:
                    # Adiciona as linhas selecionadas ao DataFrame de análise no estado da sessão
                    st.session_state.df_user = pd.concat(
                        [st.session_state.df_user, df_selected]
                    ).drop_duplicates()

    # Exibe o DataFrame de eletrodomésticos selecionados para análise
    st.markdown("# 2. Visualize os eletrodomésticos escolhidos para análise")
    df_selected_for_analysis = st.session_state.df_user

    # Exibe o DataFrame com os eletrodomésticos selecionados
    df_index = st.dataframe(
        df_selected_for_analysis,
        hide_index=True,
        use_container_width=True,
        column_order=["Marca", "Modelo", "Produto", "LINK"],
        on_select="rerun",  # Aciona a atualização do estado ao selecionar
        selection_mode=["multi-row"],  # Permite selecionar múltiplas linhas
        column_config={
            "LINK": st.column_config.LinkColumn("LINK", display_text="Saiba Mais"),
        },
    )
    # Botão para adicionar a seleção ao DataFrame de análise
    col_btn = st.columns([1, 1, 1])
    with col_btn[2]:
        if st.button("Remover na lista", use_container_width=True, type="primary"):

            if len(df_index.get("selection", {}).get("rows", [])) != 0:
                # Captura as linhas selecionadas no df_index
                selected_rows = df_index.get("selection", {}).get("rows", [])
                df_selected = df.iloc[selected_rows]
                # Remove as linhas selecionadas
                st.session_state.df_user = st.session_state.df_user.drop(
                    df_selected, axis=1
                )

    # Botão para gerar o relatório final com os eletrodomésticos selecionados
    st.button("Gerar relatório", use_container_width=True, key="btn_get_analise")

    return st.session_state.df_user
