import pandas as pd

dados = pd.read_csv('src/Data/Data2.csv')

def filtrar_dados(tipo=None, fornecedor=None, data_inicio=None, data_fim=None, valor_minimo=None, valor_maximo=None):
    df_filtrado = dados.copy()

    if tipo:
        df_filtrado = df_filtrado[df_filtrado['Tipo'].str.contains(tipo, case=False, na=False)]

    return df_filtrado

dados_filtrados = filtrar_dados(tipo='S')

dados_filtrados