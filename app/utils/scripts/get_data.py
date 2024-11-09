import pandas as pd

df_aquecedores_de_agua = pd.read_csv("app/data/AQUECEDORES_DE_AGUA.csv")
df_condicionadores_de_ar = pd.read_csv("app/data/CONDICIONADORES_DE_AR.csv")
df_fogoes = pd.read_csv("app/data/FOGOES.csv")
df_forno_microondas = pd.read_csv("app/data/FORNO_MICROONDAS.csv")
df_maqina_de_lavar_roupa = pd.read_csv("app/data/MAQUINA_DE_LAVAR_ROUPA.csv")
df_refrigeradores = pd.read_csv("app/data/REFRIGERADORES.csv")
df_televisores = pd.read_csv("app/data/TELEVISORES.csv")


def transform_dataframe(df, origem):
    df_result = pd.DataFrame()
    df_result["Marca"] = df["Marca"]
    df_result["Modelo"] = df["Modelo"]
    df_result["origem_dataframe"] = origem

    if "Classificação PBE" in df.columns:
        df_result["Classificacao_energetica"] = df["Classificação PBE"]
    elif "Classificação  PBE" in df.columns:
        df_result["Classificacao_energetica"] = df["Classificação  PBE"]
    elif "Faixa de Classificação" in df.columns:
        df_result["Classificacao_energetica"] = df["Faixa de Classificação"]
    elif "Classificação PBE Forno" in df.columns:
        df_result["Classificacao_energetica"] = df["Classificação PBE Forno"]
    elif "Faixa de Classificação Global" in df.columns:
        df_result["Classificacao_energetica"] = df["Faixa de Classificação Global"]
    elif "Classificação" in df.columns:
        df_result["Classificacao_energetica"] = df["Classificação"]
    elif "Classe de Eficiência Energética Padrão 2022" in df.columns:
        df_result["Classificacao_energetica"] = df[
            "Classe de Eficiência Energética Padrão 2022"
        ]
    elif "Classificação Eficiência Energética" in df.columns:
        df_result["Classificacao_energetica"] = df[
            "Classificação Eficiência Energética"
        ]
    else:
        df_result["Classificacao_energetica"] = None

    if "Tipo de Gás" in df.columns:
        df_result["Tipo_gas"] = df["Tipo de Gás"]
    else:
        df_result["Tipo_gas"] = None

    if "Consumo de Energia Mensal (kWh/mês)" in df.columns:
        df_result["Consumo_energia_mensal_kWh"] = df[
            "Consumo de Energia Mensal (kWh/mês)"
        ]
    elif "Potência (kW)" in df.columns:
        df_result["Consumo_energia_mensal_kWh"] = df["Potência (kW)"] * 24 * 30
    elif "Consumo Anual de Energia (kWh)" in df.columns:
        df_result["Consumo_energia_mensal_kWh"] = (
            df["Consumo Anual de Energia (kWh)"] / 12
        )
    elif "Consumo (kWh/mês)" in df.columns:
        df_result["Consumo_energia_mensal_kWh"] = df["Consumo (kWh/mês)"]
    elif "Potência Nominal (W)" in df.columns:
        df_result["Consumo_energia_mensal_kWh"] = (
            df["Potência Nominal (W)"] * 24 * 30 / 1000
        )
    elif "Consumo de energia (kWh/ciclo) água fria" in df.columns:
        df_result["Consumo_energia_mensal_kWh"] = (
            df["Consumo de energia (kWh/ciclo) água quente"].combine_first(
                df["Consumo de energia (kWh/ciclo) água fria"]
            )
            * 24
            * 30
        )
    else:
        df_result["Consumo_energia_mensal_kWh"] = None

    if "Capacidade de Vazão (litros/min)" in df.columns:
        df_result["Consumo_agua_mensal_l"] = (
            df["Capacidade de Vazão (litros/min)"] * 60 * 30
        )
    elif "Consumo de água (l)" in df.columns:
        df_result["Consumo_agua_mensal_l"] = df["Consumo de água (l)"] * 30
    else:
        df_result["Consumo_agua_mensal_l"] = None

    df = df.rename(columns={"Fluido refrigerante": "Fluido Refrigerante"})
    if (
        "Fluido Refrigerante" in df.columns
        or "Se outro fluido refrigerante, especificar" in df.columns
    ):
        df_result["Fluido_refrigerante"] = df["Fluido Refrigerante"].combine_first(
            df["Se outro fluido refrigerante, especificar"]
        )
    elif "Fluido refrigerante" in df.columns:
        df_result["Fluido_refrigerante"] = df["Fluido refrigerante"]
    else:
        df_result["Fluido_refrigerante"] = None

    return df_result


dfs = [
    ("Aquecedores de Água", df_aquecedores_de_agua),
    ("Condicionadores de Ar", df_condicionadores_de_ar),
    ("Fogões", df_fogoes),
    ("Forno Microondas", df_forno_microondas),
    ("Máquina de Lavar Roupa", df_maqina_de_lavar_roupa),
    ("Refrigeradores", df_refrigeradores),
    ("Televisores", df_televisores),
]

df_final = pd.concat(
    [transform_dataframe(df, origem) for origem, df in dfs], ignore_index=True
)
df_final.head()
df_final[["Consumo_energia_mensal_kWh", "Consumo_agua_mensal_l"]] = (
    df_final[["Consumo_energia_mensal_kWh", "Consumo_agua_mensal_l"]]
    .astype(float)
    .round(2)
    .fillna("-")
    .astype(str)
)

df_final = df_final.fillna("-")

df_filtrado = df_final[
    ~(
        (df_final["Classificacao_energetica"] == "-")
        & (df_final["Tipo_gas"] == "-")
        & (df_final["Consumo_agua_mensal_l"] == "-")
        & (df_final["Consumo_energia_mensal_kWh"] == "-")
        & (df_final["Fluido_refrigerante"] == "-")
    )
]

df_filtrado.to_excel("BASE_FINAL.xlsx", index=False)
