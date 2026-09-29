import pandas as pd
from pathlib import Path

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
# ou seja, 
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
