# %% [markdown]
# # Menu Controle de Despesas

# %%
from openpyxl.utils.dataframe import dataframe_to_rows
import xml.etree.ElementTree as ET
import datetime as dt
import openpyxl as xl
import pandas as pd
import regex as re
import time
import os


# %% [markdown]
# ### titulos

# %%
## Titulos do menu

titulo_empresa = """
 ██████████                                                               
▒▒███▒▒▒▒▒█                                                               
 ▒███  █ ▒  █████████████   ████████  ████████   ██████   █████   ██████  
 ▒██████   ▒▒███▒▒███▒▒███ ▒▒███▒▒███▒▒███▒▒███ ███▒▒███ ███▒▒   ▒▒▒▒▒███ 
 ▒███▒▒█    ▒███ ▒███ ▒███  ▒███ ▒███ ▒███ ▒▒▒ ▒███████ ▒▒█████   ███████ 
 ▒███ ▒   █ ▒███ ▒███ ▒███  ▒███ ▒███ ▒███     ▒███▒▒▒   ▒▒▒▒███ ███▒▒███ 
 ██████████ █████▒███ █████ ▒███████  █████    ▒▒██████  ██████ ▒▒████████
▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒ ▒▒▒ ▒▒▒▒▒  ▒███▒▒▒  ▒▒▒▒▒      ▒▒▒▒▒▒  ▒▒▒▒▒▒   ▒▒▒▒▒▒▒▒ 
                            ▒███                                          
                            █████                                         
                           ▒▒▒▒▒      
"""

registrar_titulo = '''
▀██▀▀█▄                    ██           ▄                           
 ██   ██    ▄▄▄▄    ▄▄▄ ▄ ▄▄▄   ▄▄▄▄  ▄██▄  ▄▄▄ ▄▄   ▄▄▄▄   ▄▄▄ ▄▄  
 ██▀▀█▀   ▄█▄▄▄██  ██ ██   ██  ██▄ ▀   ██    ██▀ ▀▀ ▀▀ ▄██   ██▀ ▀▀ 
 ██   █▄  ██        █▀▀    ██  ▄ ▀█▄▄  ██    ██     ▄█▀ ██   ██     
▄██▄  ▀█▀  ▀█▄▄▄▀  ▀████▄ ▄██▄ █▀▄▄█▀  ▀█▄▀ ▄██▄    ▀█▄▄▀█▀ ▄██▄    
                  ▄█▄▄▄▄▀                                           
                                                                                                                              
'''

visualizar_titulo = '''
▀██▀  ▀█▀  ██                          ▀██   ██                          
 ▀█▄  ▄▀  ▄▄▄   ▄▄▄▄  ▄▄▄ ▄▄▄   ▄▄▄▄    ██  ▄▄▄  ▄▄▄▄▄▄   ▄▄▄▄   ▄▄▄ ▄▄  
  ██  █    ██  ██▄ ▀   ██  ██  ▀▀ ▄██   ██   ██  ▀  ▄█▀  ▀▀ ▄██   ██▀ ▀▀ 
   ███     ██  ▄ ▀█▄▄  ██  ██  ▄█▀ ██   ██   ██   ▄█▀    ▄█▀ ██   ██     
    █     ▄██▄ █▀▄▄█▀  ▀█▄▄▀█▄ ▀█▄▄▀█▀ ▄██▄ ▄██▄ ██▄▄▄▄█ ▀█▄▄▀█▀ ▄██▄    
                                                              
'''

alterar_titulo = '''
    █     ▀██    ▄                                   
   ███     ██  ▄██▄    ▄▄▄▄  ▄▄▄ ▄▄   ▄▄▄▄   ▄▄▄ ▄▄  
  █  ██    ██   ██   ▄█▄▄▄██  ██▀ ▀▀ ▀▀ ▄██   ██▀ ▀▀ 
 ▄▀▀▀▀█▄   ██   ██   ██       ██     ▄█▀ ██   ██     
▄█▄  ▄██▄ ▄██▄  ▀█▄▀  ▀█▄▄▄▀ ▄██▄    ▀█▄▄▀█▀ ▄██▄    
                                                                                                    
'''

# %% [markdown]
# ## Variaveis globais
# 

# %%
## Variaveis globais

debug = True
TabList = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
today = dt.date.today()
current_month_index = today.month - 1
dados = pd.DataFrame()
tag_padrao = '{http://www.portalfiscal.inf.br/nfe}'

csv_file = './src/Data/Dados.csv'
excel_file = './src/template/DM-2025 - Template.xlsx'
if debug:
    save_csv_file = 'src/Data/Dados_Debug.csv'
else:
    save_csv_file = './src/Data/Dados.csv'
output_file = os.path.join(os.path.expanduser('~'), 'Downloads', f'Gastos-{today.year}-{today.month:02d}.xlsx')

