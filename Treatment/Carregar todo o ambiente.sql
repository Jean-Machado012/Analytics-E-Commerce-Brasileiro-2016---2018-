DELIMITER $$

CREATE PROCEDURE usp_load_envirioment()

BEGIN
	
    -- Carregando área de Stage
    CALL staging_analitycs_olist.usp_st_load();

	-- Carregando Data Warehouse
	CALL dw_analitycs_olist.usp_dw_load();
    
END $$

DELIMITER ;