import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text


base_dir = Path(__file__).resolve().parent
pasta_parquet = base_dir / 'Parquet'

# Carrega as variáveis do arquivo somente no .env
load_dotenv(base_dir / '.env')

# --------  Criando conexão  ---------------

conn_mysql = URL.create(
    drivername = 'mysql+mysqlconnector',
    username = os.getenv('MYSQL_USER'),
    password = os.getenv('MYSQL_PASSWORD'),
    host = os.getenv('MYSQL_HOST'),
    port = int(os.getenv('MYSQL_PORT')),
    database = os.getenv('MYSQL_SCHEMA')
)

engine = create_engine(conn_mysql)

def testar_conexao():
    # connect solicita a conexão com o banco
    with engine.connect() as conexao:
        # informa qual o comando em SQL, a função text está ai
        # para informar a engine que é um comando em cadeia de texto
        # e também dessa forma o comando passa por dentro da engine
        # poderia usar o ".exec.driver_sql()" que enviaria a consulta
        # direto para o drive do mysql sem passar pela engine
        resultado = conexao.execute(text('SELECT DATABASE()'))
        print(f'Schema conectado: {resultado.scalar()}')




def ler_product_category():
    arquivo = pasta_parquet / 'product_category_name_translation.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('------ Product Category -------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {list(df.columns)}')
    print(f'Amostra dos dados:')
    print(df.head())

    return df


def tabela_product_category():
    script = text("""
        CREATE TABLE IF NOT EXISTS product_category(
            product_category_name VARCHAR(100) NOT NULL,
            priduct_category_name_english VARCHAR(100) NOT NULL,
            PRIMARY KEY(product_category_name)
        )
    """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela product_category criada ou já existente')




if __name__ == '__main__':
    testar_conexao()
    ler_product_category()
    tabela_product_category()