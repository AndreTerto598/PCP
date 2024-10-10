
CREATE TABLE "Estoque_tecido" (
	id SERIAL PRIMARY KEY,
	nome_tela VARCHAR(255) NOT NULL,
	quantidade_tela BIGINT NOT NULL,
	tipo_tela VARCHAR(255) NOT NULL,
	unidade_medida VARCHAR(2) NOT NULL
);

SELECT * FROM Estoque_tecido

CREATE TABLE "Estoque_alca" (
	id SERIAL PRIMARY KEY,
	nome_alca VARCHAR(255) NOT NULL,
	quantidade_alca BIGINT NOT NULL,
	unidade_medida VARCHAR(2) NOT NULL
);

SELECT * FROM pg_catalog.pg_tables WHERE tablename = 'estoque_alca';

SELECT * FROM Estoque_alca