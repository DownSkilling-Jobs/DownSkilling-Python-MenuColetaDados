# %% [markdown]
# # Menu Controle de Despesas

# %%
import xml.etree.ElementTree as ET
import openpyxl as xl
import pandas as pd
import regex as re
import os


# %% [markdown]
# ### titulos

# %%
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
 ██   ██    ▄▄▄▄    ▄▄▄ ▄ ▄▄▄   ▄▄▄▄  ▄██▄   ▄▄▄▄   ▄▄▄ ▄▄  
 ██▀▀█▀   ▄█▄▄▄██  ██ ██   ██  ██▄ ▀   ██   ▀▀ ▄██   ██▀ ▀▀ 
 ██   █▄  ██        █▀▀    ██  ▄ ▀█▄▄  ██   ▄█▀ ██   ██     
▄██▄  ▀█▀  ▀█▄▄▄▀  ▀████▄ ▄██▄ █▀▄▄█▀  ▀█▄▀ ▀█▄▄▀█▀ ▄██▄    
                  ▄█▄▄▄▄▀                                   
                                                            
'''

visualizar_titulo = '''
▀██▀  ▀█▀  ██                          ▀██   ██                          
 ▀█▄  ▄▀  ▄▄▄   ▄▄▄▄   ▄▄▄▄   ▄▄▄ ▄▄▄   ██  ▄▄▄  ▄▄▄▄▄▄   ▄▄▄▄   ▄▄▄ ▄▄  
  ██  █    ██  ██▄ ▀  ▀▀ ▄██   ██  ██   ██   ██  ▀  ▄█▀  ▀▀ ▄██   ██▀ ▀▀ 
   ███     ██  ▄ ▀█▄▄ ▄█▀ ██   ██  ██   ██   ██   ▄█▀    ▄█▀ ██   ██     
    █     ▄██▄ █▀▄▄█▀ ▀█▄▄▀█▀  ▀█▄▄▀█▄ ▄██▄ ▄██▄ ██▄▄▄▄█ ▀█▄▄▀█▀ ▄██▄                                                                         

'''

alterar_titulo = '''
    █     ▀██    ▄                                   
   ███     ██  ▄██▄    ▄▄▄▄  ▄▄▄ ▄▄   ▄▄▄▄   ▄▄▄ ▄▄  
  █  ██    ██   ██   ▄█▄▄▄██  ██▀ ▀▀ ▀▀ ▄██   ██▀ ▀▀ 
 ▄▀▀▀▀█▄   ██   ██   ██       ██     ▄█▀ ██   ██     
▄█▄  ▄██▄ ▄██▄  ▀█▄▀  ▀█▄▄▄▀ ▄██▄    ▀█▄▄▀█▀ ▄██▄    
                                                     
                                                     
'''

# %%
debug = False

# %% [markdown]
# ## Menu Inicial

# %%
def exibir_titulo(texto):
    '''Exibe o titulo estilizado na tela'''
    os.system('cls')
    print(texto)

def exibir_opcoes():
    '''Exibe todas as opcoes de input do usuario'''
    print('1. Registrar Custos')
    print('2. Visualizar Despesas')
    print('3. Alternar Dados')
    print('4. Salvar Arquivo Excel')
    print('9. Sair\n')

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
    main()

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
    
def listar_jogadoras():
    '''Lista jogadoras registradas no banco de dados
    
    Inputs:
    - Dictionary de jogadoras
    
    Outputs:
    - Exibe lista de jogadoras na tela
    
    '''
    global jogadoras

    paginacao(jogadoras, "Lista de Jogadoras Cadastradas")

    voltar_ao_menu_principal()

# %% [markdown]
# ## Registrar

# %%
def registro_automatico():
    for file in os.listdir('./src/Data/xml'):
        if file.endswith('.xml'):
            caminho_arquivo = os.path.join('./src/Data/xml', file)
            tree = ET.parse(caminho_arquivo)
            root = tree.getroot()
            base = root[0][0]
            # Aqui você pode adicionar o código para processar e registrar os dados do DataFrame

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
        elif opcao_escolhida == 2: 
            registro_despesas()
        elif opcao_escolhida == 3: 
            registro_servicos()
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
def exibir_opcoes_visualizar():
    '''Exibe todas as opcoes de input do usuario do menu registrar dados'''
    print('1. Visualizar todos os dados')
    print('2. Visualizar Compras')
    print('3. Visualizar Despesas')
    print('4. Visualizar Servicos')
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
            visualizar_compras()
        elif opcao_escolhida == 3: 
            visualizar_despesas()
        elif opcao_escolhida == 4: 
            visualizar_servicos()
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

# %%
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
            salvar_arquivo_excel()
        elif opcao_escolhida == 9: 
            finalizar_app()
        else: 
            opcao_invalida()
    except Exception as e:
        if debug:
            print(f'Error: {type(e).__name__}')
            print(f"Error message: {e}")
        opcao_invalida()

def main():
    '''Funcao principal que inicial o programa'''
    os.system('cls')
    exibir_titulo(titulo_empresa)
    exibir_opcoes()
    escolher_opcao()

if __name__ == '__main__':
    main()


