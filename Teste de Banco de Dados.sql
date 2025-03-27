-- Tabela para armazenar os dados das operadoras de planos de saúde
CREATE TABLE operadoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cnpj VARCHAR(14),
    nome_operadora VARCHAR(255),
    endereco VARCHAR(255),
    telefone VARCHAR(20),
    email VARCHAR(255),
    data_entrada DATE
);

-- Tabela para armazenar os demonstrativos contábeis
CREATE TABLE demonstrativos_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operadora_id INT,
    ano INT,
    trimestre INT,
    categoria VARCHAR(255),
    despesas DECIMAL(15, 2),
    FOREIGN KEY (operadora_id) REFERENCES operadoras(id)
);


-- Importação dos dados das operadoras
LOAD DATA INFILE '/path/to/operadoras_de_plano_de_saude_ativas.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES 
(cnpj, nome_operadora, endereco, telefone, email, data_entrada);

-- Importação dos dados dos demonstrativos contábeis
LOAD DATA INFILE '/path/to/demonstracoes_contabeis.csv'
INTO TABLE demonstrativos_contabeis
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(operadora_id, ano, trimestre, categoria, despesas);



---Concultas Analiticas - Operadoras com Maiores Despesas no Último Trimestre
SELECT o.nome_operadora, SUM(d.despesas) AS total_despesas
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.operadora_id = o.id
WHERE d.ano = YEAR(CURDATE()) AND d.trimestre = QUARTER(CURDATE())
  AND d.categoria = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
GROUP BY o.nome_operadora
ORDER BY total_despesas DESC
LIMIT 10;

---Concultas Analiticas - 10 Operadoras com Maiores Despesas no Último Ano
SELECT o.nome_operadora, SUM(d.despesas) AS total_despesas
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.operadora_id = o.id
WHERE d.ano = YEAR(CURDATE()) - 1
  AND d.categoria = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
GROUP BY o.nome_operadora
ORDER BY total_despesas DESC
LIMIT 10;

