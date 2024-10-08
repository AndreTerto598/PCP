PGDMP  	                	    |            PCP    17.0    17.0 9               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false                       1262    16388    PCP    DATABASE     |   CREATE DATABASE "PCP" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';
    DROP DATABASE "PCP";
                     postgres    false                       0    0    DATABASE "PCP"    ACL     �   REVOKE ALL ON DATABASE "PCP" FROM postgres;
GRANT CREATE,CONNECT ON DATABASE "PCP" TO postgres;
GRANT TEMPORARY ON DATABASE "PCP" TO postgres WITH GRANT OPTION;
                        postgres    false    4882            �            1259    16476    Cliente    TABLE     �  CREATE TABLE public."Cliente" (
    "Id_Cliente" integer NOT NULL,
    "Nome_Cliente" character varying(255) DEFAULT '100'::character varying NOT NULL,
    "Endereco_Cliente" character varying(255) DEFAULT '255'::character varying NOT NULL,
    "Telefone_Cliente" character varying(255) DEFAULT '20'::character varying NOT NULL,
    "Email_Cliente" character varying(255) DEFAULT '100'::character varying NOT NULL,
    "Cnpj_Cliente" character varying(255) DEFAULT '14'::character varying NOT NULL,
    "Cidade_Cliente" character varying(255) DEFAULT '100'::character varying NOT NULL,
    "Estado_Cliente" character varying(255) DEFAULT '2'::character varying NOT NULL,
    "Cep_Cliente" character varying(255) DEFAULT '10'::character varying NOT NULL
);
    DROP TABLE public."Cliente";
       public         heap r       postgres    false            �            1259    16475    Cliente_Id_Cliente_seq    SEQUENCE     �   CREATE SEQUENCE public."Cliente_Id_Cliente_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public."Cliente_Id_Cliente_seq";
       public               postgres    false    218                       0    0    Cliente_Id_Cliente_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public."Cliente_Id_Cliente_seq" OWNED BY public."Cliente"."Id_Cliente";
          public               postgres    false    217            �            1259    16556    Entrega    TABLE     =  CREATE TABLE public."Entrega" (
    "Id_Cliente" bigint NOT NULL,
    "Nome_Cliente" character varying(255) NOT NULL,
    "Endereco_Cliente" character varying(255) NOT NULL,
    "Telefone_Cliente" character varying(255) NOT NULL,
    "Cidade_Cliente" character varying(255) NOT NULL,
    "Estado_Cliente" character varying(255) NOT NULL,
    "Cep_Cliente" character varying(255) NOT NULL,
    "Id_Entregador" bigint NOT NULL,
    "Nome_Entregador" character varying(255) NOT NULL,
    "Data_Entrega" timestamp without time zone NOT NULL,
    "Qt_Pedido" bigint NOT NULL
);
    DROP TABLE public."Entrega";
       public         heap r       postgres    false            �            1259    16548 
   Entregador    TABLE     �   CREATE TABLE public."Entregador" (
    "Id_Entregador" integer NOT NULL,
    "Nome_Entregador" character varying(255) NOT NULL,
    "Cnpj_Entregador" character varying(255)
);
     DROP TABLE public."Entregador";
       public         heap r       postgres    false            �            1259    16547    Entregador_Id_Entregador_seq    SEQUENCE     �   CREATE SEQUENCE public."Entregador_Id_Entregador_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public."Entregador_Id_Entregador_seq";
       public               postgres    false    227                       0    0    Entregador_Id_Entregador_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public."Entregador_Id_Entregador_seq" OWNED BY public."Entregador"."Id_Entregador";
          public               postgres    false    226            �            1259    16530    Estoque    TABLE     %  CREATE TABLE public."Estoque" (
    "Id_Produto" bigint NOT NULL,
    "Nome_Produto" character varying(255) NOT NULL,
    "Qt_Estoque" bigint NOT NULL,
    "Preco_Medio" numeric(10,0),
    "Minimo_Estoque" bigint,
    "Unidade_Medida" character varying(255) DEFAULT '10'::character varying
);
    DROP TABLE public."Estoque";
       public         heap r       postgres    false            �            1259    16493 
   Fornecedor    TABLE     I  CREATE TABLE public."Fornecedor" (
    "Id_Fornecedor" integer NOT NULL,
    "Nome_Fornecedor" character varying(255) DEFAULT '100'::character varying NOT NULL,
    "Endereco_Fornecedor" character varying(255) DEFAULT '255'::character varying NOT NULL,
    "Telefone_Fornecedor" character varying(255) DEFAULT '20'::character varying NOT NULL,
    "Email_Fornecedor" character varying(255) DEFAULT '100'::character varying NOT NULL,
    "Cnpj_Fornecedor" character varying(255) DEFAULT '14'::character varying NOT NULL,
    "Tipo_fornecedor" character varying(255) NOT NULL,
    "Cidade_Fornecedor" character varying(255) DEFAULT '100'::character varying NOT NULL,
    "Estado_Fornecedor" character varying(255) DEFAULT '2'::character varying NOT NULL,
    "Cep_Fornecedor" character varying(255) DEFAULT '10'::character varying NOT NULL
);
     DROP TABLE public."Fornecedor";
       public         heap r       postgres    false            �            1259    16492    Fornecedore_Id_Fornecedor_seq    SEQUENCE     �   CREATE SEQUENCE public."Fornecedore_Id_Fornecedor_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public."Fornecedore_Id_Fornecedor_seq";
       public               postgres    false    220                       0    0    Fornecedore_Id_Fornecedor_seq    SEQUENCE OWNED BY     d   ALTER SEQUENCE public."Fornecedore_Id_Fornecedor_seq" OWNED BY public."Fornecedor"."Id_Fornecedor";
          public               postgres    false    219            �            1259    16522    Ordem_Producao    TABLE     �  CREATE TABLE public."Ordem_Producao" (
    "Ordem_Prioridade" character varying(255) NOT NULL,
    "Id_Ordem" integer NOT NULL,
    "Id_Produto" bigint NOT NULL,
    "Nome_Produto" character varying(255) NOT NULL,
    "Qt_Pedido" bigint NOT NULL,
    "Data_Inicio" timestamp without time zone NOT NULL,
    "Data_Fim" timestamp without time zone,
    "Status_Ordem" character varying(255) NOT NULL,
    "Id_Usuario" character varying(255),
    "Obs_Ordem" character varying(255),
    "Data_Cadastro" timestamp without time zone NOT NULL,
    "Custo_Estimado" numeric(10,0),
    "Custo_Real" numeric(10,0),
    "Data_Entrega" timestamp without time zone,
    "Id_Cliente" bigint NOT NULL,
    "Nome_Cliente" bigint NOT NULL,
    "Endereco_Entrega" character varying(255) NOT NULL,
    "Lista_Materiais" character varying(255) NOT NULL,
    "Qt_Materiais" bigint NOT NULL,
    "Qt_Pronto" bigint NOT NULL
);
 $   DROP TABLE public."Ordem_Producao";
       public         heap r       postgres    false            �            1259    16521    Ordem_Producao_Id_Ordem_seq    SEQUENCE     �   CREATE SEQUENCE public."Ordem_Producao_Id_Ordem_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public."Ordem_Producao_Id_Ordem_seq";
       public               postgres    false    224                       0    0    Ordem_Producao_Id_Ordem_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public."Ordem_Producao_Id_Ordem_seq" OWNED BY public."Ordem_Producao"."Id_Ordem";
          public               postgres    false    223            �            1259    16510    Produto    TABLE     �  CREATE TABLE public."Produto" (
    "Id_Produto" integer NOT NULL,
    "Nome_Produto" character varying(255) DEFAULT '100'::character varying NOT NULL,
    "Preco_Produto" numeric(10,0),
    "Qt_Estoque" bigint,
    "Categoria_Produto" character varying(255) DEFAULT '50'::character varying,
    "Peso_Produto" numeric(10,0),
    "Id_Fornecedor" bigint,
    "Unidade_Medida" character varying(255) DEFAULT '10'::character varying
);
    DROP TABLE public."Produto";
       public         heap r       postgres    false            �            1259    16509    Produto_Id_Produto_seq    SEQUENCE     �   CREATE SEQUENCE public."Produto_Id_Produto_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public."Produto_Id_Produto_seq";
       public               postgres    false    222                       0    0    Produto_Id_Produto_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public."Produto_Id_Produto_seq" OWNED BY public."Produto"."Id_Produto";
          public               postgres    false    221            �            1259    24805    usuario    TABLE     �   CREATE TABLE public.usuario (
    id integer NOT NULL,
    usuario character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    senha character varying(100) NOT NULL
);
    DROP TABLE public.usuario;
       public         heap r       postgres    false            �            1259    24804    usuario_id_seq    SEQUENCE     �   CREATE SEQUENCE public.usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.usuario_id_seq;
       public               postgres    false    230                       0    0    usuario_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.usuario_id_seq OWNED BY public.usuario.id;
          public               postgres    false    229            B           2604    16479    Cliente Id_Cliente    DEFAULT     ~   ALTER TABLE ONLY public."Cliente" ALTER COLUMN "Id_Cliente" SET DEFAULT nextval('public."Cliente_Id_Cliente_seq"'::regclass);
 E   ALTER TABLE public."Cliente" ALTER COLUMN "Id_Cliente" DROP DEFAULT;
       public               postgres    false    218    217    218            Z           2604    16551    Entregador Id_Entregador    DEFAULT     �   ALTER TABLE ONLY public."Entregador" ALTER COLUMN "Id_Entregador" SET DEFAULT nextval('public."Entregador_Id_Entregador_seq"'::regclass);
 K   ALTER TABLE public."Entregador" ALTER COLUMN "Id_Entregador" DROP DEFAULT;
       public               postgres    false    226    227    227            K           2604    16496    Fornecedor Id_Fornecedor    DEFAULT     �   ALTER TABLE ONLY public."Fornecedor" ALTER COLUMN "Id_Fornecedor" SET DEFAULT nextval('public."Fornecedore_Id_Fornecedor_seq"'::regclass);
 K   ALTER TABLE public."Fornecedor" ALTER COLUMN "Id_Fornecedor" DROP DEFAULT;
       public               postgres    false    219    220    220            X           2604    16525    Ordem_Producao Id_Ordem    DEFAULT     �   ALTER TABLE ONLY public."Ordem_Producao" ALTER COLUMN "Id_Ordem" SET DEFAULT nextval('public."Ordem_Producao_Id_Ordem_seq"'::regclass);
 J   ALTER TABLE public."Ordem_Producao" ALTER COLUMN "Id_Ordem" DROP DEFAULT;
       public               postgres    false    223    224    224            T           2604    16513    Produto Id_Produto    DEFAULT     ~   ALTER TABLE ONLY public."Produto" ALTER COLUMN "Id_Produto" SET DEFAULT nextval('public."Produto_Id_Produto_seq"'::regclass);
 E   ALTER TABLE public."Produto" ALTER COLUMN "Id_Produto" DROP DEFAULT;
       public               postgres    false    222    221    222            [           2604    24808 
   usuario id    DEFAULT     h   ALTER TABLE ONLY public.usuario ALTER COLUMN id SET DEFAULT nextval('public.usuario_id_seq'::regclass);
 9   ALTER TABLE public.usuario ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    229    230    230                       0    16476    Cliente 
   TABLE DATA           �   COPY public."Cliente" ("Id_Cliente", "Nome_Cliente", "Endereco_Cliente", "Telefone_Cliente", "Email_Cliente", "Cnpj_Cliente", "Cidade_Cliente", "Estado_Cliente", "Cep_Cliente") FROM stdin;
    public               postgres    false    218   �Q       
          0    16556    Entrega 
   TABLE DATA           �   COPY public."Entrega" ("Id_Cliente", "Nome_Cliente", "Endereco_Cliente", "Telefone_Cliente", "Cidade_Cliente", "Estado_Cliente", "Cep_Cliente", "Id_Entregador", "Nome_Entregador", "Data_Entrega", "Qt_Pedido") FROM stdin;
    public               postgres    false    228   �Q       	          0    16548 
   Entregador 
   TABLE DATA           ]   COPY public."Entregador" ("Id_Entregador", "Nome_Entregador", "Cnpj_Entregador") FROM stdin;
    public               postgres    false    227   �Q                 0    16530    Estoque 
   TABLE DATA           �   COPY public."Estoque" ("Id_Produto", "Nome_Produto", "Qt_Estoque", "Preco_Medio", "Minimo_Estoque", "Unidade_Medida") FROM stdin;
    public               postgres    false    225   R                 0    16493 
   Fornecedor 
   TABLE DATA           �   COPY public."Fornecedor" ("Id_Fornecedor", "Nome_Fornecedor", "Endereco_Fornecedor", "Telefone_Fornecedor", "Email_Fornecedor", "Cnpj_Fornecedor", "Tipo_fornecedor", "Cidade_Fornecedor", "Estado_Fornecedor", "Cep_Fornecedor") FROM stdin;
    public               postgres    false    220   *R                 0    16522    Ordem_Producao 
   TABLE DATA           ^  COPY public."Ordem_Producao" ("Ordem_Prioridade", "Id_Ordem", "Id_Produto", "Nome_Produto", "Qt_Pedido", "Data_Inicio", "Data_Fim", "Status_Ordem", "Id_Usuario", "Obs_Ordem", "Data_Cadastro", "Custo_Estimado", "Custo_Real", "Data_Entrega", "Id_Cliente", "Nome_Cliente", "Endereco_Entrega", "Lista_Materiais", "Qt_Materiais", "Qt_Pronto") FROM stdin;
    public               postgres    false    224   GR                 0    16510    Produto 
   TABLE DATA           �   COPY public."Produto" ("Id_Produto", "Nome_Produto", "Preco_Produto", "Qt_Estoque", "Categoria_Produto", "Peso_Produto", "Id_Fornecedor", "Unidade_Medida") FROM stdin;
    public               postgres    false    222   dR                 0    24805    usuario 
   TABLE DATA           <   COPY public.usuario (id, usuario, email, senha) FROM stdin;
    public               postgres    false    230   �R                  0    0    Cliente_Id_Cliente_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public."Cliente_Id_Cliente_seq"', 1, false);
          public               postgres    false    217                       0    0    Entregador_Id_Entregador_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public."Entregador_Id_Entregador_seq"', 1, false);
          public               postgres    false    226                       0    0    Fornecedore_Id_Fornecedor_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public."Fornecedore_Id_Fornecedor_seq"', 1, false);
          public               postgres    false    219                       0    0    Ordem_Producao_Id_Ordem_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public."Ordem_Producao_Id_Ordem_seq"', 1, false);
          public               postgres    false    223                       0    0    Produto_Id_Produto_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public."Produto_Id_Produto_seq"', 1, false);
          public               postgres    false    221                       0    0    usuario_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.usuario_id_seq', 4, true);
          public               postgres    false    229            ]           2606    16491    Cliente Cliente_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public."Cliente"
    ADD CONSTRAINT "Cliente_pkey" PRIMARY KEY ("Id_Cliente");
 B   ALTER TABLE ONLY public."Cliente" DROP CONSTRAINT "Cliente_pkey";
       public                 postgres    false    218            e           2606    16555    Entregador Entregador_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public."Entregador"
    ADD CONSTRAINT "Entregador_pkey" PRIMARY KEY ("Id_Entregador");
 H   ALTER TABLE ONLY public."Entregador" DROP CONSTRAINT "Entregador_pkey";
       public                 postgres    false    227            _           2606    16508    Fornecedor Fornecedore_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public."Fornecedor"
    ADD CONSTRAINT "Fornecedore_pkey" PRIMARY KEY ("Id_Fornecedor");
 I   ALTER TABLE ONLY public."Fornecedor" DROP CONSTRAINT "Fornecedore_pkey";
       public                 postgres    false    220            c           2606    16529 "   Ordem_Producao Ordem_Producao_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public."Ordem_Producao"
    ADD CONSTRAINT "Ordem_Producao_pkey" PRIMARY KEY ("Id_Ordem");
 P   ALTER TABLE ONLY public."Ordem_Producao" DROP CONSTRAINT "Ordem_Producao_pkey";
       public                 postgres    false    224            a           2606    16520    Produto Produto_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public."Produto"
    ADD CONSTRAINT "Produto_pkey" PRIMARY KEY ("Id_Produto");
 B   ALTER TABLE ONLY public."Produto" DROP CONSTRAINT "Produto_pkey";
       public                 postgres    false    222            g           2606    24810    usuario usuario_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public                 postgres    false    230            l           2606    16581    Entrega Entrega_fk0    FK CONSTRAINT     �   ALTER TABLE ONLY public."Entrega"
    ADD CONSTRAINT "Entrega_fk0" FOREIGN KEY ("Id_Cliente") REFERENCES public."Cliente"("Id_Cliente");
 A   ALTER TABLE ONLY public."Entrega" DROP CONSTRAINT "Entrega_fk0";
       public               postgres    false    218    4701    228            m           2606    16586    Entrega Entrega_fk7    FK CONSTRAINT     �   ALTER TABLE ONLY public."Entrega"
    ADD CONSTRAINT "Entrega_fk7" FOREIGN KEY ("Id_Entregador") REFERENCES public."Entregador"("Id_Entregador");
 A   ALTER TABLE ONLY public."Entrega" DROP CONSTRAINT "Entrega_fk7";
       public               postgres    false    4709    228    227            k           2606    16576    Estoque Estoque_fk0    FK CONSTRAINT     �   ALTER TABLE ONLY public."Estoque"
    ADD CONSTRAINT "Estoque_fk0" FOREIGN KEY ("Id_Produto") REFERENCES public."Produto"("Id_Produto");
 A   ALTER TABLE ONLY public."Estoque" DROP CONSTRAINT "Estoque_fk0";
       public               postgres    false    4705    222    225            i           2606    16571 "   Ordem_Producao Ordem_Producao_fk14    FK CONSTRAINT     �   ALTER TABLE ONLY public."Ordem_Producao"
    ADD CONSTRAINT "Ordem_Producao_fk14" FOREIGN KEY ("Id_Cliente") REFERENCES public."Cliente"("Id_Cliente");
 P   ALTER TABLE ONLY public."Ordem_Producao" DROP CONSTRAINT "Ordem_Producao_fk14";
       public               postgres    false    218    4701    224            j           2606    16566 !   Ordem_Producao Ordem_Producao_fk2    FK CONSTRAINT     �   ALTER TABLE ONLY public."Ordem_Producao"
    ADD CONSTRAINT "Ordem_Producao_fk2" FOREIGN KEY ("Id_Produto") REFERENCES public."Produto"("Id_Produto");
 O   ALTER TABLE ONLY public."Ordem_Producao" DROP CONSTRAINT "Ordem_Producao_fk2";
       public               postgres    false    222    4705    224            h           2606    16561    Produto Produto_fk6    FK CONSTRAINT     �   ALTER TABLE ONLY public."Produto"
    ADD CONSTRAINT "Produto_fk6" FOREIGN KEY ("Id_Fornecedor") REFERENCES public."Fornecedor"("Id_Fornecedor");
 A   ALTER TABLE ONLY public."Produto" DROP CONSTRAINT "Produto_fk6";
       public               postgres    false    220    222    4703                   x������ � �      
      x������ � �      	      x������ � �            x������ � �            x������ � �            x������ � �            x������ � �         a   x�M�K
� D��a�h�E7��"�����B�̇y��&��TJ�W@��XJ�.G)�S8�H>����EG���n��x��Q��T�jf��>
��0     