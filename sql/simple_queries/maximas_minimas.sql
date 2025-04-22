-- Query: Máximas e Mínimas Mensais (Identifica níveis de suporte/resistência)
SELECT
    DATE_TRUNC('month', date) AS month,  -- Agrupa registros por mês
    MAX(high) AS monthly_high,           -- Maior preço atingido no mês
    MIN(low) AS monthly_low              -- Menor preço atingido no mês
FROM main_table
GROUP BY 1
ORDER BY 1 DESC;  -- Ordena do mês mais recente para o mais antigo