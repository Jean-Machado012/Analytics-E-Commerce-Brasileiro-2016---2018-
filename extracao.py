import pandas as pd
from pathlib import Path
import json

# Registrando o caminho desta forma possibilita o repositório ser clonado em qualquer máquina,
# então realizando desta forma, pode-se descartar o uso das bibliotecas "dotenv" e "os", lembrando
# somente para o acesso nesses arquivos...
base_dir =  Path(__file__).resolve().parent
pasta_csv = base_dir / 'CSVs'

# Criando uma lista com o camimho completo de todos os arquivos na pasta
# A função "glob" permite que eu especifique um caminho genérico e leia tudo com uma terminação que eu passar
arquivos = list(pasta_csv.glob('*.csv'))

# ------------------   Realizando tratamento e verificando qualidade dos arquivos --------------------------

# Obs: Caso exista linha, colunas ou registro duplicado, ele será removido
'''
def qualidade_csv():
    def separador_linha():
        print('-'*50)

    # Criando função para ler os arquivos, e analisar a qualidade dos dados
    def verificar_arquivos(caminho):
        df = pd.read_csv(caminho)

        linhas_vazias = df.isna().all(axis = 1).sum()
        colunas_vazias = df.isna().all(axis = 0).sum()
        duplicatas = df.duplicated().sum()

        separador_linha()
        print(f'Nome Arquivo: {caminho.name}')
        print(f'Linhas: {len(df)}')
        print(f'Colunas: {len(df.columns)}')
        print(f'Linhas vazias: {linhas_vazias}')
        print(f'Colunas vazias: {colunas_vazias}')
        print(f'Linhas duplicadas: {duplicatas}')
        print(f'Valores únicos:\n{df.nunique()}')
        print(f'{df.describe()}')
        print(f'Tipos dos dados:\n{df.info()}')

    # Um dicionário onde a chave é o nome do arquivo e o valor são os nomes das colunas de data
    # Procedimento realizado para que no pd.read_csv(), ele consiga ler arquivo por arquivo e achar as colunas corretas dentro do arquivo
    colunas_date = {
        'olist_orders_dataset.csv' : 
        [
        'order_delivered_carrier_date' ,
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
        ],

        'olist_order_items_dataset.csv' : 
        [
        'shipping_limit_date'
        ],

        'olist_order_reviews_dataset.csv' :
        [
        'review_creation_date',
        'review_answer_timestamp'
        ]
    }

    # Esta função ela recebe um arquivo como 1º param e as colunas do 2º param são do dicionário criado acima,
    # ou seja, deste modo é possível passar o cada coluna da lista acima referente a seu arquivo pai
    def analisar_csv(caminho, colunas_date = ''):
        df = pd.read_csv(caminho)

        if colunas_date:
            for coluna in colunas_date:
                df[coluna] = pd.to_datetime(df[coluna])

        print(df.dtypes)

        return df


    for i in arquivos:
        # Com está variavel "datas" pegamos individualmente o nome de cada coluna do dicionario e passamos uma a uma
        datas = colunas_date.get(i.name)
        df = analisar_csv(i, datas)
        verificar_arquivos(i)
'''

# ---------------- Realizando Integração da API Via CEP -------------------

# Por conta do dataset não oferecer o cep completo, apenas o prefixo, irei assumir
# o sufixo do cep como "000", assim ainda mantenho a informação do bairro mas sem 
# enxergar a rua exatamente daquela localização

# Primeiro como são muitos pedidos vamos pegar o prefixos unicos de cep

def gerar_prefixos():
    ceps_prefixo = []
    consulta_cep_prefixo = pd.read_csv(pasta_csv / 'olist_geolocation_dataset.csv')
    # Eliminar os valores nulos e as duplicatas
    df_coluna_cep = consulta_cep_prefixo['geolocation_zip_code_prefix'].dropna().unique()
    # Neste passo é necessário transformar a coluna para string pois ela com o tipo int
    # perde-se o "0" caso seja inicial no número
    df_coluna_cep = df_coluna_cep.astype(str)

    # Para os números que tem apenas 4 caracteres em seu prefixo, como no csv foi tratado como int
    # então é pressuposto com seja zero no incio, e como explicado acima será um geral da região
    # por isso o acréscimo de "000" ao final
    for i in df_coluna_cep:
        ceps_prefixo.append(i)

    # Criando uma nova lista com indice para os prefixos
    lista_prefixos = [
        {
            'indice' : indice,
            'prefixo' : prefixo
        }
        for indice, prefixo in enumerate(ceps_prefixo)
    ]

    #Salvando a lista com indice e prefixos em json
    save_prefixos = base_dir / 'prefixos.json'

    with open(save_prefixos, 'w', encoding = 'utf-8') as arquivo:
        json.dump(lista_prefixos, arquivo, ensure_ascii = False, indent = 4)

    print(f'Total de prefixos salvos: {len(lista_prefixos)}')

    if __name__ == '__main__':
        gerar_prefixos()



def solicitar_api(prefixo):
    import requests
    from requests.exceptions import RequestException
    from time import sleep

    cep = f'{int(prefixo):05d}000'

    url = f'https://viacep.com.br/ws/{cep}/json/'

    consulta_cep_completo = {
        'prefixo' : prefixo,
        'cep' : cep,
        'bairro' : '',
        'estado' : '',
        'regiao' : '',
        'status' : ''
    }

    try:
        request = requests.get(url, timeout = 10)
        sleep(0.5)

        if request.status_code != 200:
            consulta_cep_completo['status'] = f'erro_http_{request.status_code}'
            return consulta_cep_completo

        response = request.json()

    except RequestException as erro:
        print(f'Erro ao consultar CEP: {cep} -> ({erro})')
        consulta_cep_completo['status'] = 'erro_conexao'
        return consulta_cep_completo

    if 'erro' in response:
        print(f'CEP não encontrado: {cep}')
        consulta_cep_completo['status'] = 'não_encontrado'
        return consulta_cep_completo


    consulta_cep_completo['cep'] = response.get('cep', '')
    consulta_cep_completo['bairro'] = response.get('bairro', '')
    consulta_cep_completo['estado'] = response.get('estado', '')
    consulta_cep_completo['regiao'] = response.get('regiao', '')
    consulta_cep_completo['status'] = 'encontrado'


    return consulta_cep_completo
