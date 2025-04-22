-- Particionamento 3: Divide a tabela por faixa de preço de fechamento (melhora performance em queries segmentadas)
CREATE TABLE main_table_partitioned PARTITION BY RANGE (close);  -- Define estratégia de particionamento
-- Cria partições físicas separadas:
CREATE TABLE partition_low VALUES LESS THAN (100);    -- Fechamento < US$100
CREATE TABLE partition_med VALUES LESS THAN (200);    -- Fechamento entre US$100 e US$200
CREATE TABLE partition_high VALUES LESS THAN (MAXVALUE);  -- Fechamento >= US$200