# %% [markdown]
# ### Carregar Dados

# %%
def carregar_dados():
    '''
    Carrega os dados do arquivo CSV para o DataFrame pandas em uma variavel global
    '''
    global dados
    dados = pd.read_csv(csv_file)

# %% [markdown]
# ## Menu Inicial

# %%
def exibir_titulo(texto):
    '''Exibe o titulo estilizado na tela'''
    os.system('cls')
    print(texto)

def finalizar_app():
    '''Exibe mensagem de finalizacao do app'''
    exibir_subtitulo('Finalizando app')

def voltar_ao_menu_principal():
    '''
    Solicita uma tecla e retorna ao menu principal
        
    Outputs:
    - Retorna ao menu principal
    '''
    input('\nDigite uma tecla para voltar ao menu ')
    main_menu()

def opcao_invalida():
    '''Case o usuario insira um input invalido, retorne ele ao menu principal
    
    Outputs:
    - Retorna ao menu principal
    '''
    print('Input inválido! Retornando ao menu...')
    voltar_ao_menu_principal()

def exibir_subtitulo(texto):
    '''Limpa a tela e exibe o subtitulo estilizado na tela
    
    Inputs:
    - texto: str - o texto do subtitulo
    '''
    os.system('cls')
    linha = '*' * (len(texto))
    print(linha)
    print(texto)
    print(linha)
    print()

# %% [markdown]
# ## Paginacao

# %%

def exibir_pagina(tabela, numero, max):
    '''
    Exibe ao usuario parte da lista de jogadoras, baseado no numero inserido (numero da pagina).
    Caso o ultimo index a ser exibido passe do valor maximo de jogadora registradas, o ultimo index é alterado para o limite.
    '''
    num_min = (numero - 1) * 10
    num_max = num_min + 10
    if num_max > max:
        num_max = max
    print(tabela[num_min:num_max])

def converter_input_numero_pagina(input_numero_pagina):
    '''
    Converte o input do usuario para um numero inteiro.
    Caso o input seja vazio ou invalido, retorna None
    '''
    try:
        input_numero_pagina = int(input_numero_pagina)
        return input_numero_pagina
    except:
        return None

def paginacao(tabela, subtitulo=str):
    '''
    Função que implementa a paginação para exibir a tabela em partes para o usuario.
    Inputs:
    - tabela: pd.DataFrame - a tabela de dados a ser exibida
    - subtitulo: str - o texto do subtitulo a ser exibido
    Outputs:
    - Exibe a tabela paginada na tela de forma interativa
    '''
    exibir_subtitulo(subtitulo)
    
    input_numero_pagina = 1
    pagina_max = len(tabela)
    numero_de_paginas = int(((pagina_max - 1)/10)+1)

    exibir_pagina(tabela, input_numero_pagina, pagina_max)
    print(f"\n-----------! Numeor de paginas: {numero_de_paginas} !----------")
    
    input_numero_pagina = converter_input_numero_pagina(input("\nInsira o numero da pagina que deseja visualizar ou pressione enter para sair: "))
    
    while isinstance(input_numero_pagina, int):
        if isinstance(input_numero_pagina, int):
            if 1 <= input_numero_pagina <= numero_de_paginas:
                exibir_subtitulo(subtitulo)
                exibir_pagina(tabela, input_numero_pagina, pagina_max)
                print(f"\n-----------! Numero de paginas: {numero_de_paginas} !----------")
                input_numero_pagina = converter_input_numero_pagina(input("\nInsira o numero da pagina que deseja visualizar ou pressione enter para sair: "))
            else:
                exibir_subtitulo(subtitulo)
                print("Numero de pagina inserido invalido.")
                print(f"\n-----------! Numero de paginas: {numero_de_paginas} !----------")
                input_numero_pagina = converter_input_numero_pagina(input("\nInsira o numero da pagina que deseja visualizar ou pressione enter para sair: "))
        else:
            print("\nRetornando ao menu principal...\n")
            voltar_ao_menu_principal()
    

# %% [markdown]
# # Menus

# %% [markdown]
# ## Registrar

# %%
# Padrões de regex para validação de datas

regex_pattern_date01 = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'
regex_pattern_date04 = r'[0-9]{4}/[0-9]{2}/[0-9]{2}'
regex_pattern_date02 = r'[0-9]{2}/[0-9]{2}/[0-9]{4}'
regex_pattern_date03 = r'[0-9]{2}-[0-9]{2}-[0-9]{4}'

# Dicionario para converter o valor retornado por weekday() em dia da semana em portugues
dias_da_semana = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

