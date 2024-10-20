import streamlit as st
import pandas as pd
import base64
from streamlit_dynamic_filters import DynamicFilters
from streamlit_navigation_bar import st_navbar
from streamlit_echarts import st_echarts
import streamlit_antd_components as sac
from streamlit_extras.dataframe_explorer import dataframe_explorer

from utils.create_card import Cards


st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

pages = ["Home", "Sobre o Projeto", "Dashboard", "Calcule o seu!"]
styles = {
    "nav": {
        "background-color": "#495B29",
        "display": "flex",
        "justify-content": "flex-end",
    },
    "div": {"max-width": "32rem", "padding-top": "10px", "padding-bottom": "10px"},
    "span": {
        "border-radius": "0.5rem",
        "color": "#CFCBBA",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {"background-color": "rgba(189, 209, 155, 0.25)", "color": "white"},
    "hover": {
        "background-color": "rgba(189, 209, 155, 0.5)",
    },
}


@st.cache_data
def get_data():
    df = pd.read_excel("app/data/output/BASE_FINAL.xlsx")
    return df, pd.DataFrame(columns=list(df.columns))


df, df_user = get_data()

page = st_navbar(pages, styles=styles)

if page == "Home":
    st.title("EcoImpact")
    with open("app/assets/environmental-audit-animate.svg", "rb") as svg_file:
        svg_base64 = base64.b64encode(svg_file.read()).decode("utf-8")

    cols = st.columns(2)
    with cols[0]:
        st.markdown(
            f"""
            <style>
                .stButton {{
                    color: #18314f;
                }}
                .stButton:active {{
                    color: #18314f;
                }}
            </style>

            <div style="font-weight: 1000; font-size: 40px; color: #18314f">Descubra o impacto ambiental dos seus eletrodomésticos</div>
            <div style="font-size: 20px; padding-bottom: 20px;">Descubra o quanto os seus aparelhos afetam o meio ambiente e adote práticas mais sustentáveis para um futuro mais verde!</div>
            """,
            unsafe_allow_html=True,
        )

        st.button("**Faça Sua Análise Agora**", use_container_width=False)
    with cols[1]:

        st.markdown(
            f"""
        <style>
        .stApp {{
            background: white;
        }}
        .principal {{
            display: flex;
            height: 400px;
        }}
        .container-left {{
            width: 50%;
        }}
        </style>
        
        <div style="width: 100%; height: 100%;">
            <img src="data:image/svg+xml;base64,{svg_base64}" style="width: 110%; margin-top: -100px;"/>                
        </div>
        """,
            unsafe_allow_html=True,
        )

elif page == "Sobre o Projeto":
    with open("app/assets/sobre_o_projeto_page_vector.svg", "rb") as svg_file:
        svg_base64 = base64.b64encode(svg_file.read()).decode("utf-8")

    cols = st.columns(2)
    with cols[1]:
        st.title("Sobre nós")
        st.markdown(
            f"""
                <div style="font-size: 20px; padding-bottom: 20px;">Somos três estudantes de Ciência da Computação, motivadas pelo estado ambiental do planeta, e criamos este site para avaliar o impacto ambiental dos eletrodomésticos, considerando aspectos como consumo de energia e tipos de fluidos refrigerantes. Equipamentos como ar-condicionados e refrigeradores podem ter um grande efeito no meio ambiente, contribuindo para emissões de gases de efeito estufa e outros impactos ecológicos. Utilizamos dados detalhados do INMETRO para fornecer relatórios e gráficos que mostram claramente como suas escolhas afetam o meio ambiente. Com essas análises, você pode comparar diferentes marcas e modelos, ajudando a tomar decisões mais informadas e sustentáveis para reduzir sua pegada ecológica.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with cols[0]:

        st.markdown(
            f"""
        <style>
        .stApp {{
            background: white;
        }}
        .principal {{
            display: flex;
            height: 400px;
        }}
        .container-left {{
            width: 50%;
        }}
        </style>
        
        <div style="width: 100%; height: 100%;">
            <img src="data:image/svg+xml;base64,{svg_base64}" style="width: 90%;"/>                
        </div>
        """,
            unsafe_allow_html=True,
        )
elif page == "Dashboard":

    if "df_user" not in st.session_state:
        st.session_state["df_user"] = df_user

    st.markdown(
        "#### 1. Utilize os filtros para selecionar os eletrodésticos que deseja analisar"
    )

    dynamic_filters = DynamicFilters(
        df,
        filters=["origem_dataframe", "Marca", "Modelo"],
        filters_name="selected",
    )
    dynamic_filters.display_filters(location="columns", num_columns=3)
    dynamic_filters.display_df(use_container_width=True, hide_index=True)

    col_btn = st.columns([1, 1, 1])
    print(list(df.columns))
    with col_btn[2]:
        if st.button("Adicionar na lista", use_container_width=True, type="primary"):
            df_aux = df.loc[
                (
                    (df["Marca"] == st.session_state.get("selectedMarca", [None])[0])
                    & (
                        df["Modelo"]
                        == st.session_state.get("selectedModelo", [None])[0]
                    )
                )
            ]
            st.session_state.df_user = pd.concat([st.session_state.df_user, df_aux])

    st.markdown("#### 2. Visualize os eletrodésticos escolhidos para análise")
    st.dataframe(
        st.session_state.df_user,
        on_select="rerun",
        selection_mode=["multi-row", "multi-column"],
        hide_index=True,
        use_container_width=True,
    )

    st.button("Gerar relatório", use_container_width=True)

#########################################################################################
else:
    # Definindo as cores da paleta
    colors = {
        "eletrodomesticos": "#33576E",
        "marcas": "#A0A742",
        "fluidos": "#BBCF9B",
        "gases": "#498B6D",
        "gases_pie": "#A0A742",  # Cor para o gráfico de pizza dos gases
        "fluido_pie": "#BBCF9B",  # Cor para o gráfico de pizza dos fluidos refrigerantes
    }

    color_list = [
        "#33576E",
        "#A0A742",
        "#BBCF9B",
        "#498B6D",
        "#A0A742",
        "#BBCF9B",
    ]

    # Montando os cartões
    col_cards = st.columns(4)
    with col_cards[0]:
        Cards(
            titulo="Eletrodomésticos Mapeados",
            qtd_valor=len(df),
            color=colors["eletrodomesticos"],
        ).render_html_card()
    with col_cards[1]:
        Cards(
            titulo="Marcas Avaliadas",
            qtd_valor=df["Marca"].nunique(),
            color=colors["marcas"],
        ).render_html_card()
    with col_cards[2]:
        Cards(
            titulo="Fluidos Refrigerantes Mapeados",
            qtd_valor=df["Fluido_refrigerante"].nunique(),
            color=colors["fluidos"],
        ).render_html_card()
    with col_cards[3]:
        Cards(
            titulo="Gases Mapeados",
            qtd_valor=df["Tipo_gas"].nunique(),
            color=colors["gases"],
        ).render_html_card()

    st.write("\n")

    # Filtrar os aparelhos com melhor classificação energética
    df_melhor_classificacao = df[
        df["Classificacao_energetica"].isin(["A", "A+++", "A+", "A++"])
    ]

    # Contar as ocorrências de cada marca com classificação "A"
    ranking_marcas = df_melhor_classificacao["Marca"].value_counts().head(10)

    # Configurações do gráfico de barras
    options = {
        "title": {"text": "Ranking das Marcas com Melhor Classificação Energética"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "yAxis": {"type": "category", "data": ranking_marcas.index.tolist()},
        "xAxis": {"type": "value"},
        "series": [
            {
                "data": ranking_marcas.values.tolist(),
                "type": "bar",
                "color": ["#003366"],
            }
        ],
    }

    cols = st.columns([2, 2, 2], gap="small")
    with cols[0]:
        st_echarts(options=options)

    with cols[1]:
        # Contar a distribuição dos tipos de gás
        tipo_gas_distribution = df["Tipo_gas"].value_counts().reset_index()
        tipo_gas_distribution.columns = ["Tipo_gas", "Count"]
        tipo_gas_distribution = tipo_gas_distribution[
            tipo_gas_distribution["Tipo_gas"] != "-"
        ]

        # Configurações do gráfico de pizza
        options_pie = {
            "title": {"text": "Distribuição dos Tipos de Gás", "left": "center"},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "horizontal", "bottom": "8%"},
            "series": [
                {
                    "name": "Tipo de Gás",
                    "type": "pie",
                    "radius": "50%",
                    "data": [
                        {"value": v, "name": k}
                        for k, v in zip(
                            tipo_gas_distribution["Tipo_gas"].tolist(),
                            tipo_gas_distribution["Count"].tolist(),
                        )
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        }
        st_echarts(options=options_pie, key="ewd")

    with cols[2]:
        # Contar a distribuição dos fluidos refrigerantes
        tipo_fluido_distribution = (
            df["Fluido_refrigerante"].value_counts().reset_index()
        )
        tipo_fluido_distribution.columns = ["Fluido_refrigerante", "Count"]
        tipo_fluido_distribution = tipo_fluido_distribution[
            tipo_fluido_distribution["Fluido_refrigerante"] != "-"
        ]

        # Configurações do gráfico de pizza
        options_fluido_pie = {
            "title": {
                "text": "Distribuição dos Fluidos Refrigerantes",
                "left": "center",
            },
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "horizontal", "bottom": "8%"},
            "series": [
                {
                    "name": "Fluido Refrigerante",
                    "type": "pie",
                    "radius": "50%",
                    "data": [
                        {"value": v, "name": k}
                        for k, v in zip(
                            tipo_fluido_distribution["Fluido_refrigerante"].tolist(),
                            tipo_fluido_distribution["Count"].tolist(),
                        )
                    ],
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        }
        st_echarts(options=options_fluido_pie)

    # Criar abas usando streamlit_antd_components
    tabs = sac.tabs(
        [
            sac.TabsItem(label=origem)
            for origem in df_melhor_classificacao["origem_dataframe"].unique()
        ],
        color="green",
        variant="outline",
    )
    df_origem = df_melhor_classificacao[
        df_melhor_classificacao["origem_dataframe"] == tabs
    ]

    ranking_marcas_origem = df_origem["Marca"].value_counts().head(10)

    # Configurações do gráfico de barras agrupadas
    options = {
        "title": {
            "text": f"Ranking das Marcas com Melhor Classificação Energética - {tabs}"
        },
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {
            "type": "category",
            "data": ranking_marcas_origem.index.tolist(),
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": ranking_marcas_origem.values.tolist(),
                "type": "bar",
                "backgroundStyle": {"color": "rgba(180, 180, 180, 0.2)"},
                "itemStyle": {"color": colors["marcas"]},
            }
        ],
    }

    st.subheader(f"Gráfico para {tabs}")
    st_echarts(options=options)

    with st.expander("Visualizar tabela!"):
        filtered_df = dataframe_explorer(df, case=False)
        st.dataframe(filtered_df, use_container_width=True)
