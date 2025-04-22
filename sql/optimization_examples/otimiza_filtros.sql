-- Índice: Otimiza filtros em volume alto (ex: consultas que buscam dias com mais de 1M de volume)
CREATE INDEX idx_volume_filter ON main_table(volume) 
WHERE volume > 1000000;  -- Cria índice apenas para registros que satisfazem a condição