def request_date(texto):
    '''
    Solicita ao usuario uma data e valida se a data é valida. 
    Requisita que a data seja inserida no formato AAAA-MM-DD, porém aceita outros formatos comuns.
    Inputs:
    - texto: str - o texto a ser exibido na solicitacao da data
    Outputs:
    - data: date - a data inserida pelo usuario, ou None se o usuario optar por sair
    '''
    date_input = input(f"Insira a data de {texto} (no formato AAAA-MM-DD): ")

    try:
        if re.fullmatch(regex_pattern_date01, date_input):
            print(f"Data '{date_input}' está no formato AAAA-MM-DD.")
            data = dt.datetime.strptime(date_input, "%Y-%m-%d").date()
        elif re.fullmatch(regex_pattern_date04, date_input):
            print(f"Data '{date_input}' está no formato AAAA/MM/DD.")
            data = dt.datetime.strptime(date_input, "%Y/%m/%d").date()
        elif re.fullmatch(regex_pattern_date02, date_input):
            print(f"Data '{date_input}' está no formato DD/MM/AAAA.")
            data = dt.datetime.strptime(date_input, "%d/%m/%Y").date()
        elif re.fullmatch(regex_pattern_date03, date_input):
            print(f"Data '{date_input}' está no formato DD-MM-AAAA.")
            data = dt.datetime.strptime(date_input, "%d-%m-%Y").date()
        elif date_input == '':
            return None
        else:
            print("Valor inserido Invalido. Tente novamente.\n")
            return request_date(texto)
    except ValueError as e:
        print('Valor inserido invalido. Tente novamente.\n')
        print(f"Error parsing date: {e}")
        if date_input != '':
            return request_date(texto)
        else:
            return None
    else:
        if debug:
            weekday = dias_da_semana[data.weekday()]
            print(f"DEBUG: O dia da semana é: {weekday}")
        return data

# %%
def registrar_gasto(tipo, data_emissao, fornecedor, data_pagamento, nNF, valor, valor_icms, valor_cofins, valor_pis, valor_ipi):
    '''
    Registra um novo gasto no DataFrame e salva no arquivo CSV
    Se debug estiver ativo, as mudanças são salvas em um arquivo separado para debug
    
    '''
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
    dados.to_csv(save_csv_file, index=False)
    print("Gasto registrado com sucesso!")

def input_valor_monetario(prompt):
    '''
    Solicita ao usuario um valor monetario e valida se o valor é valido.
    Aceita valores com até duas casas decimais e permite o uso de vírgula como separador decimal.
    Inputs:
    - prompt: str - o texto a ser exibido na solicitacao do valor
    Outputs:
    - valor: float - o valor monetario inserido pelo usuario, ou '' se o usuario optar por sair
    '''
    valor_str = 'valor'
    while True and valor_str != '':
        valor_str = input(prompt).replace(',', '.')
        if re.match(r'^\d+(\.\d{1,2})?$', valor_str):
            return float(valor_str)
        else:
            print("Valor inválido. Por favor, insira um valor monetário válido (ex: 1234.56). Ou aperte Enter para sair.")
    
    return ''

def registro_manual(tipo):
    '''
    Registra um gasto manualmente solicitando os dados ao usuario.
    Inputs:
    - tipo: str - o tipo do gasto a ser registrado (C, D ou S)
    '''
    tipo = tipo.upper()
    print(f"\nRegistrando gasto do tipo: {tipo}")
    fornecedor = input("Fornecedor: ")
    if fornecedor == '':
        print("Registro cancelado.")
        return
    data_emissao = request_date("Emissão")
    if data_emissao is None:
        print("Registro cancelado.")
        return
    data_pagamento = request_date("Vencimento")
    if data_pagamento is None:
        print("Registro cancelado.")
        return
    try:
        nNF = int(input("N° da NF: "))
    except ValueError:
        print("Número da NF inválido. Registro cancelado.")
        return
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

