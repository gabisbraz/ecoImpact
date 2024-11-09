import sys
from pathlib import Path
from streamlit_navigation_bar import st_navbar

DIR_ROOT = str(Path(__file__).parents[1])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)


def navbar_page():
    pages = ["Home", "Sobre o Projeto", "Visão Geral", "Análise Personalizada"]
    styles = {
        "nav": {
            "background-color": "#495B29",
            "display": "flex",
            "justify-content": "flex-end",
            "height": "70px",
        },
        "div": {"max-width": "32rem", "padding-top": "30px", "padding-bottom": "30px"},
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
    return st_navbar(pages, styles=styles)
