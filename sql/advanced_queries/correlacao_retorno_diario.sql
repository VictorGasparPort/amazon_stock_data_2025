-- Query: Correlação de Retornos Diários (Analisa relação entre retornos consecutivos)
WITH DailyReturns AS (  -- CTE: Calcula retorno diário (% de variação entre abertura e fechamento)
    SELECT 
        date,
        (close - open)/open AS daily_return  -- Fórmula do retorno diário (ex: 0.05 = 5% de alta)
    FROM main_table
)
-- Calcula correlação móvel entre retorno do dia atual e do dia anterior:
SELECT
    a.date,
    CORR(a.daily_return, b.daily_return) OVER (  -- Função de correlação de Pearson
        ORDER BY a.date 
        ROWS BETWEEN 20 PRECEDING AND CURRENT ROW  -- Janela de 21 dias para cálculo
    ) AS rolling_correlation
FROM DailyReturns a
JOIN DailyReturns b ON a.date = b.date + INTERVAL '1 day';  -- Compara cada dia com o seguinte