# %%
def registro_automatico():
    '''
    Registra gastos automaticamente verificando todos os arquivos XML na pasta ./src/Data/xml
    Iterando um por um, a função extrai os dados necessarios e registra o gasto no DataFrame.
    Após salva os gastos no arquivo CSV. (Se debug estiver ativo, salva em um arquivo separado)
    '''
    for file in os.listdir('./src/Data/xml'):
        if file.endswith('.xml'):
            caminho_arquivo = os.path.join('./src/Data/xml', file)
            tree = ET.parse(caminho_arquivo)
            root = tree.getroot()
            base = root.find(f'{tag_padrao}NFe').find(f'{tag_padrao}infNFe')

            tipo = 'C'
            dataE = base.find(f'{tag_padrao}ide').find(f'{tag_padrao}dhEmi').text
            dataE = dataE.split('T')[0]
            fornecedor = base.find(f'{tag_padrao}emit').find(f'{tag_padrao}xNome').text
            if base.find(f'{tag_padrao}cobr') is None:
                dataV = dataE
            else:
                dataV = base.find(f'{tag_padrao}cobr').find(f'{tag_padrao}dup').find(f'{tag_padrao}dVenc').text
            nNF = int(base.find(f'{tag_padrao}ide').find(f'{tag_padrao}nNF').text)
            valor_total = float(base.find(f'{tag_padrao}total').find(f'{tag_padrao}ICMSTot').find(f'{tag_padrao}vNF').text)
            valor_icms = float(base.find(f'{tag_padrao}total').find(f'{tag_padrao}ICMSTot').find(f'{tag_padrao}vICMS').text)
            valor_cofins = float(base.find(f'{tag_padrao}total').find(f'{tag_padrao}ICMSTot').find(f'{tag_padrao}vCOFINS').text)
            valor_pis = float(base.find(f'{tag_padrao}total').find(f'{tag_padrao}ICMSTot').find(f'{tag_padrao}vPIS').text)
            valor_ipi = float(base.find(f'{tag_padrao}total').find(f'{tag_padrao}ICMSTot').find(f'{tag_padrao}vIPI').text)

            print(f'Arquivo: {file} -> Nota Fiscal: {nNF} - Fornecedor: {fornecedor} - Valor Total: {valor_total}')

            registrar_gasto(tipo, dataE, fornecedor, dataV, nNF, valor_total, valor_icms, valor_cofins, valor_pis, valor_ipi)

    print('\nRegistro automatico finalizado.')



# %%
def exibir_opcoes_registrar():
    '''Exibe todas as opcoes de input do usuario do menu registrar dados'''
    print('1. Compras - Registro Automatico - via Arquivos XML')
    print('2. Despesas - Registro Manual')
    print('3. Servicos - Registro Manual')
    print('9. Voltar ao menu Principal\n')

def escolher_opcao_registrar():
    ''' Solicita a executa a opcao escolhida pelo usuario
    
    Outputs:
    -Executa a opcao escolhida pelo usuario
    '''
    try:
        opcao_escolhida = int(input('Escolha uma opção: '))
        # opcao_escolhida = int(opcao_escolhida)

        if opcao_escolhida == 1: 
            registro_automatico()
            input('\nDigite uma tecla para voltar ao menu ')
            menu_registrar_dados()
        elif opcao_escolhida == 2: 
            registro_manual('D')
            input('\nDigite uma tecla para voltar ao menu ')
            menu_registrar_dados()
        elif opcao_escolhida == 3: 
            registro_manual('S')
            input('\nDigite uma tecla para voltar ao menu ')
            menu_registrar_dados()
        elif opcao_escolhida == 9: 
            voltar_ao_menu_principal()
        else: 
            opcao_invalida()
    except Exception as e:
        if debug:
            print(f'Error: {type(e).__name__}')
            print(f"Error message: {e}")
        opcao_invalida()

def menu_registrar_dados():
    '''Menu para registrar dados de jogadoras'''
    exibir_titulo(registrar_titulo)
    exibir_opcoes_registrar()
    escolher_opcao_registrar()

# %% [markdown]
# ## Visualizar

# %%
def visualizar_dados():
    '''
    Lista dados registrados ao usuario usando a função de paginação
    
    Outputs:
    - Exibe lista de dados na tela
    
    '''
    global dados

    paginacao(dados, "Lista de Gastos")

    input('\nDigite uma tecla para voltar ao menu ')
    menu_visualizar_dados()

# %%
def salvar_dados_em_excel(excel_file, output_file):
    '''
    Salva os dados em uma planilha Excel 'template' existente,
    aplicando estilos e formatos específicos para valores monetários.
    Inputs:
    - excel_file: str - caminho para o arquivo Excel 'template' existente
    - output_file: str - caminho para salvar o arquivo Excel atualizado
    '''
    # Carrega a planilha Excel 'template' existente
    workbook = xl.load_workbook(excel_file)
    sheet = workbook[TabList[current_month_index]]

    # Define o estilo padrão para as células que serão preenchidas
    style = xl.styles.NamedStyle(name="standard_style")
    style.font = xl.styles.Font(name='Aptos', size=11)
    style.alignment = xl.styles.Alignment(horizontal='center', vertical='center')
    style.border = xl.styles.Border(
        left=xl.styles.Side(border_style='medium', color='000000'),
        right=xl.styles.Side(border_style='medium', color='000000'),
        top=xl.styles.Side(border_style='none', color='000000'),
        bottom=xl.styles.Side(border_style='none', color='000000')
    )
    workbook.add_named_style(style)

    global dados

    # Coloca os dados do DataFrame na planilha Excel
    for r in dataframe_to_rows(dados, index=False, header=False):
        if 'current_row' not in locals():
            current_row = 3
        for col_idx, value in enumerate(r, start=1):
            sheet.cell(row=current_row, column=col_idx, value=value)
            sheet.cell(row=current_row, column=col_idx).style = "standard_style"
            if col_idx in [ 5, 7, 8, 9, 10 ]:  # Colunas monetárias
                sheet.cell(row=current_row, column=col_idx).number_format = 'R$ #,##0.00'
            
        current_row += 1

    # Muda a aba ativa para a do mes atual
    workbook.active = workbook[TabList[current_month_index]]
    # Salva o arquivo Excel atualizado
    workbook.save(output_file)

