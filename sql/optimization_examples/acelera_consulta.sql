-- Índice 1: Acelera consultas por intervalo de datas 
-- (ideal para dados temporais sequenciais)
CREATE INDEX idx_date_range ON main_table USING BRIN(date);  -- BRIN é mais eficiente que B-Tree para datas ordenadas