import streamlit as st


def footer_page():
    footer_html = """
    <style>
      /* Hide Streamlit default footer and menu */
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      
      /* Footer styling */
      .custom-footer {
          display: flex;
          align-items: center;
          position: fixed;
          left: 0;
          bottom: 0;
          width: 100%;
          background-color: #495B29;
          color: white;
          padding: 25px 20px;
          font-family: Arial, sans-serif;
          font-size: 14px;
      }

      .footer-left, .footer-center, .footer-right {
          padding: 0 20px;
          color: white;
      }

      .footer-link {
          color: white;
          text-decoration: none;
      }
      
      .footer-link:hover {
          text-decoration: underline;
          color: white;
      }
    </style>

    <div class="custom-footer">
        <div class="footer-left">
            <a href="https://www.gov.br/inmetro/pt-br" target="_blank" style="color: white;" class="footer-link">DADOS INMETRO</a>
        </div>
        <div class="footer-right">
            <a href="https://github.com/gabisbraz" target="_blank" style="color: white;" class="footer-link">GITHUB</a>
        </div>
        <div class="footer-center">
            Made with ❤️ by GMG
        </div>
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)
