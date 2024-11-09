import streamlit as st
import base64

import sys
from pathlib import Path

DIR_ROOT = str(Path(__file__).parents[1])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from utils.footer import footer_page


def sobre_nos_page():
    footer_page()

    with open("assets/sobre_o_projeto_page_vector.svg", "rb") as svg_file:
        svg_base64 = base64.b64encode(svg_file.read()).decode("utf-8")

    cols = st.columns(2)
    with cols[1]:
        st.title("Sobre nós")
        st.markdown(
            f"""
                <div style="font-size: 20px; padding-bottom: 20px;">Somos três estudantes de Ciência da Computação,
                motivadas pelo estado ambiental do planeta, e criamos este site para <b style='color: #3B5B33;'>avaliar o
                impacto ambiental dos eletrodomésticos</b>, considerando aspectos como <b style='color: #3B5B33;'>consumo de
                energia</b> e <b style='color: #3B5B33;'>tipos de fluidos refrigerantes</b>. Equipamentos como ar-condicionados e
                refrigeradores podem ter um grande efeito no meio ambiente, contribuindo para
                emissões de <b style='color: #3B5B33;'>gases de efeito estufa</b> e outros impactos ecológicos. Utilizamos
                dados detalhados do <b style='color: #3B5B33;'>INMETRO</b> para fornecer <b style='color: #3B5B33;'>relatórios e gráficos</b> que mostram
                claramente como suas escolhas afetam o meio ambiente. Com essas análises,
                você pode comparar diferentes marcas e modelos, ajudando a tomar <b style='color: #3B5B33;'>decisões
                mais informadas</b> e <b style='color: #3B5B33;'>sustentáveis</b> para reduzir sua <b style='color: #3B5B33;'>pegada ecológica</b>.</div>
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
