import streamlit as st
import base64

import sys
from pathlib import Path

DIR_ROOT = str(Path(__file__).parents[1])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from utils.footer import footer_page


def home_page():
    st.write("\n")

    with open(
        Path(DIR_ROOT, "assets/environmental-audit-animate.svg"), "rb"
    ) as svg_file:
        svg_base64 = base64.b64encode(svg_file.read()).decode("utf-8")

    footer_page()
    cols = st.columns(2)
    with cols[0]:
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")
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

            <div style="font-weight: 1000; font-size: 45px; color: #3B5B33">EcoImpact</div>
            <div style="font-weight: 1000; font-size: 40px; color: black">Descubra o impacto ambiental dos seus eletrodomésticos</div>
            <div style="font-size: 20px; padding-bottom: 20px;">Descubra o quanto os seus aparelhos afetam o meio ambiente e adote práticas mais sustentáveis para um futuro melhor!</div>
            """,
            unsafe_allow_html=True,
        )

        st.button("**Faça sua análise agora**", use_container_width=False)
    with cols[1]:

        st.write("\n")
        st.write("\n")
        st.write("\n")
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