# %%
def salvar_arquivo_excel():
    '''
    Salva o arquivo excel com os dados coletados
    (Um timer foi adicionado para garantir que a notificação ao usuario de falha ou sucesso esteja correta)
    '''
    try:
        salvar_dados_em_excel(excel_file, output_file)
    except Exception as e:
        print(f'Erro ao salvar: {e}')
        voltar_ao_menu_principal()
        return

    timeout = 2.0      # segundos máximos para esperar
    interval = 0.2     # intervalo entre checagens
    waited = 0.0
    while not os.path.isfile(output_file) and waited < timeout:
        time.sleep(interval)
        waited += interval

    if os.path.isfile(output_file):
        print(f'Arquivo salvo com sucesso em na pasta de Downloads como: {os.path.basename(output_file)}')
    else:
        print('Erro ao salvar o arquivo. Feche o Excel e tente novamente.')

    input('\nDigite uma tecla para voltar ao menu ')
    menu_visualizar_dados()

# %%
def filtrar_dados(tipo=None):
    '''
    Filtra os dados com base no tipo fornecido.
    Inputs:
    - tipo: str ou None - o tipo de dado a ser filtrado. Se None, retorna todos os dados.
    Outputs:
    - pd.DataFrame - a tabela filtrada
    '''
    global dados
    df_filtrado = dados.copy()

    if tipo:
        df_filtrado = df_filtrado[df_filtrado['Tipo'].str.contains(tipo, case=False, na=False)]

    return df_filtrado

# %%
def visualizar_por_categoria():
    '''
    Visualiza os dados filtrados por categoria
    Utilizando a função paginação para exibir apenas 10 linhas por vez
    '''
    tipo = input('Insira o tipo de despesa (C para Compras, D para Despesas, S para Serviços): ').strip().upper()
    if tipo not in ['C', 'D', 'S']:
        print('Tipo inválido. Retornando ao menu principal.')
        voltar_ao_menu_principal()
        return
    dados_filtrados = filtrar_dados(tipo=tipo)
    paginacao(dados_filtrados, f"Dados Filtrados por Tipo: {tipo}")
    
    input('\nDigite uma tecla para voltar ao menu ')
    menu_visualizar_dados()

# %%
def exibir_opcoes_visualizar():
    '''Exibe todas as opcoes de input do usuario do menu visualizar dados'''
    print('1. Visualizar todos os dados')
    print('2. Visualizar por Categorias')
    print('3. Salvar Arquivo Excel')
    print('9. Voltar ao menu Principal\n')
    
def escolher_opcao_visualizar():
    ''' Solicita a executa a opcao escolhida pelo usuario
    
    Outputs:
    -Executa a opcao escolhida pelo usuario
    '''
    try:
        opcao_escolhida = int(input('Escolha uma opção: '))
        # opcao_escolhida = int(opcao_escolhida)

        if opcao_escolhida == 1: 
            visualizar_dados()
        elif opcao_escolhida == 2: 
            visualizar_por_categoria()
        elif opcao_escolhida == 3: 
            salvar_arquivo_excel()
        elif opcao_escolhida == 9: 
            voltar_ao_menu_principal()
        else: 
            opcao_invalida()
    except Exception as e:
        if debug:
            print(f'Error: {type(e).__name__}')
            print(f"Error message: {e}")
        opcao_invalida()

def menu_visualizar_dados():
    '''Menu para registrar dados de jogadoras'''
    exibir_titulo(visualizar_titulo)
    exibir_opcoes_visualizar()
    escolher_opcao_visualizar()

# %% [markdown]
# ## Alterar

