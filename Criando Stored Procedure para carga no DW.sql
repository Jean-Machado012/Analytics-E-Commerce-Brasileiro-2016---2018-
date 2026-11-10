USE dw_analitycs_olist;

DELIMITER $$

CREATE PROCEDURE usp_dw_load()

BEGIN

	/* -------------------- Criando Tabelas Fatos e Dimensões -------------------- */

	
	CREATE TABLE IF NOT EXISTS dw_analitycs_olist.dim_customers(
		id		   INT AUTO_INCREMENT,
		idCustomer VARCHAR(100),
		prefixo    VARCHAR(9),
		cep		   VARCHAR(9),
		bairro	   VARCHAR(80),
		estado	   VARCHAR(50),
		uf 		   CHAR(2),
		regiao	   VARCHAR(30),
		PRIMARY KEY(id),
		INDEX idx_customer (idCustomer)
	);


	CREATE TABLE IF NOT EXISTS dw_analitycs_olist.dim_sellers(
		id			INT AUTO_INCREMENT,
		idSeller	VARCHAR(100),
		prefixo		INT,
		city		VARCHAR(50),
		UF			CHAR(2),
		PRIMARY KEY(id),
		INDEX idx_sellers (idSeller)
	);


	CREATE TABLE IF NOT EXISTS dw_analitycs_olist.dim_products(
		id			INT AUTO_INCREMENT,
		idProduto	VARCHAR(100),
		categoria	VARCHAR(100),
		PRIMARY KEY(id),
		INDEX idx_products (idProduto)
	);


	CREATE TABLE IF NOT EXISTS dw_analitycs_olist.fato_reviews(
		id					INT AUTO_INCREMENT,
		idReview			VARCHAR(100),
		idOrder				VARCHAR(100),
		score				INT,
		comment_title		VARCHAR(100),
		comment_message		VARCHAR(500),
		creation_date		DATE,
		answer_date			DATE,
		answer_time			TIME,
		PRIMARY KEY(id),
		INDEX idx_reviews (idReview)
	);


	CREATE TABLE IF NOT EXISTS dw_analitycs_olist.fato_orders(
		id									INT AUTO_INCREMENT,
		idOrder								VARCHAR(100),
		idCustomer							INT,
		idSeller							INT,
		idProduto							INT,
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
		PRIMARY KEY(id),
		CONSTRAINT fk_customer_order
		FOREIGN KEY(idCustomer) 			REFERENCES dw_analitycs_olist.dim_customers(id),
		CONSTRAINT fk_seller_order
		FOREIGN KEY(idSeller)				REFERENCES dw_analitycs_olist.dim_sellers(id),
		CONSTRAINT fk_product_order
		FOREIGN KEY(idProduto)				REFERENCES dw_analitycs_olist.dim_products(id),
		INDEX idx_orders (idOrder)
	);

	/* -------------------- Realizando Truncate -------------------- */
    
    SET FOREIGN_KEY_CHECKS = 0;
    
    TRUNCATE TABLE dw_analitycs_olist.fato_orders;
    TRUNCATE TABLE dw_analitycs_olist.fato_reviews;
    TRUNCATE TABLE dw_analitycs_olist.dim_customers;
    TRUNCATE TABLE dw_analitycs_olist.dim_products;
    TRUNCATE TABLE dw_analitycs_olist.dim_sellers;
    
    
    SET FOREIGN_KEY_CHECKS = 1;
    
    /* -------------------- Populando Tabelas -------------------- */
    
    INSERT INTO dw_analitycs_olist.dim_customers(
		idCustomer,
        prefixo,
        cep,
        bairro,
        estado,
        uf,
        regiao
	)
    SELECT	idCustomer,
			prefix,
            cep,
            bairro,
            estado,
            UF,
            regiao
	FROM staging_analitycs_olist.vw_dim_customers;
    
    
	INSERT INTO dw_analitycs_olist.dim_products(
		idProduto,
        categoria
	)
    SELECT	idProduto,
			categoria
	FROM staging_analitycs_olist.vw_dim_products;
    
    
    INSERT INTO dw_analitycs_olist.dim_sellers(
		idSeller,
        prefixo,
        city,
        UF
	)
    SELECT	idSeller,
			prefixo,
            city,
            UF
	FROM staging_analitycs_olist.vw_dim_sellers;
    

	INSERT INTO dw_analitycs_olist.fato_reviews(
		idReview,
        idOrder,
        score,
        comment_title,
        comment_message,
        creation_date,
        answer_date,
        answer_time
	)
    SELECT	idReview,
			idOrder,
            score,
            comment_title,
            comment_message,
            creation_date,
            answer_date,
            answer_time
	FROM staging_analitycs_olist.vw_fato_reviews;
    
    
    INSERT INTO dw_analitycs_olist.fato_orders(
		idOrder,
        idCustomer,
        idSeller,
        idProduto,
        qtdItens,
        price,
        valor_frete,
        data_compra,
        hora_compra,
        data_pagamento,
        hora_pagamento,
        data_envio_logistica,
        hora_envio_logistica,
        data_limite_ordem_logistica,
        hora_limite_ordem_logistica,
        data_prevista_entrega_customer,
        data_recebido_customer,
        hora_recebido_customer,
        qtd_methods_payments,
        payment_type,
        qtd_parcelada
	)
    SELECT	A.idOrder,
			B.id,
			C.id,
			D.id,
			A.qtdItens,
			A.price,  
			A.valor_frete, 
			A.data_compra, 
			A.hora_compra, 
			A.data_pagamento, 
			A.hora_pagamento, 
			A.data_envio_logistica,  
			A.hora_envio_logistica, 
			A.data_limite_ordem_logistica, 
			A.hora_limite_ordem_logistica, 
			A.data_prevista_entrega_customer, 
			A.data_recebido_customer, 
			A.hora_recebido_customer, 
			A.qtd_methods_payments, 
			A.payment_type,
			A.qtd_parcelada
		FROM staging_analitycs_olist.vw_fato_orders		A
        LEFT JOIN dw_analitycs_olist.dim_customers		B
			ON A.idCustomer = B.idCustomer
		LEFT JOIN dw_analitycs_olist.dim_sellers		C
			ON A.idSeller = C.idSeller
		LEFT JOIN dw_analitycs_olist.dim_products		D
			ON A.idProduto = D.idProduto;
        
END $$

DELIMITER ;
