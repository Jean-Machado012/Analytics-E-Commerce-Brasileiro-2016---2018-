/* -------------------- Criando Tabelas Fatos e Dimensões -------------------- */

CREATE TABLE IF NOT EXISTS dim_customers(
	idCustomer VARCHAR(100),
    prefixo    VARCHAR(9),
    cep		   VARCHAR(9),
    bairro	   VARCHAR(80),
    estado	   VARCHAR(50),
    uf 		   CHAR(2),
    regiao	   VARCHAR(30),
    PRIMARY KEY( idCustomer)
);


CREATE TABLE IF NOT EXISTS dim_sellers(
	idSeller	VARCHAR(100),
    prefixo		INT,
    city		VARCHAR(50),
    UF			CHAR(2),
    PRIMARY KEY(idSeller)
);


CREATE TABLE IF NOT EXISTS dim_products(
	idProduto	VARCHAR(100),
    categoria	VARCHAR(100),
    PRIMARY KEY(idProduto)
);


CREATE TABLE IF NOT EXISTS fato_reviews(
	idReview			VARCHAR(100),
    idOrder				VARCHAR(100),
    score				INT,
    comment_title		VARCHAR(100),
    comment_message		VARCHAR(500),
    creation_date		DATE,
    answer_date			DATE,
    answer_time			TIME,
    PRIMARY KEY(idReview)
);


CREATE TABLE IF NOT EXISTS fato_orders(
	idOrder								VARCHAR(100),
    idCustomer							VARCHAR(100),
    idSeller							VARCHAR(100),
    idProduto							VARCHAR(100),
    qtdItens							SMALLINT,
    price								FLOAT,
    valor_frete							FLOAT,
    data_compra							DATE,
    hora_compra							TIME,
    data_pagamento						DATE,
    hora_pagamento						TIME,
    data_envio_logistica				DATE,
    hora_envio_logistica				TIME,
    data_limite_ordem_logistica			DATE,
    hora_limite_ordem_logistica			TIME,
    data_prevista_entrega_customer		DATE,
    data_recebido_customer				DATE,
    hora_recebido_customer				TIME,
    qtd_methods_payments				SMALLINT,
    payment_type						VARCHAR(50),
    qtd_parcelada						SMALLINT,
    PRIMARY KEY(idOrder),
    FOREIGN KEY(idCustomer) 			REFERENCES dim_customers (idCustomer),
    FOREIGN KEY(idSeller)				REFERENCES dim_sellers(idSeller),
    FOREIGN KEY(idProduto)				REFERENCES dim_products(idProduto)
);