# %%
def alterar_dados(indice):
    '''
    Altera os dados de um gasto especificado pelo indice no DataFrame e salva no arquivo CSV
    Função re-utilizada em todas as funções de alteração de dados
    
    Inputs:
    - indice: int - o índice do gasto a ser alterado
    '''

    global dados
    global save_csv_file
    novo_fornecedor = input(f"Fornecedor atual ({dados.at[indice, 'Fornecedor']}), novo valor (pressione Enter para manter): ")
    if novo_fornecedor:
        dados.at[indice, 'Fornecedor'] = novo_fornecedor

    nova_data_emissao = request_date("Emissão (pressione Enter para manter)")
    if nova_data_emissao:
        dados.at[indice, 'Data de emissão'] = nova_data_emissao

    nova_data_pagamento = request_date("Vencimento (pressione Enter para manter)")
    if nova_data_pagamento:
        dados.at[indice, 'Data de Vencimento'] = nova_data_pagamento

    novo_valor = input_valor_monetario(f"V. Total da NF atual (R$ {dados.at[indice, 'V. Total da NF']}), novo valor (pressione Enter para manter): R$ ")
    if novo_valor != '':
        dados.at[indice, 'V. Total da NF'] = novo_valor

    novo_valor_icms = input_valor_monetario(f"ICMS atual (R$ {dados.at[indice, 'ICMS']}), novo valor (pressione Enter para manter): R$ ")
    if novo_valor_icms != '':
        dados.at[indice, 'ICMS'] = novo_valor_icms

    novo_valor_cofins = input_valor_monetario(f"COFINS atual (R$ {dados.at[indice, 'COFINS']}), novo valor (pressione Enter para manter): R$ ")
    if novo_valor_cofins != '':
        dados.at[indice, 'COFINS'] = novo_valor_cofins

    novo_valor_pis = input_valor_monetario(f"PIS atual (R$ {dados.at[indice, 'PIS']}), novo valor (pressione Enter para manter): R$ ")
    if novo_valor_pis != '':
        dados.at[indice, 'PIS'] = novo_valor_pis

    novo_valor_ipi = input_valor_monetario(f"IPI atual (R$ {dados.at[indice, 'IPI']}), novo valor (pressione Enter para manter): R$ ")
    if novo_valor_ipi != '':
        dados.at[indice, 'IPI'] = novo_valor_ipi

        if novo_fornecedor or nova_data_emissao or nova_data_pagamento or novo_valor != '' or novo_valor_icms != '' or novo_valor_cofins != '' or novo_valor_pis != '' or novo_valor_ipi != '':
            dados.to_csv(save_csv_file, index=False)
            print("Dados alterados com sucesso!")
        else:
            print("Nenhum dado foi alterado.")


# %%
def alterar_por_nNF():
    '''
    Altera os dados de uma despesa baseado no N° da NF
    Se o N° da NF for duplicado, solicita o indice do registro a ser alterado
    Após alterar os dados, salva no arquivo CSV (ou arquivo de debug se debug estiver ativo)
    '''

    exibir_subtitulo("Alterar registro por N° da NF")
    nNF_input = input("Insira o N° da NF que deseja alterar: ")
    try:
        nNF_input = int(nNF_input)
    except ValueError:
        print("Número da NF inválido. Retornando ao menu...")
        menu_alterar_dados()
        return

    global dados
    if nNF_input not in dados['N° da NF'].values:
        print(f"Número da NF {nNF_input} não encontrado. Retornando ao menu...")
        menu_alterar_dados()
        return
    elif len(dados[dados['N° da NF'] == nNF_input]) > 1:
        print(f"Mais de um registro encontrado para a NF {nNF_input}.\n")
        print(dados[dados['N° da NF'] == nNF_input])
        indice = input("Insira o índice do registro que deseja apagar (conforme exibido acima): ")
        try:
            indice = int(indice)
            if indice not in dados.index:
                print("Índice inválido. Retornando ao menu...")
                menu_alterar_dados()
                return
        except ValueError:
            print("Valor inserido inválido. Retornando ao menu...")
            menu_alterar_dados()
            return
    else:
        indice = dados.index[dados['N° da NF'] == nNF_input][0]

    print(f"Alterando dados para a NF {nNF_input}:")
    
    # Chama a função de alterar dados
    alterar_dados(indice)
    
    input('\nDigite uma tecla para voltar ao menu.')
    menu_alterar_dados()



# %%
def alterar_por_data_emissao():
    '''
    Altera os dados de uma despesa baseado na Data de Emissão
    Após receber a data de emissão, exibe todos os registros encontrados
    Solicita o N° da NF para identificar o registro a ser alterado
    '''

    exibir_subtitulo("Alterar registro por Data de Emissão")
    
    data_emissao = request_date("Emissão para busca")
    if data_emissao is None:
        print("Data inválida. Retornando ao menu...")
        menu_alterar_dados()
        return

    global dados
    dados_filtrados = dados[dados['Data de emissão'] == str(data_emissao)]

    if dados_filtrados.empty:
        print(f"Nenhum registro encontrado para a data de emissão {data_emissao}. Retornando ao menu...")
        menu_alterar_dados()
        return

    print(f"Registros encontrados para a data de emissão {data_emissao}:")
    print(dados_filtrados)

    nNF_input = input("Insira o N° da NF que deseja alterar: ")
    try:
        nNF_input = int(nNF_input)
    except ValueError:
        print("Valor inserido inválido. Retornando ao menu...")
        menu_alterar_dados()
        return

    if nNF_input not in dados_filtrados['N° da NF'].values:
        print(f"Número da NF {nNF_input} não encontrado na data de emissão {data_emissao}. Retornando ao menu...")
        menu_alterar_dados()
        return

    indice = dados.index[dados['N° da NF'] == nNF_input][0]
    print(f"Alterando dados para a NF {nNF_input}:")
    
    alterar_dados(indice)
    
    input('\nDigite uma tecla para voltar ao menu.')
    menu_alterar_dados()

