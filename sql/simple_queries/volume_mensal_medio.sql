-- Query: Volume Médio por Mês (Analisa sazonalidade no volume de negociações)
SELECT
    TO_CHAR(date, 'YYYY-MM') AS month,  -- Formata data como 'ANO-MÊS' (ex: '2023-07')
    AVG(volume) AS avg_volume           -- Calcula volume médio do mês
FROM main_table
GROUP BY 1    -- Agrupa pelo primeiro campo (month)
ORDER BY 1;   -- Ordena cronologicamente
