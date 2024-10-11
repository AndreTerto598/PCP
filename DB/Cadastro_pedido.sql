CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    nome_cliente VARCHAR(100) NOT NULL,
    produto VARCHAR(100) NOT NULL,
    data_emissao DATE NOT NULL,
    data_entrega DATE NOT NULL,
    entregador VARCHAR(100),
    emissor_pedido VARCHAR(100),
    tamanho VARCHAR(50),
    tela VARCHAR(100),
    alca VARCHAR(100),
    estampa VARCHAR(100),
    quantidade INTEGER NOT NULL,
    qtd_volumes INTEGER,
    observacao TEXT
);

