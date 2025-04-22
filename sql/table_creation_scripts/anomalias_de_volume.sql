-- Anomalias de Volume (Registra dias com volume atípico para investigação futura)
CREATE TABLE volume_anomalies (
    anomaly_date DATE PRIMARY KEY,  -- Data onde ocorreu a anomalia
    volume NUMERIC,                 -- Volume registrado naquela data
    deviation NUMERIC               -- Desvio padrão em relação à média (ex: 2.5 = 2.5σ acima da média)
);