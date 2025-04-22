-- Query: Variação Percentual Diária (Mostra volatilidade diária)
SELECT
    date,
    ROUND(((close - open)/open * 100), 2) AS daily_change_percent  -- Calcula % de variação e arredonda para 2 casas
FROM main_table
ORDER BY date DESC;  -- Ordena do dia mais recente para o mais antigo
