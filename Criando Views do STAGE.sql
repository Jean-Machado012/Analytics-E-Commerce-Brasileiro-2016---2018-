/* -------------------- Criando as VIEW do STAGE -------------------- */

CREATE OR REPLACE VIEW vw_dim_customers
AS (
	SELECT 	DISTINCT(A.customer_unique_id)		AS 'idCustomer',
			A.customer_zip_code_prefix			AS 'prefix',
			C.cep,
			C.bairro,
			C.estado,
			B.state								AS 'UF',
			C.regiao
	FROM st_customers 			A
	LEFT JOIN st_geolocation	B
		ON A.customer_zip_code_prefix = B.zip_code_prefix
	LEFT JOIN st_api_enderecos	C
		ON A.customer_zip_code_prefix = C.prefix
);

    
CREATE OR REPLACE VIEW vw_dim_sellers
AS (
	SELECT	seller_id		AS 'idSeller',
			seller_city		AS 'city',
			seller_state	AS 'UF'
	FROM st_sellers
);


CREATE OR REPLACE VIEW vw_dim_products
AS (
	SELECT	A.product_id				AS 'idProduto',
			B.product_category_name		AS 'categoria'
	FROM st_products				A
	LEFT JOIN st_product_category	B
		ON A.category_name = B.product_category_name
);
    

CREATE OR REPLACE VIEW vw_dim_sellers
AS (
	SELECT	seller_id					AS 'idSeller',
			seller_zip_code_prefix		AS 'prefixo',
			seller_city					AS 'city',
			seller_state				AS 'UF'
	FROM st_sellers
);


CREATE OR REPLACE VIEW vw_fato_orders
AS (
	SELECT	A.order_id							AS 'idOrder',
			A.customer_id						AS 'idCustomer',
			B.seller_id							AS 'idSeller',
			B.product_id						AS 'idProduto',
			B.order_item_id						AS 'qtdItens',
			B.price,		
			B.freight_value						AS 'valor_frete',
			DATE(A.purchase_timestamp)			AS 'data_compra',
			TIME(A.purchase_timestamp)			AS 'hora_compra',
			DATE(A.approved_at)					AS 'data_pagamento',
			TIME(A.approved_at)					AS 'hora_pagamento',
			DATE(A.delivered_carrier_date)		AS 'data_envio_logistica',
			TIME(A.delivered_carrier_date)		AS 'hora_envio_logistica',
			DATE(B.shipping_limit_date)			AS 'data_limite_ordem_logistica',
			TIME(B.shipping_limit_date)			AS 'hora_limite_ordem_logistica',
			DATE(A.estimated_delivery_date)		AS 'data_prevista_entrega_customer',
			DATE(A.delivered_customer_date)		AS 'data_recebido_customer',
			TIME(A.delivered_customer_date)		AS 'hora_recebido_customer',
			C.payment_sequential				AS 'qtd_methods_payments',
			C.payment_type,
			C.payment_installments				AS 'qtd_parcelada'
	FROM st_orders					A
	LEFT JOIN st_order_items		B
		ON A.order_id = B.order_id
	LEFT JOIN st_order_payments		C
		ON A.order_id = C.order_id
);
    


CREATE OR REPLACE VIEW vw_fato_reviews
AS (
	SELECT	review_id	AS 'idReview',
			order_id	AS 'idOrder',
			score,
			comment_title,
			comment_message,
			DATE(creation_date)		AS 'creation_date',
			DATE(answer_timestamp)	AS 'answer_date',
			TIME(answer_timestamp)	AS 'answer_time'
	FROM st_order_reviews
);


