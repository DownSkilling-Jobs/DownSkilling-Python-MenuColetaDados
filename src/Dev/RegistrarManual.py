import pandas as pd
import datetime as dt
import regex as re

dados = pd.read_csv('src/Data/Data2.csv')
today = dt.date.today()

def registrar_gasto(tipo, data_emissao, fornecedor, data_pagamento, nNF, valor, valor_icms, valor_cofins, valor_pis, valor_ipi):
    novo_gasto = {
        'Tipo': tipo,
        'Data de emissão': data_emissao,
        'Fornecedor': fornecedor,
        'Data de Vencimento': data_pagamento,
        'N° da NF': nNF,
        'V. Total da NF': valor,
        'ICMS': valor_icms,
        'COFINS': valor_cofins,
        'PIS': valor_pis,
        'IPI': valor_ipi
    }
    global dados
    dados = pd.concat([dados, pd.DataFrame([novo_gasto])], ignore_index=True)
    dados.to_csv('src/Data/Data2.csv', index=False)
    print("Gasto registrado com sucesso!")

def input_valor_monetario(prompt):
    valor_str = 'valor'
    while True and valor_str != '':
        valor_str = input(prompt).replace(',', '.')
        if re.match(r'^\d+(\.\d{1,2})?$', valor_str):
            return float(valor_str)
        else:
            print("Valor inválido. Por favor, insira um valor monetário válido (ex: 1234.56). Ou aperte Enter para sair.")
    
    return ''

def registro_manual(tipo):
    print(f"\nRegistrando gasto do tipo: {tipo}")
    fornecedor = input("Fornecedor: ")
    data_emissao = input("Data de emissão (AAAA-MM-DD): ")
    data_pagamento = input("Data de Vencimento (AAAA-MM-DD): ")
    nNF = int(input("N° da NF: "))
    valor = input_valor_monetario("V. Total da NF: R$ ")
    if valor == '':
        print("Registro cancelado.")
        return
    valor_icms = input_valor_monetario("ICMS: R$ ")
    if valor_icms == '':
        print("Registro cancelado.")
        return
    valor_cofins = input_valor_monetario("COFINS: R$ ")
    if valor_cofins == '':
        print("Registro cancelado.")
        return
    valor_pis = input_valor_monetario("PIS: R$ ")
    if valor_pis == '':
        print("Registro cancelado.")
        return
    valor_ipi = input_valor_monetario("IPI: R$ ")
    if valor_ipi == '':
        print("Registro cancelado.")
        return

    registrar_gasto(tipo, data_emissao, fornecedor, data_pagamento, nNF, valor, valor_icms, valor_cofins, valor_pis, valor_ipi)

if __name__ == "__main__":
    registro_manual('D')