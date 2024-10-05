CREATE TABLE IF NOT EXISTS "Cliente" (
	"Id_Cliente" serial NOT NULL UNIQUE,
	"Nome_Cliente" varchar(255) NOT NULL DEFAULT '100',
	"Endereco_Cliente" varchar(255) NOT NULL DEFAULT '255',
	"Telefone_Cliente" varchar(255) NOT NULL DEFAULT '20',
	"Email_Cliente" varchar(255) NOT NULL DEFAULT '100',
	"Cnpj_Cliente" varchar(255) NOT NULL DEFAULT '14',
	"Cidade_Cliente" varchar(255) NOT NULL DEFAULT '100',
	"Estado_Cliente" varchar(255) NOT NULL DEFAULT '2',
	"Cep_Cliente" varchar(255) NOT NULL DEFAULT '10',
	PRIMARY KEY ("Id_Cliente")
);

CREATE TABLE IF NOT EXISTS "Fornecedore" (
	"Id_Fornecedor" serial NOT NULL,
	"Nome_Fornecedor" varchar(255) NOT NULL DEFAULT '100',
	"Endereco_Fornecedor" varchar(255) NOT NULL DEFAULT '255',
	"Telefone_Fornecedor" varchar(255) NOT NULL DEFAULT '20',
	"Email_Fornecedor" varchar(255) NOT NULL DEFAULT '100',
	"Cnpj_Fornecedor" varchar(255) NOT NULL DEFAULT '14',
	"Tipo_fornecedor" varchar(255) NOT NULL,
	"Cidade_Fornecedor" varchar(255) NOT NULL DEFAULT '100',
	"Estado_Fornecedor" varchar(255) NOT NULL DEFAULT '2',
	"Cep_Fornecedor" varchar(255) NOT NULL DEFAULT '10',
	PRIMARY KEY ("Id_Fornecedor")
);

CREATE TABLE IF NOT EXISTS "Produto" (
	"Id_Produto" serial NOT NULL UNIQUE,
	"Nome_Produto" varchar(255) NOT NULL DEFAULT '100',
	"Preco_Produto" numeric(10,0),
	"Qt_Estoque" bigint,
	"Categoria_Produto" varchar(255) DEFAULT '50',
	"Peso_Produto" numeric(10,0),
	"Id_Fornecedor" bigint,
	"Unidade_Medida" varchar(255) DEFAULT '10',
	PRIMARY KEY ("Id_Produto")
);

CREATE TABLE IF NOT EXISTS "Ordem_Producao" (
	"Ordem_Prioridade" varchar(255) NOT NULL,
	"Id_Ordem" serial NOT NULL,
	"Id_Produto" bigint NOT NULL,
	"Nome_Produto" varchar(255) NOT NULL,
	"Qt_Pedido" bigint NOT NULL,
	"Data_Inicio" timestamp without time zone NOT NULL,
	"Data_Fim" timestamp without time zone,
	"Status_Ordem" varchar(255) NOT NULL,
	"Id_Usuario" varchar(255),
	"Obs_Ordem" varchar(255),
	"Data_Cadastro" timestamp without time zone NOT NULL,
	"Custo_Estimado" numeric(10,0),
	"Custo_Real" numeric(10,0),
	"Data_Entrega" timestamp without time zone,
	"Id_Cliente" bigint NOT NULL,
	"Nome_Cliente" bigint NOT NULL,
	"Endereco_Entrega" varchar(255) NOT NULL,
	"Lista_Materiais" varchar(255) NOT NULL,
	"Qt_Materiais" bigint NOT NULL,
	"Qt_Pronto" bigint NOT NULL,
	PRIMARY KEY ("Id_Ordem")
);

CREATE TABLE IF NOT EXISTS "Estoque" (
	"Id_Produto" bigint NOT NULL,
	"Nome_Produto" varchar(255) NOT NULL,
	"Qt_Estoque" bigint NOT NULL,
	"Preco_Medio" numeric(10,0),
	"Minimo_Estoque" bigint,
	"Unidade_Medida" varchar(255) DEFAULT '10'
);

CREATE TABLE IF NOT EXISTS "Usuario" (
	"Id_Usuario" serial NOT NULL UNIQUE,
	"Nome_Usuario" varchar(255) NOT NULL DEFAULT '100',
	"Senha_Usuario" varchar(255) NOT NULL DEFAULT '255',
	PRIMARY KEY ("Id_Usuario")
);

CREATE TABLE IF NOT EXISTS "Entregador" (
	"Id_Entregador" serial NOT NULL UNIQUE,
	"Nome_Entregador" varchar(255) NOT NULL,
	"Cnpj_Entregador" varchar(255),
	PRIMARY KEY ("Id_Entregador")
);

CREATE TABLE IF NOT EXISTS "Entrega" (
	"Id_Cliente" bigint NOT NULL,
	"Nome_Cliente" varchar(255) NOT NULL,
	"Endereco_Cliente" varchar(255) NOT NULL,
	"Telefone_Cliente" varchar(255) NOT NULL,
	"Cidade_Cliente" varchar(255) NOT NULL,
	"Estado_Cliente" varchar(255) NOT NULL,
	"Cep_Cliente" varchar(255) NOT NULL,
	"Id_Entregador" bigint NOT NULL,
	"Nome_Entregador" varchar(255) NOT NULL,
	"Data_Entrega" timestamp without time zone NOT NULL,
	"Qt_Pedido" bigint NOT NULL
);




ALTER TABLE "Produto" ADD CONSTRAINT "Produto_fk6" FOREIGN KEY ("Id_Fornecedor") REFERENCES "Fornecedore"("Id_Fornecedor");

ALTER TABLE "Ordem_Producao" ADD CONSTRAINT "Ordem_Producao_fk2" FOREIGN KEY ("Id_Produto") REFERENCES "Produto"("Id_Produto");

ALTER TABLE "Ordem_Producao" ADD CONSTRAINT "Ordem_Producao_fk6" FOREIGN KEY ("Id_Usuario") REFERENCES "Usuario"("Id_Usuario");

ALTER TABLE "Ordem_Producao" ADD CONSTRAINT "Ordem_Producao_fk14" FOREIGN KEY ("Id_Cliente") REFERENCES "Cliente"("Id_Cliente");

ALTER TABLE "Entrega" ADD CONSTRAINT "Entrega_fk0" FOREIGN KEY ("Id_Cliente") REFERENCES "Cliente"("Id_Cliente");

ALTER TABLE "Entrega" ADD CONSTRAINT "Entrega_fk7" FOREIGN KEY ("Id_Entregador") REFERENCES "Entregador"("Id_Entregador");