# %%
def alterar_por_fornecedor():
    '''
    Altera os dados de uma despesa baseado no Fornecedor
    Após receber o nome do fornecedor, exibe todos os registros encontrados
    Solicita o N° da NF para identificar o registro a ser alterado
    '''

    exibir_subtitulo("Alterar dados por Fornecedor")

    fornecedor_input = input("Insira o nome do Fornecedor que deseja alterar: ").strip()
    if not fornecedor_input:
        print("Valor inválido. Retornando ao menu...")
        menu_alterar_dados()
        return

    global dados
    dados_filtrados = dados[dados['Fornecedor'].str.contains(fornecedor_input, case=False, na=False)]

    if dados_filtrados.empty:
        print(f"Nenhum registro encontrado para o fornecedor '{fornecedor_input}'. Retornando ao menu...")
        menu_alterar_dados()
        return

    print(f"Registros encontrados para o fornecedor '{fornecedor_input}':")
    print(dados_filtrados)

    nNF_input = input("Insira o N° da NF que deseja alterar: ")
    try:
        nNF_input = int(nNF_input)
    except ValueError:
        print("Número da NF inválido. Retornando ao menu...")
        menu_alterar_dados()
        return

    if nNF_input not in dados_filtrados['N° da NF'].values:
        print(f"Número da NF {nNF_input} não encontrado para o fornecedor '{fornecedor_input}'. Retornando ao menu...")
        menu_alterar_dados()
        return

    indice = dados.index[dados['N° da NF'] == nNF_input][0]
    print(f"Alterando dados para a NF {nNF_input}:")
    
    alterar_dados(indice)
    
    input('\nDigite uma tecla para voltar ao menu.')
    menu_alterar_dados()

# %%
def alterar_por_data_vencimento():
    '''
    Altera uma despesa baseado na Data de Vencimento
    Após receber a data de vencimento, exibe todos os registros encontrados
    Solicita o N° da NF para identificar o registro a ser alterado
    '''
    
    exibir_subtitulo("Alterar registro por Data de Vencimento")

    data_vencimento = request_date("Vencimento para busca")
    if data_vencimento is None:
        print("Data inválida. Retornando ao menu...")
        menu_alterar_dados()
        return

    global dados
    dados_filtrados = dados[dados['Data de Vencimento'] == str(data_vencimento)]

    if dados_filtrados.empty:
        print(f"Nenhum registro encontrado para a data de vencimento {data_vencimento}. Retornando ao menu...")
        menu_alterar_dados()
        return

    print(f"Registros encontrados para a data de vencimento {data_vencimento}:")
    print(dados_filtrados)

    nNF_input = input("Insira o N° da NF que deseja alterar: ")
    try:
        nNF_input = int(nNF_input)
    except ValueError:
        print("Número da NF inválido. Retornando ao menu...")
        menu_alterar_dados()
        return

    if nNF_input not in dados_filtrados['N° da NF'].values:
        print(f"Número da NF {nNF_input} não encontrado na data de vencimento {data_vencimento}. Retornando ao menu...")
        menu_alterar_dados()
        return

    indice = dados.index[dados['N° da NF'] == nNF_input][0]
    print(f"Alterando dados para a NF {nNF_input}:")
    
    alterar_dados(indice)
    
    input('\nDigite uma tecla para voltar ao menu.')
    menu_alterar_dados()

# %%
def apagar_por_nNF():
    '''
    Apaga os dados de uma despesa baseado no N° da NF
    Após receber o N° da NF, exibe todos os registros encontrados
    Solicita o índice para identificar o registro a ser apagado
    Caso apenas um registro seja encontrado, o unico registro é apagado
    Porém antes de apagar, solicita confirmação do usuário
    Após apagar os dados, salva no arquivo CSV (ou arquivo de debug se debug estiver ativo)
    '''

    exibir_subtitulo("Apagar registro por N° da NF")

    nNF_input = input("Insira o N° da NF que deseja apagar: ")
    try:
        nNF_input = int(nNF_input)
    except ValueError:
        print("Número da NF inválido. Retornando ao menu...")
        menu_alterar_dados()
        return

    global dados
    if nNF_input not in dados['N° da NF'].values:
        print(f"Número da NF {nNF_input} não encontrado. Retornando ao menu...")
        menu_alterar_dados()
        return
    elif len(dados[dados['N° da NF'] == nNF_input]) > 1:
        print(f"Mais de um registro encontrado para a NF {nNF_input}.\n")
        print(dados[dados['N° da NF'] == nNF_input])
        index = input("Insira o índice do registro que deseja apagar (conforme exibido acima): ")
        try:
            index = int(index)
            if index not in dados.index:
                print("Índice inválido. Retornando ao menu...")
                menu_alterar_dados()
                return
        except ValueError:
            print("Valor inserido inválido. Retornando ao menu...")
            menu_alterar_dados()
            return
    else:
        index = dados.index[dados['N° da NF'] == nNF_input][0]

    confirmacao = input(f"Tem certeza que deseja apagar a NF {nNF_input}? (s/n): ").strip().lower()
    if confirmacao == 's':
        dados = dados.drop(index)
        dados.to_csv(save_csv_file, index=False)
        print("Registro apagado com sucesso!")
    else:
        print("Operação cancelada.")

    input('\nDigite uma tecla para voltar ao menu.')
    menu_alterar_dados()

