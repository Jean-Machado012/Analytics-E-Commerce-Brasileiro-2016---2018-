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


# ----------------------- TABLE PRODUCT CATEGORY ---------------------------

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


df_product_category = ler_product_category()


def table_product_category():
    script = text("""
        CREATE TABLE IF NOT EXISTS product_category(
            product_category_name VARCHAR(100) NOT NULL,
            product_category_name_english VARCHAR(100) NOT NULL,
            PRIMARY KEY(product_category_name)
        )
    """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela product_category criada ou já existente')



def insert_dados_product_category(df):
    with engine.begin() as conexao:
        df.to_sql(
            name = 'product_category',
            con = conexao,
            if_exists = 'append',
            index = False
        )

    print(f'Registro enviados para product_category: {len(df)} linhas')



# -------------------- TABLE CUSTOMER ------------------------

def ler_customer():
    arquivo = pasta_parquet / 'olist_customers_dataset.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('---------- CUSTOMER ----------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {list(df.columns)}')
    print('Amostra dos dados: ')
    print(df.head())

    return df


df_customers = ler_customer()


def table_customer():
    script = text("""
        CREATE TABLE IF NOT EXISTS customers(
            customer_id VARCHAR(100) NOT NULL,
            customer_unique_id VARCHAR(100) NOT NULL,
            customer_zip_code_prefix INT NOT NULL,
            customer_city VARCHAR(100) NOT NULL,
            customer_state VARCHAR(50) NOT NULL,
            PRIMARY KEY(customer_unique_id, customer_id)
        )
        """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela customer criada ou já existente')


def insert_dados_customers(df):
    with engine.begin() as conexao:
        df.to_sql(
            name = 'customers',
            con = conexao,
            if_exists = 'append',
            index = False
        )

    print(f'Registros enviados para customers: {len(df)} linhas')



# ----------------- TABLE GEOLOCATION -----------------------

def ler_geolocation():
    arquivo = pasta_parquet / 'olist_geolocation_dataset.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('---------- GEOLOCATION ----------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {list(df.columns)}')
    print('Amostra dos dados: ')
    print(df.head())

    return df


df_geolocation = ler_geolocation()

def table_geolocation():
    script = text("""
        CREATE TABLE IF NOT EXISTS geolocation(
            zip_code_prefix INT NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            city VARCHAR(100) NOT NULL,
            state VARCHAR(100) NOT NULL
        )
    """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela geolocation criada ou já existente')



def insert_dados_geolocation(df):

    df = df.rename(columns ={
        'geolocation_zip_code_prefix': 'zip_code_prefix',
        'geolocation_lat': 'latitude',
        'geolocation_lng': 'longitude',
        'geolocation_city': 'city',
        'geolocation_state': 'state'
    })

    with engine.begin() as conexao:
        df.to_sql(
            name = 'geolocation',
            con = conexao,
            if_exists = 'append',
            index = False,
            # O Parametro "chunksize" permite o pandas separar em lotes
            chunksize = 1000
        )

    print(f'Registros enviados para geolocation: {len(df)} linhas')


# -------------- Table Order Item ---------------------

def ler_order_item():
    arquivo = pasta_parquet / 'olist_order_items_dataset.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('---------- ORDER ITEM ----------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {list(df.columns)}')
    print('Amostra dos dados: ')
    print(df.head())

    return df


df_order_items = ler_order_item()


def table_order_items():
    script = text("""
        CREATE TABLE IF NOT EXISTS order_items(
            order_id VARCHAR(100) NOT NULL,
            order_item_id SMALLINT NOT NULL,
            product_id VARCHAR(100) NOT NULL,
            seller_id VARCHAR(100) NOT NULL,
            shipping_limit_date DATETIME NOT NULL,
            price FLOAT(10,2) NOT NULL,
            freight_value FLOAT(10, 2) NOT NULL,
            PRIMARY KEY(order_id, order_item_id)
        )
        """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela order_items criada ou já existente')



def insert_dados_order_items(df):
    with engine.begin() as conexao:
        df.to_sql(
            name = 'order_items',
            con = conexao,
            if_exists = 'append',
            index = False,
            chunksize = 1000
        )

    print(f'Registros enviados para order_items: {len(df)} linhas')



# --------------------- Tabela order_payments ------------------------


def ler_order_payments():
    arquivo = pasta_parquet / 'olist_order_payments_dataset.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('---------- ORDER PAYMENTS ----------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {list(df.columns)}')
    print('Amostra dos dados: ')
    print(df.head())

    return df



df_order_payments = ler_order_payments()


def table_order_payments():
    script = text("""
        CREATE TABLE IF NOT EXISTS order_payments(
            order_id VARCHAR(100) NOT NULL,
            payment_sequential SMALLINT NOT NULL,
            payment_type VARCHAR(50) NOT NULL,
            payment_installments SMALLINT NOT NULL,
            payment_value FLOAT(7,2) NOT NULL,
            PRIMARY KEY(order_id, payment_sequential)
        )
        """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela order_payments criada ou já existente')


def insert_dados_order_payments(df):
    with engine.begin() as conexao:
        df.to_sql(
            name = 'order_payments',
            con = conexao,
            if_exists = 'append',
            index = False,
            chunksize = 100
        )

    print(f'Registro envidados para order_paymentos: {len(df)} linhas')


# --------------- Tabela Order Reviews -----------------


def ler_order_reviews():
    arquivo = pasta_parquet / 'olist_order_reviews_dataset.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('---------- ORDER REVIEWS ----------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {list(df.columns)}')
    print(f'Amostra dos dados: ')
    print(df.head())

    return df



df_order_reviwes = ler_order_reviews()


def table_order_reviews():
    script = text("""
        CREATE TABLE IF NOT EXISTS order_reviews(
            review_id VARCHAR(100) NOT NULL,
            order_id VARCHAR(100) NOT NULL,
            score INT NOT NULL,
            comment_title VARCHAR(100),
            comment_message VARCHAR(500),
            creation_date DATETIME NOT NULL,
            answer_timestamp DATETIME NOT NULL,
            PRIMARY KEY(review_id, order_id)
        )
        """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela order_reviews criada ou já existente')



def insert_dados_order_reviews(df):
    df = df.rename(columns ={
            'review_score': 'score',
            'review_comment_title': 'comment_title',
            'review_comment_message': 'comment_message',
            'review_creation_date': 'creation_date',
            'review_answer_timestamp': 'answer_timestamp'
        })

    with engine.begin() as conexao:
         df.to_sql(
             name = 'order_reviews',
             con = conexao,
             if_exists = 'append',
             index = False,
             chunksize = 1000
         )

    print(f'Registros enviados para: {len(df)} linhas')



def ler_orders():
    arquivo = pasta_parquet / 'olist_orders_dataset.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('---------- ORDERS ----------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {df.columns}')
    print('Amostra dos dados: ')
    print(df.head())

    return df



df_orders = ler_orders()


def table_orders():
    script = text("""
        CREATE TABLE IF NOT EXISTS orders(
            order_id VARCHAR(100) NOT NULL,
            customer_id VARCHAR(100) NOT NULL,
            status VARCHAR(30) NOT NULL,
            purchase_timestamp DATETIME NOT NULL,
            approved_at DATETIME NOT NULL,
            delivered_carrier_date DATETIME NOT NULL,
            delivered_customer_date DATETIME NOT NULL,
            estimated_delivery_date DATETIME NOT NULL,
            PRIMARY KEY(order_id)
        )
        """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela orders criada ou já existente')


def insert_dados_orders(df):
    df = df.rename(columns = {
        'order_status' : 'status',
        'order_purchase_timestamp' : 'purchase_timestamp',
        'order_approved_at' : 'approved_at',
        'order_delivered_carrier_date' : 'delivered_carrier_date',
        'order_delivered_customer_date' : 'delivered_customer_date',
        'order_estimated_delivery_date' : 'estimated_delivery_date'
    })

    with engine.begin() as conexao:
        df.to_sql(
            name = 'orders',
            con = conexao,
            if_exists = 'append',
            index = False,
            chunksize = 1000
        )

    print(f'Registros enviados para orders: {len(df)} linhas')



# ----------- Tabela Products ----------------


def ler_products():
    arquivo = pasta_parquet / 'olist_products_dataset.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('---------- PRODUCTS ----------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {df.columns[0:2]}')
    print('Amostra dos dados: ')
    print(df.head())

    return df


df_products = ler_products()


def table_products():
    script = text("""
        CREATE TABLE IF NOT EXISTS products(
            product_id VARCHAR(100) NOT NULL,
            category_name VARCHAR(30) NOT NULL,
            PRIMARY KEY(product_id)
        )
        """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela products criada ou já existente')



def insert_dados_products(df):
    df = df[['product_id', 'product_category_name']]

    df = df.rename(columns = {
        'product_category_name' : 'category_name'
    })

    with engine.begin() as conexao:
        df.to_sql(
            name = 'products',
            con = conexao,
            if_exists = 'append',
            index = False,
            chunksize = 1000
        )

    print(f'Registros enviados para products: {len(df)} linhas')



# ------------ Tabela Sellers --------------

def ler_sellers():
    arquivo = pasta_parquet / 'olist_sellers_dataset.parquet'

    if not arquivo.exists():
        raise FileNotFoundError(
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_parquet(arquivo, engine = 'pyarrow')

    print('----------- SELLERS ----------')
    print(f'Registro: {len(df)}')
    print(f'Colunas: {list(df.columns)}')
    print('Amostra dos dados: ')
    print(df.head())

    return df


df_sellers = ler_sellers()


def table_sellers():
    script = text("""
        CREATE TABLE IF NOT EXISTS sellers(
            seller_id VARCHAR(100) NOT NULL,
            seller_zip_code_prefix INT NOT NULL,
            seller_city VARCHAR(50) NOT NULL,
            seller_state VARCHAR(50) NOT NULL,
            PRIMARY KEY(seller_id)
        )
        """
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela sellers criada ou já existente')



def insert_dados_sellers(df):
    with engine.begin() as conexao:
        df.to_sql(
            name = 'sellers',
            con = conexao,
            if_exists = 'append',
            index = False
        )

    print(f'Registros enviados para tabela sellers: {len(df)} linhas')


# ---------- Enderecos API ----------

def ler_enderecos_api():
    arquivo = base_dir / 'Enderecos' / 'enderecos.json'

    if not arquivo.exists():
        raise FileNotFoundError (
            print(f'Arquivo não encontrado: {arquivo}')
        )

    df = pd.read_json(arquivo)

    print('---------- Enderecos ----------')
    print(f'Registros: {len(df)}')
    print(f'Colunas: {list(df.columns)}')
    print('Amostra dos dados: ')
    print(df.head())

    return df


df_enderecos_api = ler_enderecos_api()


def table_enderecos_api():
    script = text('''
        CREATE TABLE IF NOT EXISTS api_enderecos(
            prefix VARCHAR(5) NOT NULL,
            cep VARCHAR(9) NOT NULL,
            bairro VARCHAR(100),
            estado VARCHAR(100),
            regiao VARCHAR(20),
            status VARCHAR(30),
            PRIMARY KEY(prefix)
        )
    '''
    )

    with engine.begin() as conexao:
        conexao.execute(script)

    print('Tabela enderecos já criada ou existente')



def insert_dados_api_enderecos(df):
    df = df.rename(columns = {
        'prefixo' : 'prefix'
    })

    with engine.begin() as conexao:
        df.to_sql(
            name = 'api_enderecos',
            con = conexao,
            if_exists = 'append',
            index = False,
            chunksize = 1000
        )

    print(f'Registros enviados para tabela api_endereços: {len(df)} linhas')


ler_enderecos_api()

# Lendo as tabelas no parquet

def read_tables():
    ler_product_category()
    ler_customer()
    ler_geolocation()
    ler_order_item()
    ler_order_payments()
    ler_order_reviews()
    ler_orders()
    ler_products()
    ler_sellers()
    ler_enderecos_api()


# Realizando o CREATE TABLE no banco

def create_tables():
    table_product_category()
    table_customer()
    table_geolocation()
    table_order_items()
    table_order_payments()
    table_order_reviews()
    table_orders()
    table_products()
    table_sellers()
    table_enderecos_api()


# Inserindo dados nas tabelas

def insert_dados():
    insert_dados_sellers(df_sellers)
    insert_dados_products(df_products)
    insert_dados_orders(df_orders)
    insert_dados_order_reviews(df_order_reviwes)
    insert_dados_order_payments(df_order_payments)
    insert_dados_order_items(df_order_items)
    insert_dados_geolocation(df_geolocation)
    insert_dados_customers(df_customers)
    insert_dados_product_category(df_product_category)


if __name__ == '__main__':
    read_tables()
    # create_tables()
    # insert_dados()
    # insert_dados_api_enderecos(df_enderecos_api)
