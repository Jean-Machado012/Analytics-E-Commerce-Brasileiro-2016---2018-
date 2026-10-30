DELIMITER $$

CREATE PROCEDURE usp_st_load()

USE staging_analitycs_olist;

BEGIN

/* ---------- Criando tabelas de STAGE caso elas não existam ---------- */


CREATE TABLE IF NOT EXISTS st_customers(
	customer_id VARCHAR(100),
    customer_unique_id VARCHAR(100),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS st_geolocation(
	zip_code_prefix INT,
    latitude FLOAT,
    longitude FLOAT,
    city VARCHAR(100),
    state VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS st_order_items(
	order_id VARCHAR(100),
    order_item_id SMALLINT,
    product_id VARCHAR(100),
    seller_id VARCHAR(100),
    shipping_limit_date DATETIME,
    price FLOAT,
    freight_value FLOAT
);
    

CREATE TABLE IF NOT EXISTS st_order_payments(
	order_id VARCHAR(100),
    payment_sequential SMALLINT,
    payment_type VARCHAR(50),
    payment_installments SMALLINT,
    payment_value FLOAT
);


CREATE TABLE IF NOT EXISTS st_order_reviews(
	review_id VARCHAR(100),
    order_id VARCHAR(100),
    score INT,
    comment_title VARCHAR(100),
    comment_message VARCHAR(500),
    creation_date DATETIME,
    answer_timestamp DATETIME
);


CREATE TABLE IF NOT EXISTS st_orders(
	order_id VARCHAR(100),
    customer_id VARCHAR(100),
    status VARCHAR(30),
    purchase_timestamp DATETIME,
    approved_at DATETIME,
    delivered_carrier_date DATETIME,
    delivered_customer_date DATETIME,
    estimated_delivery_date DATETIME
);


CREATE TABLE IF NOT EXISTS st_product_category(
	product_category_name VARCHAR(100),
    product_category_name_english VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS st_products(
	product_id VARCHAR(100),
    category_name VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS st_sellers(
	seller_id VARCHAR(100),
    seller_zip_code_prefix INT,
    seller_city VARCHAR(50),
    seller_state VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS st_api_enderecos(
	prefix VARCHAR(5),
    cep VARCHAR(9),
    bairro VARCHAR(100),
    estado VARCHAR(100),
    regiao VARCHAR(20),
    status VARCHAR(30)
);



/* ---------- Limpando área de STAGE ---------- */

TRUNCATE TABLE st_api_enderecos;
TRUNCATE TABLE st_customers;
TRUNCATE TABLE st_geolocation;
TRUNCATE TABLE st_order_items;
TRUNCATE TABLE st_order_payments;
TRUNCATE TABLE st_order_reviews;
TRUNCATE TABLE st_orders;
TRUNCATE TABLE st_product_category;
TRUNCATE TABLE st_products;
TRUNCATE TABLE st_sellers;



/* ---------- Populando área de STAGE ---------- */

INSERT INTO st_customers(
	customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
)
SELECT	customer_id,
		customer_unique_id,
		customer_zip_code_prefix,
		customer_city,
		customer_state
FROM db_analitycs_olist.customers;




INSERT INTO st_geolocation(
	zip_code_prefix,
    latitude,
    longitude,
    city,
    state
)
SELECT	zip_code_prefix,
		latitude,
		longitude,
		city,
		state
FROM db_analitycs_olist.geolocation;



INSERT INTO st_order_items(
	order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value
)
SELECT	order_id,
		order_item_id,
		product_id,
		seller_id,
		shipping_limit_date,
		price,
		freight_value
FROM db_analitycs_olist.order_items;



INSERT INTO st_order_payments(
	order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
)
SELECT	order_id,
		payment_sequential,
		payment_type,
		payment_installments,
		payment_value
FROM db_analitycs_olist.order_payments;



INSERT INTO st_order_reviews(
	review_id,
    order_id,
    score,
    comment_title,
    comment_message,
    creation_date,
    answer_timestamp
)
SELECT	review_id,
		order_id,
		score,
		comment_title,
		comment_message,
		creation_date,
		answer_timestamp
FROM db_analitycs_olist.order_reviews;



INSERT INTO st_orders(
	order_id,
    customer_id,
    status,
    purchase_timestamp,
    approved_at,
    delivered_carrier_date,
    delivered_customer_date,
    estimated_delivery_date
)
SELECT	order_id,
		customer_id,
		status,
		purchase_timestamp,
		approved_at,
		delivered_carrier_date,
		delivered_customer_date,
		estimated_delivery_date
FROM db_analitycs_olist.orders;



INSERT INTO st_product_category(
	product_category_name,
    product_category_name_english
)
SELECT	product_category_name,
		product_category_name_english
FROM db_analitycs_olist.product_category;



INSERT INTO st_products(
	product_id,
    category_name
)
SELECT	product_id,
		category_name
FROM db_analitycs_olist.products;



INSERT INTO st_sellers(
	seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
)
SELECT 	seller_id,
		seller_zip_code_prefix,
		seller_city,
		seller_state
FROM db_analitycs_olist.sellers;




INSERT INTO st_api_enderecos(
	prefix,
    cep,
    bairro,
    estado,
    regiao,
    status
)
SELECT	prefix,
		cep,
		bairro,
		estado,
		regiao,
		status
FROM db_analitycs_olist.api_enderecos;


END $$

DELIMITER ;

