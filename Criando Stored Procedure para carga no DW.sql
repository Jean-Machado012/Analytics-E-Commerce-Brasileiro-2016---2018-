DELIMITER $$

CREATE PROCEDURE usp_dw_load()

USE dw_analitycs_olist

BEGIN

	/* -------------------- Realizando Truncate -------------------- */
    
    TRUNCATE TABLE dim_customers;
    TRUNCATE TABLE dim_products;
    TRUNCATE TABLE dim_sellers;
    TRUNCATE TABLE fato_orders;
    TRUNCATE TABLE fato_reviews;
    -- dim_calendario
    
    