-- Média Móvel Mensal (Armazena médias de abertura/fechamento por mês para análise histórica)
CREATE TABLE amazon_monthly_avg AS
SELECT
    DATE_TRUNC('month', date) AS month,  -- Agrupa registros por mês (ex: '2023-01-01' para todo janeiro/2023)
    AVG(open) AS avg_open,               -- Calcula a média dos preços de abertura do mês
    AVG(close) AS avg_close              -- Calcula a média dos preços de fechamento do mês
FROM main_table
GROUP BY 1;  -- Agrupa resultados pelo primeiro campo (month)
