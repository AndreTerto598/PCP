
![Banner do YouTube eSports Gamer Escuro Vermelho Preto](https://github.com/user-attachments/assets/538caa9c-ba91-47dd-818f-4364a427ba28)

# PCP - SACACHO ⚙️🔨
Desenvolvimento de um programa PCP (Programação e controle de produção) para atender as necessidades da empresa de confecção têxtil Sacacho, uma empresa voltada para o ramo de embalagens de ráfia.

### Definição de requisitos e esboço📔:

•Página de Login: O sistema deverá contar com uma página inicial de login, para identificação e autenticação dos usuários, já que será utilizado por diferentes setores e colaboradores.
•	Cadastros : O sistema deverá contar com uma parte de cadastros, que serão separados inicialmente em: Cadastro de usuários, cadastro de produtos( Matéria prima e produtos acabados) e cadastro de fichas técnicas.

•	Cadastro de pedidos : É necessário uma página para cadastro dos pedidos que irão para a produção, esse cadastro de pedidos deve conter: 

-Nome do Cliente;
-Tipo de produto(Saco, bolsa ou rolo);
-Medida em cm;
-Tipo de tecido;
-Cor e tamanho da alça;
-Estampa;
-Data de emissão e entrega;
-Identificação do entregador;
-Nome do emissor do pedido;
-Quantidade de itens e volumes;
-Campo de observação.

![image](https://github.com/user-attachments/assets/e4d3da1c-b3c1-4933-ad95-fefba38affde)

•	Produção – A parte de produção deverá indicar se o pedido está em produção, ou se já foi produzido, além disso é importante que seja possível fazer lançamentos parciais dos pedidos, com quantidades parciais. Nesta seção serão alocados os pedidos cadastros anteriormente no cadastro de pedidos, portanto é importante que os pedidos sejam identificados por: Número de pedido, nome do cliente e produto.

•	Cálculo da matéria prima – A parte de produção deverá calcular o total de tecido gasto em KG e de alças gastas em metros. Para o cálculo dos tecidos devemos considerar as seguintes informações:

O cálculo para telas planas e telas tubulares é diferente, além disso deve-se considerar que para o cálculo das bolsas, acrescenta-se + 5 cm na altura da bolsa, enquanto que no cálculo do saco acrescenta-se + 3 cm na altura do saco.

-Telas Planas: Para os materiais cortados em telas planas, o cálculo é feito da seguinte maneira: Largura da tela em metros (EX: 93 plano é 0,93.) * corte em metros (Lembrar de considerar o acréscimo de bolsas e sacos) * Quantidade * gramatura da tela em KG (se for 65g ficará 0,065)

-Telas Tubulares: Para os materiais cortados em telas tubulares o cálculo é o mesmo, porém multiplica a largura da tela por 2, ou seja: Caso a tela seja de 50 cm laminada, a largura da tela no cálculo entrara como 1 m e não 0,50m.

Quais são as telas planas? As telas planas são: 

100 PLANO;
115 HB MARROM;
115 HB BRANCA;
60 HB BRANCA;
60 HB CINZA;
60 HBX;
60 PL CAST;
93 PLANO;
95 PLANO UV;
70 PL PLANO;


E quais são as telas tubulares? As telas tubulares são:

45 PL;		60 PL;			90 PL;
50 SL;		60 PL MARROM;
50 AM;	  60 SL;
50 PL;		60 AM;
50 VD;		60 VD;
55 PL;		65 PL;
65 SL;		70 PL;
75 PL;		80 PL;

•	Quais são as gramaturas das telas?

115 HB BRANCA -	90g
115 HB MARROM	- 90g
45 PL -	65g
45 SL -	58g
50 AM -	70g
50 HB CINZA -	110g
50 PL -	67g
50 PL CAST - 84g
50 VD -	70g
52 HB BRANCO -	120g
55 PL -	65g
60 HB BRANCA -	120g
60 HB CINZA -	120g
60 HBX -	79g
60 PL -	65g
60 PL CAST -	84g
60 PL MARROM -	60g
60 SL -	58g
60 VD -	70g
65 PL -	65g
65 SL -	60g
70 PL -	65g
75 PL -	65g
80 PL -	65g
93 PLANO -	65g
70 PL PLANO -	65g
95 PLANO UV -	65g
120 HB PL -	90g
60 AM -	70g
70 HB BRANCA -	120g
100 PLANO -	65g
90 PL -	65g

• Cálculo de alças :  O cálculo de alças é Quantidade de bolsas * 2 * tamanho da alça em metro.
### Estoque 
Necessita-se de uma visualização do estoque, em tempo real, conforme os gastos de matéria prima dos pedidos. Se possível com uma visualização diferente para quando a quantidade entrar em nível crítico.
![image](https://github.com/user-attachments/assets/d342f877-fd04-433f-8903-abed920bb3b5)

### Linguagens Utilizadas 💻:

Django como o framework web, SQLAlchemy para interagir com o banco de dados, e HTML/CSS/JavaScript para o frontend. Postgre pra banco de dados.
