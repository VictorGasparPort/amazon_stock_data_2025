-- Metadados (Documentação das colunas para governança de dados)
CREATE TABLE column_metadata (
    column_name VARCHAR(50),   -- Nome da coluna original (ex: 'open')
    data_type VARCHAR(50),     -- Tipo de dado armazenado (ex: NUMERIC)
    description TEXT           -- Explicação do significado da coluna
);
-- Popula a tabela com metadados básicos:
INSERT INTO column_metadata VALUES
('date', 'DATE', 'Data do registro'),
('open', 'NUMERIC', 'Preço de abertura'),
('close', 'NUMERIC', 'Preço de fechamento');