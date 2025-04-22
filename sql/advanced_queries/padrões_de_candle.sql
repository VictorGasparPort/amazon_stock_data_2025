-- Query: Detecção de Padrões de Candlestick (Identifica formações técnicas para trading)
SELECT *
FROM (
    SELECT
        date,
        CASE  -- Classifica padrões baseado em relações entre preços
            WHEN close > open AND high - close > close - open THEN 'Hammer'        -- Martelo (alta potencial)
            WHEN close < open AND close - low > open - close THEN 'Shooting Star' -- Estrela Cadente (queda potencial)
        END AS candle_pattern,
        LEAD(close,1) OVER (ORDER BY date) AS next_day_close  -- Preço de fechamento do próximo dia (para validação)
    FROM main_table
) patterns
WHERE candle_pattern IS NOT NULL;  -- Filtra apenas dias com padrões identificados