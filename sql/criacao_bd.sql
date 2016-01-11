-- Cria o banco de dados inicial

CREATE TABLE cotacoes
(
    id serial NOT NULL,
    data_pregao date NOT NULL,
    cod_bdi character varying(2) NOT NULL,
    cod_papel character varying(12) NOT NULL,
    tp_merc character varying(3) NOT NULL,
    nome_resum character varying(12) NOT NULL,
    espec_papel character varying(10) NOT NULL,
    prazo_dias_termo smallint NOT NULL,
    moeda character varying(4) NOT NULL,
    preco_abertura double precision NOT NULL,
    preco_maximo double precision NOT NULL,
    preco_minimo double precision NOT NULL,
    preco_medio double precision NOT NULL,
    preco_ultimo double precision NOT NULL,
    preco_melhor_compra double precision NOT NULL,
    preco_melhor_venda double precision NOT NULL,
    num_negocios double precision NOT NULL,
    qtde_titulos double precision NOT NULL,
    vol_titulos double precision NOT NULL,
    preco_exerc double precision NOT NULL,
    indicador_correcao character varying(1) NOT NULL,
    data_vencimento date NOT NULL,
    fator_cotacao smallint NOT NULL,
    preco_exerc_pontos double precision NOT NULL,
    cod_isi character varying(12) NOT NULL,
    distribuicao_papel character varying(3) NOT NULL,

    CONSTRAINT cotacoes_pkey PRIMARY KEY (
        id
    ),
    CONSTRAINT cotacoes_unique UNIQUE (
        data_pregao, cod_bdi, cod_papel, tp_merc, prazo_dias_termo
    )
)