# %%
def exibir_opcoes_alterar():
    '''Exibe todas as opcoes de input do usuario no menu alterar dados'''
    print('1. Alterar Gastos - Procurar por N° da NF')
    print('2. Alterar Gastos - Procurar por Fornecedor')
    print('3. Alterar Gastos - Procurar por Data de Emissão')
    print('4. Alterar Gastos - Procurar por Data de Vencimento')
    print('5. Apagar Gastos - Procurar por N° da NF')
    print('9. Voltar ao Menu Principal\n')

def escolher_opcao_alterar():
    ''' Solicita a executa a opcao escolhida pelo usuario
    
    Outputs:
    -Executa a opcao escolhida pelo usuario
    '''
    try:
        opcao_escolhida = int(input('Escolha uma opção: '))
        # opcao_escolhida = int(opcao_escolhida)

        if opcao_escolhida == 1: 
            alterar_por_nNF()
        elif opcao_escolhida == 2: 
            alterar_por_fornecedor()
        elif opcao_escolhida == 3: 
            alterar_por_data_emissao()            
        elif opcao_escolhida == 4:
            alterar_por_data_vencimento()
        elif opcao_escolhida == 5:
            apagar_por_nNF()
        elif opcao_escolhida == 9: 
            voltar_ao_menu_principal()
        else: 
            opcao_invalida()
    except Exception as e:
        if debug:
            print(f'Error: {type(e).__name__}')
            print(f"Error message: {e}")
        opcao_invalida()

def menu_alterar_dados():
    '''Menu para alterar dados de jogadoras'''
    os.system('cls')
    exibir_titulo(alterar_titulo)
    exibir_opcoes_alterar()
    escolher_opcao_alterar()

# %% [markdown]
# #### debug

# %%
def alternar_debug():
    '''Alterna o modo debug'''
    global debug
    global save_csv_file
    debug = not debug
    status = 'ativado' if debug else 'desativado'
    exibir_subtitulo('Alterar Modo Debug')
    print(f'\nModo debug {status}.')
    if debug:
        save_csv_file = 'src/Data/Data_Debug.csv'
    else:
        save_csv_file = './src/Data/Dados.csv'
    time.sleep(1)
    voltar_ao_menu_principal()

# %% [markdown]
# ## Principal

# %%
def exibir_opcoes():
    '''Exibe todas as opcoes de input do usuario'''
    print('1. Registrar Custos')
    print('2. Visualizar Despesas')
    print('3. Alterar Dados')
    print('4. Alternar Debug')
    print('9. Sair\n')

def escolher_opcao():
    ''' Solicita a executa a opcao escolhida pelo usuario
    
    Outputs:
    -Executa a opcao escolhida pelo usuario
    '''
    try:
        opcao_escolhida = int(input('Escolha uma opção: '))
        # opcao_escolhida = int(opcao_escolhida)

        if opcao_escolhida == 1: 
            menu_registrar_dados()
        elif opcao_escolhida == 2: 
            menu_visualizar_dados()
        elif opcao_escolhida == 3: 
            menu_alterar_dados()            
        elif opcao_escolhida == 4:
            alternar_debug()
        elif opcao_escolhida == 9: 
            finalizar_app()
        else: 
            opcao_invalida()
    except Exception as e:
        if debug:
            print(f'Error: {type(e).__name__}')
            print(f"Error message: {e}")
        opcao_invalida()

def main_menu():
    '''Funcao principal que inicial o programa'''
    os.system('cls')    
    exibir_titulo(titulo_empresa)
    exibir_opcoes()
    escolher_opcao()


# %% [markdown]
# # Main

# %%
def main():
    '''
    Ponto de entrada do programa
    Carrega os dados ao Dataframe padrão e então exibe o menu ao usuario
    '''
    carregar_dados()
    main_menu()

if __name__ == '__main__':
    main()


