import streamlit as st


class Cards:

    def __init__(
        self,
        titulo: str = "-",
        qtd_valor: int = 0,
        porcentagem: float = 0,
        serie_historica: dict = {},
        color: str = "grey",
    ):
        self.titulo = titulo
        self.qtd_valor = qtd_valor
        self.porcentagem = porcentagem
        self.serie_historica = serie_historica
        self.color = color
        self.card = None

    def render_html_card(self):
        if self.porcentagem != 0:
            html = f"""
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
            <div style='box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); display: flex; border-radius: 10px; height: 100%;'>
                <div style='border-left: 1rem solid {self.color}; border-top-left-radius: 10px; border-bottom-left-radius: 10px;'>
                </div>
                <div style='width: 100%;'>
                    <div style='display: flex; width: 100%;'>
                        <div style='margin-left: 10px; width: 100%; display: flex; flex-direction: column;'>
                            <div style='width: 100%; padding-top: 8px; padding-bottom: 12px; color: #4D4D4D; font-weight: 400;'>{self.titulo.title()}</div>
                            <div style='display: flex; padding-bottom: 15px;'>
                                <div style='font-size: 25px; font-weight: 400; display: flex; align-items: center;'>
                                    {str(self.qtd_valor)}
                                </div>
                                <div style='width: 1px; background-color: black; margin-left: 20px; margin-right: 20px; display: flex; align-items: center;'>
                                </div>
                                <div style='font-size: 20px; font-weight: 300; display: flex; align-items: center;'>
                                    {str(self.porcentagem).replace(".", ",")}%
                                </div>
                            </div>
                        </div>
                        <div style='padding-top: 5px; padding-right: 8px;'>
                            <i class='bi bi-x-circle-fill' style='font-size: 1.3rem; color: {self.color};'></i>
                        </div>
                    </div>
                </div>
            </div>
            """
        else:
            html = f"""
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
            <div style='box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); display: flex; border-radius: 10px; height: 100%;'>
                <div style='border-left: 1rem solid {self.color}; border-top-left-radius: 10px; border-bottom-left-radius: 10px;'>
                </div>
                <div style='width: 100%;'>
                    <div style='display: flex; width: 100%;'>
                        <div style='margin-left: 10px; width: 100%; display: flex; flex-direction: column;'>
                            <div style='width: 100%; padding-top: 8px; padding-bottom: 12px; color: #4D4D4D; font-weight: 400;'>{self.titulo.title()}</div>
                            <div style='display: flex; padding-bottom: 15px;'>
                                <div style='font-size: 25px; font-weight: 400; display: flex; align-items: center;'>
                                    {str(self.qtd_valor)}
                                </div>
                            </div>
                        </div>
                        <div style='padding-top: 5px; padding-right: 8px;'>
                            <i class='bi bi-x-circle-fill' style='font-size: 1.3rem; color: {self.color};'></i>
                        </div>
                    </div>
                </div>
            </div>
            """

        st.markdown(html, unsafe_allow_html=True)
        return html
