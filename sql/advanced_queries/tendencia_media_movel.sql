-- Query 1: Tendência com Média Móvel e Rank de Volume Anual (Identifica padrões temporais)
SELECT
    date,
    close,
    AVG(close) OVER (
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW  -- Janela de 30 dias (dia atual + 29 anteriores)
    ) AS 30_day_avg,  -- Média móvel de 30 dias para suavizar tendências
    
    RANK() OVER (
        PARTITION BY EXTRACT(year FROM date)  -- Agrupa por ano (ex: 2023, 2024)
        ORDER BY volume DESC                 -- Ordena por volume descendente
    ) AS yearly_volume_rank  -- Classifica os dias por volume dentro de cada ano
FROM main_table;
