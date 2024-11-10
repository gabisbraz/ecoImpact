import streamlit as st
from streamlit_echarts import st_echarts
import streamlit_antd_components as sac

import sys
from pathlib import Path

DIR_ROOT = str(Path(__file__).parents[1])
if DIR_ROOT not in sys.path:
    sys.path.append(DIR_ROOT)

from utils.create_card import Cards
from utils.dataframe_exp import dataframe_explorer


def analise_page(df):

    def generate_google_link(marca, modelo):
        query = f"{marca} {modelo}"
        google_search_link = (
            f"https://www.google.com/search?q={query.replace(' ', '+')}"
        )
        return google_search_link

    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.title("1. Visualize os aparelhos mapedos")
    # Definindo as cores da paleta
    colors = {
        "eletrodomesticos": "#33576E",
        "marcas": "#A0A742",
        "fluidos": "#BBCF9B",
        "gases": "#498B6D",
        "gases_pie": "#A0A742",  # Cor para o gráfico de pizza dos gases
        "fluido_pie": "#BBCF9B",  # Cor para o gráfico de pizza dos fluidos refrigerantes
    }

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
        x = len(df.loc[df["Classificação Energética"].isin(["E", "F", "D"])])
        y = len(df.loc[df["Classificação Energética"].isin(["GLP"])])
        z = len(df.loc[df["Fluído Refrigerante"].isin(["R-410a", "R-134a"])])
        Cards(
            titulo="Alto Impacto Ambiental",
            qtd_valor=x + y + z,
            color=colors["fluidos"],
        ).render_html_card()
    with col_cards[3]:
        Cards(
            titulo="Gases Mapeados",
            qtd_valor=df["Tipo de Gás"].nunique(),
            color=colors["gases"],
        ).render_html_card()
    st.write("\n")
    with st.expander("Visualizar tabela!"):
        # Cria a coluna 'LINK' com os hyperlinks
        df["LINK"] = df.apply(
            lambda row: generate_google_link(row["Marca"], row["Modelo"]), axis=1
        )
        filtered_df = dataframe_explorer(df, case=False, key="data_geral_mult")
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "LINK": st.column_config.LinkColumn("LINK", display_text="Saiba Mais"),
            },
            key="data_geral1",
        )

    st.write("\n")
    st.title("2. Entenda o impacto ambiental dos eletrodomésticos")

    cols = st.columns([2.7, 2, 2], gap="small")
    with cols[0]:
        # Filtrar os aparelhos com melhor classificação energética
        df_melhor_classificacao = df[
            df["Classificação Energética"].isin(["A", "A+++", "A+", "A++"])
        ]

        # Contar as ocorrências de cada produto para cada marca
        ranking_produtos = (
            df_melhor_classificacao.groupby(["Marca", "Produto"])
            .size()
            .unstack(fill_value=0)
        )

        # Selecionar as 10 marcas mais frequentes com base na soma das ocorrências de produtos
        top_10_marcas = ranking_produtos.sum(axis=1).nlargest(10).index

        # Filtrar o ranking de produtos para incluir apenas as 10 melhores marcas
        ranking_produtos_top_10 = ranking_produtos.loc[top_10_marcas]

        # Configurações do gráfico de barras empilhadas
        options = {
            "title": {
                "text": "10 Melhores Marcas com Melhor Classificação Energética",
                "textStyle": {"fontSize": 12},
            },
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {
                "data": ranking_produtos_top_10.columns.tolist(),
                "bottom": 0,  # Definindo quais produtos serão exibidos na legenda
                "type": "scroll",
                "orient": "horizontal",
                "right": 18,
            },
            "yAxis": {
                "type": "category",
                "data": ranking_produtos_top_10.index.tolist(),
                "axisLine": {"show": False},
                "splitLine": {"show": False},
                "nameTextStyle": {"width": 300},  # Marcas no eixo Y (top 10)
            },
            "xAxis": {"type": "value", "axisLine": {"show": False}},
            "series": [
                {
                    "name": produto,
                    "data": ranking_produtos_top_10[produto].tolist(),
                    "type": "bar",
                    "stack": "stacked",  # Habilita o empilhamento de barras
                }
                for produto in ranking_produtos_top_10.columns  # Cria uma série para cada produto
            ],
        }

        # Exibindo o gráfico
        st_echarts(options=options, height="360px", width="105%", key="chart_top_10")

    with cols[1]:
        # Contar a distribuição dos tipos de gás
        tipo_gas_distribution = df["Tipo de Gás"].value_counts().reset_index()
        tipo_gas_distribution.columns = ["Tipo de Gás", "Count"]
        tipo_gas_distribution = tipo_gas_distribution[
            tipo_gas_distribution["Tipo de Gás"] != "-"
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
                            tipo_gas_distribution["Tipo de Gás"].tolist(),
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
        st_echarts(options=options_pie, key="chart_gas")

        # Texto a ser exibido no modal
        modal_text = """
        Tanto o **gás natural (GN)** quanto o **gás liquefeito de petróleo (GLP)** são fontes de energia fóssil, o que significa que ambos têm impactos ambientais, principalmente em relação às **emissões de gases de efeito estufa** e à **extração de recursos naturais**. No entanto, quando comparados, o **gás natural** tende a ser mais **ecologicamente favorável** do que o **GLP** por vários motivos:

        ### Impacto Ambiental do Gás Natural (GN):
        - **Composição**: O GN é principalmente composto de **metano (CH₄)**, que, quando queimado, gera **dióxido de carbono (CO₂)**, mas em menor quantidade em comparação com o carvão e o petróleo.
        - **Emissões de Gases de Efeito Estufa**: O GN emite cerca de **50% a 60% menos CO₂** do que o carvão e o óleo ao ser queimado, o que o torna uma opção mais limpa em termos de emissões de carbono. 
        - **Emissões de Poluentes**: Além de gerar menos CO₂, o gás natural emite **menos óxidos de nitrogênio (NOx)** e **partículas** que contribuem para a poluição do ar e para a formação de smog, comparado a outros combustíveis fósseis.
        - **Exploração e Transporte**: O processo de extração de gás natural (principalmente por meio de fraturamento hidráulico ou "fracking") pode ter impactos negativos significativos, como a **contaminação da água** e a **liberação de metano** durante o transporte e armazenamento, que é um potente gás de efeito estufa. O metano, se não for bem controlado, pode ter um impacto climático muito maior que o CO₂, com um potencial de aquecimento global **muitas vezes maior**.

        ### Impacto Ambiental do Gás Liquefeito de Petróleo (GLP):
        - **Composição**: O GLP é composto principalmente por **propano** e **butano**, que são **hidrocarbonetos mais pesados** em comparação ao metano do GN.
        - **Emissões de Gases de Efeito Estufa**: O GLP emite **mais CO₂ por unidade de energia** do que o gás natural, pois os hidrocarbonetos presentes no GLP possuem uma maior quantidade de carbono. Isso significa que, para a mesma quantidade de energia gerada, o GLP tende a liberar mais dióxido de carbono na atmosfera.
        - **Extração e Processamento**: O GLP é um subproduto da extração de **petróleo e gás natural**, e seu processo de **extração e liquefação** consome energia, o que contribui para emissões adicionais. Além disso, o armazenamento e o transporte do GLP em **botijões** podem gerar riscos de vazamentos de gás, liberando também metano, um potente gás de efeito estufa.

        ### Comparação Ecológica: GN vs GLP

        1. **Emissões de CO₂**:
        - O **gás natural** é mais eficiente em termos de emissões de CO₂, liberando menos dióxido de carbono do que o GLP para a mesma quantidade de energia gerada.
        - O **GLP** emite mais CO₂ porque seus hidrocarbonetos são mais pesados e têm maior quantidade de carbono.

        2. **Emissões de Metano**:
        - O **gás natural** pode ter uma pegada de metano maior se houver vazamentos durante a extração ou o transporte (como é o caso do fracking), mas, se bem controlado, o GN ainda pode ser mais vantajoso que o GLP nesse sentido.
        - O **GLP** também pode ter vazamentos durante o armazenamento e o transporte, mas seu impacto global tende a ser menor em termos de vazamento de metano, pois ele não depende tanto de infraestruturas de extração complexas.

        3. **Eficiência Energética**:
        - O **gás natural** tende a ser **mais eficiente** na geração de energia (menos emissões por unidade de energia gerada) em comparação ao GLP.
        
        4. **Impacto na Saúde e Poluição do Ar**:
        - O **gás natural** emite **menos poluentes** como óxidos de nitrogênio (NOx) e partículas finas, que são prejudiciais à saúde humana e contribuem para a poluição do ar.
        - O **GLP** também emite menos NOx e partículas do que o carvão, mas, devido ao maior conteúdo de carbono, ainda tem um impacto maior em relação ao CO₂.

        ### Conclusão:
        - **Ecologicamente, o gás natural (GN) é mais vantajoso** do que o GLP. Ele emite menos CO₂ por unidade de energia gerada, é mais eficiente e tem menor impacto em termos de poluição do ar.
        - **No entanto**, ambos são combustíveis fósseis, e, em um contexto de **sustentabilidade de longo prazo**, a transição para fontes de energia **renováveis e limpas** (como solar, eólica e hidroelétrica) é crucial para reduzir as emissões de gases de efeito estufa e os impactos ambientais associados ao uso de energia.

        Portanto, embora o **GN** seja uma opção **menos prejudicial ao meio ambiente** comparado ao **GLP**, o ideal é buscar alternativas mais ecológicas para reduzir nossa dependência de combustíveis fósseis.
        """

        # Função para abrir o modal com o texto
        @st.dialog("Gás Natural (GN) x Gás Liquefeito de Petróleo (GLP)", width="large")
        def open_modal():
            st.markdown(modal_text)

        if st.button("Entenda mais!", use_container_width=True):
            open_modal()

    with cols[2]:
        # Contar a distribuição dos fluidos refrigerantes
        tipo_fluido_distribution = (
            df["Fluído Refrigerante"].value_counts().reset_index()
        )
        tipo_fluido_distribution.columns = ["Fluído Refrigerante", "Count"]
        tipo_fluido_distribution = tipo_fluido_distribution[
            tipo_fluido_distribution["Fluído Refrigerante"] != "-"
        ]

        # Configurações do gráfico de pizza
        options_fluido_pie = {
            "title": {
                "text": "Distribuição dos Fluidos Refrigerantes",
                "left": "center",
            },
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "horizontal", "bottom": "0"},
            "series": [
                {
                    "name": "Fluido Refrigerante",
                    "type": "pie",
                    "radius": "50%",
                    "data": [
                        {"value": v, "name": k}
                        for k, v in zip(
                            tipo_fluido_distribution["Fluído Refrigerante"].tolist(),
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
        st_echarts(options=options_fluido_pie, key="chart_fluidos")
        # Texto a ser exibido no modal
        modal_text = """
        Aqui está uma explicação detalhada sobre cada um dos refrigerantes mencionados, incluindo os **malefícios** para o meio ambiente e a saúde, com foco no impacto ecológico.

### 1. **R-600a (Isobutano)**

   - **O que é?**  
     O R-600a é um **refrigerante natural**, classificado como hidrocarboneto, com **baixo impacto ambiental** e **alta eficiência energética**. Ele é amplamente utilizado em sistemas de refrigeração doméstica, como **refrigeradores** e **freezers**.

   - **Malefícios:**
     - **Inflamabilidade**: O principal risco associado ao R-600a é a sua **alta inflamabilidade**. Caso o refrigerante vaze e entre em contato com uma fonte de ignição, pode causar incêndios ou explosões.
     - **Gases de efeito estufa**: Embora tenha um **PAG muito baixo (20)**, o R-600a ainda pode contribuir para o **aquecimento global** se for liberado de maneira inadequada no ambiente. No entanto, seu impacto é **muito menor** do que os refrigerantes sintéticos mais antigos.
  
   - **Vantagens Ecológicas**:
     - **Baixo PAG** e **nenhum impacto sobre a camada de ozônio** (não contém cloro), tornando-o **ecologicamente amigável** em comparação com refrigerantes sintéticos.

---

### 2. **R-32 (Difluorometano)**

   - **O que é?**  
     O R-32 é um refrigerante **sintético**, mas com um **PAG significativamente menor** do que outros refrigerantes mais antigos, como o R-410a. Ele é uma opção popular em sistemas modernos de **ar-condicionado** e **climatização** devido à sua eficiência energética.

   - **Malefícios:**
     - **PAG Moderado (675)**: Embora o PAG do R-32 seja menor que o de muitos refrigerantes antigos, ele ainda contribui para o aquecimento global. Seu **PAG é 34% menor** do que o R-410a, mas **ainda é um gás de efeito estufa**.
     - **Toxicidade**: O R-32 pode ser **tóxico em concentrações elevadas**. Embora não seja altamente inflamável, o vazamento de grandes quantidades pode ser perigoso para a saúde humana.
     - **Risco de asfixia**: Em grandes concentrações, o R-32 pode deslocar o oxigênio no ar e causar asfixia em ambientes fechados.

   - **Vantagens Ecológicas**:
     - **Baixo PAG** e **nenhum impacto sobre a camada de ozônio**. O R-32 é mais **ecológico** do que o R-410a e tem sido promovido como uma alternativa para reduzir o impacto ambiental de sistemas de refrigeração.

---

### 3. **R-410a (Mistura de hidrofluorocarbonetos)**

   - **O que é?**  
     O R-410a é uma mistura de dois refrigerantes sintéticos: **R-125** e **R-32**. Ele é amplamente utilizado em sistemas de **ar-condicionado** e **climatização**, especialmente em aparelhos mais antigos, devido à sua alta eficiência de refrigeração.

   - **Malefícios:**
     - **Alto PAG (2088)**: O R-410a tem um **PAG muito alto**, o que significa que, se liberado na atmosfera, contribui significativamente para o **aquecimento global**. Mesmo que ele não afete diretamente a camada de ozônio (não contém cloro), seu **alto impacto climático** o torna menos sustentável.
     - **Contribuição para o aquecimento global**: Devido ao seu alto PAG, o R-410a é considerado um dos refrigerantes mais **nocivos ao clima** entre os refrigerantes sintéticos.
     - **Pressão e custo**: O R-410a opera em **pressões mais altas** do que refrigerantes mais antigos, o que pode aumentar o custo e a complexidade dos sistemas de refrigeração. Além disso, pode **aumentar o risco de falhas e vazamentos**.

   - **Vantagens**:
     - **Alta eficiência energética** e **boa performance** em sistemas de climatização e refrigeração.

---

### 4. **R-134a (1,1,1,2-Tetrafluoroetano)**

   - **O que é?**  
     O R-134a é um refrigerante **sintético** que foi amplamente utilizado para substituir os CFCs (clorofluorocarbonetos), que eram prejudiciais à camada de ozônio. Ele é utilizado em **refrigeradores**, **freezers** e **ar-condicionado**, especialmente em modelos mais antigos.

   - **Malefícios:**
     - **PAG Alto (1430)**: O R-134a tem um **PAG elevado**, o que significa que ele contribui para o **aquecimento global** de maneira significativa. Mesmo sendo melhor que os antigos CFCs, o seu impacto climático ainda é considerável.
     - **Substituição**: Devido ao seu alto impacto no aquecimento global, o R-134a está sendo progressivamente substituído por refrigerantes com menor PAG, como o R-32.
     - **Não afeta a camada de ozônio**: Assim como o R-410a, o R-134a não contém cloro, então não tem impacto direto sobre a camada de ozônio.

   - **Vantagens**:
     - **Segurança**: O R-134a é **não inflamável** e seguro para uso em sistemas de refrigeração e climatização.

---

### Resumo dos **Malefícios**:

| **Refrigerante** | **PAG** | **Impacto no Aquecimento Global** | **Impacto na Camada de Ozônio** | **Outros Malefícios** |
|------------------|---------|-----------------------------------|--------------------------------|-----------------------|
| **R-600a (Isobutano)** | 20      | Muito baixo                      | Nenhum                         | Inflamabilidade (risco de incêndio ou explosão) |
| **R-32 (Difluorometano)** | 675     | Moderado                         | Nenhum                         | Pode ser tóxico em grandes concentrações; risco de asfixia |
| **R-410a (Mistura de HFCs)** | 2088    | Alto                             | Nenhum                         | Contribui significativamente para o aquecimento global; pressões elevadas nos sistemas |
| **R-134a (Tetrafluoroetano)** | 1430    | Alto                             | Nenhum                         | Contribui para o aquecimento global; sendo substituído por alternativas mais ecológicas |

### Conclusão:

- **R-600a** é o mais ecológico em termos de impacto climático, mas apresenta riscos devido à sua **inflamabilidade**.
- **R-32** tem um impacto menor no aquecimento global em comparação com refrigerantes mais antigos, mas pode ser **tóxico em altas concentrações**.
- **R-410a** e **R-134a** têm **alto impacto no aquecimento global**, sendo o R-410a especialmente prejudicial devido ao seu **PAG elevado**. Ambos são seguros para a camada de ozônio, mas não são as melhores opções do ponto de vista ecológico.
        """

        # Função para abrir o modal com o texto
        @st.dialog("Fluidos Refrigerantes", width="large")
        def open_modal():
            st.markdown(modal_text)

        if st.button("Entenda mais!", use_container_width=True, key="fluidos_modal"):
            open_modal()

    col1, col2 = st.columns([4, 1], vertical_alignment="bottom")
    with col1:
        st.title("3. Veja as marcas mais sustentáveis energeticamente")
    with col2:
        modal_text = """
    As classificações energéticas do INMETRO (Instituto Nacional de Metrologia, Qualidade e Tecnologia) para aparelhos eletrodomésticos têm como objetivo informar aos consumidores sobre a eficiência energética de diversos produtos. Essas classificações ajudam na escolha de equipamentos que consomem menos energia, contribuindo para a redução de custos e o impacto ambiental.

Aqui estão os principais pontos sobre as classificações energéticas do INMETRO:

### 1. **Etiqueta Procel**
A etiqueta **Procel** (Programa Nacional de Conservação de Energia Elétrica) é uma das principais ferramentas para informar a eficiência energética de produtos no Brasil. Essa etiqueta é colocada em diversos aparelhos, como geladeiras, máquinas de lavar, ar-condicionado, chuveiros elétricos, entre outros. O objetivo é indicar quanta energia o produto consome em comparação com outros do mesmo tipo.

#### Escala de Eficiência Energética:
- **A (mais eficiente)**: Significa que o produto é o mais eficiente em termos de consumo de energia, ou seja, gasta menos eletricidade para realizar a mesma função.
- **B a E**: A escala vai de A (melhor) a E (pior), com a letra A representando os aparelhos com menor consumo de energia e a letra E indicando os aparelhos com maior consumo de energia.

Em alguns casos, também existem aparelhos classificados com a letra **"A+"** ou **"A++"**, indicando um nível ainda mais alto de eficiência energética.

### 2. **Como Funciona a Classificação**
O INMETRO avalia a eficiência de cada produto com base em testes realizados em laboratórios credenciados. Os critérios podem variar dependendo do tipo de aparelho, mas geralmente envolvem aspectos como:
- O consumo de energia do aparelho (em kWh - quilowatt-hora).
- A quantidade de energia que o produto utiliza para realizar sua função (por exemplo, refrigerar alimentos, lavar roupas).
- A eficiência em diferentes condições de operação.

A avaliação é comparada com um padrão estabelecido para o tipo de produto, e com isso é atribuída a letra correspondente (A, B, C, etc.).

### 3. **Objetivos das Etiquetas de Eficiência Energética**
- **Economia de energia**: Auxilia os consumidores a escolherem produtos que consomem menos energia, reduzindo suas contas de eletricidade.
- **Conservação ambiental**: Produtos mais eficientes geram um impacto ambiental menor, pois consomem menos recursos naturais.
- **Incentivo ao mercado**: Produtos mais eficientes se tornam mais atraentes para os consumidores, estimulando fabricantes a investirem em tecnologias que melhorem o desempenho energético dos seus produtos.

### 4. **Produtos com Etiqueta Energética**
Alguns exemplos de aparelhos eletrodomésticos que recebem a etiqueta de eficiência energética do INMETRO são:
- **Geladeiras e freezers**: Avaliados pelo consumo de energia no processo de resfriamento e congelamento.
- **Ar-condicionado**: Avaliado pela eficiência no consumo de energia ao refrigerar o ambiente.
- **Máquinas de lavar roupa e lava-louças**: A classificação leva em conta a quantidade de energia necessária para realizar ciclos de lavagem.
- **Iluminação**: Lâmpadas também possuem a etiqueta de eficiência, onde as mais eficientes (LEDs, por exemplo) recebem a classificação mais alta.


| **Letra** | **Descrição**                                                 | **Significado**                                                                                                      |
|-----------|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| **A**     | **Muito eficiente**                                           | O aparelho é o mais eficiente em termos de consumo de energia. Consome menos eletricidade em relação aos demais modelos da mesma categoria. |
| **B**     | **Eficiente**                                                 | O aparelho apresenta boa eficiência energética, mas consome um pouco mais de energia do que o modelo classificado como A. |
| **C**     | **Razoável**                                                  | O aparelho tem um consumo de energia intermediário em comparação aos outros da mesma categoria.                       |
| **D**     | **Padrão**                                                    | O aparelho apresenta um consumo de energia mais alto, mas ainda dentro de limites aceitáveis para sua classe.        |
| **E**     | **Pouco eficiente**                                           | O aparelho tem alto consumo de energia, sendo menos eficiente do que outros produtos da mesma categoria.              |
| **F**     | **Muito ineficiente**                                         | O aparelho consome uma quantidade excessiva de energia, sendo o menos eficiente da sua categoria.                    |
"""

        # Função para abrir o modal com o texto
        @st.dialog("Classificação Energética", width="large")
        def open_modal():
            st.markdown(modal_text)

        if st.button(
            "Entenda mais!", use_container_width=True, key="classificacao_energ_modal"
        ):
            open_modal()
    # Criar abas usando streamlit_antd_components
    tabs = sac.tabs(
        [
            sac.TabsItem(label=origem)
            for origem in df_melhor_classificacao["Produto"].unique()
        ],
        color="green",
        variant="outline",
    )
    df_origem = df_melhor_classificacao[df_melhor_classificacao["Produto"] == tabs]

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

    st_echarts(options=options, key="chart_clas_energ")

    # Cria a coluna 'LINK' com os hyperlinks
    df_origem["LINK"] = df_origem.apply(
        lambda row: generate_google_link(row["Marca"], row["Modelo"]), axis=1
    )
    filtered_df = dataframe_explorer(df_origem, case=False, key="data_clas_energ_mult")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "LINK": st.column_config.LinkColumn("LINK", display_text="Saiba Mais"),
        },
        key="data_clas_energ",
    )
