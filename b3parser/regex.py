# -*- coding: utf-8 -*-
# ##############################################################################
# O formato do arquivo COTAHIST.AAAA.TXT é descrito com detalhes no arquivo
# disponibilizado em '../info/Serieshistoricas_Layout.pdf'
#
# N: Numérico;
# X: Alfanumérico;
# V: Indica que o número possui vírgula;
# ( ): Quantidade de caracteres antes da vírgula;
# (99): Quantidade de caracteres depois da vírgula (potência de 10)
#
# Ex.: N(11)V99 = 13 dígitos implicitamente multiplicados por 10^2
# Ex.: N(16)V99 = 18 dígitos implicitamente multiplicados por 10^2
# Ex.: N(7)V999999 = 19 dígitos implicitamente multiplicados por 10^6
#
# ##############################################################################
regex_cabecalho = (
    # Início
    r'^'
    # Tipo registro (00 - Cabeçalho)
    r'00'
    # Caracteres fixos
    r'COTAHIST'
    # Separador
    r'\.'
    # Ano do histórico
    r'(?P<ano_historico>(\d{4}))'
    # Caracteres fixos (código da origem)
    r'BOVESPA'
    # Separador
    r' '
    # Data da criação do arquivo: AAAAMMDD
    r'(?P<data_criacao>(\d{8}))'
    # Reserva
    r'[\s]*'
    # Fim
    r'$'
)

regex_cauda = (
    # Início
    r'^'
    # Tipo registro (99 - Cauda)
    r'99'
    # Caracteres fixos
    r'COTAHIST'
    # Separador
    r'\.'
    # Ano do histórico
    r'(?P<ano_historico>(\d{4}))'
    # Caracteres fixos (código da origem)
    r'BOVESPA'
    # Separador
    r' '
    # Data da criação do arquivo: AAAAMMDD
    r'(?P<data_criacao>(\d{8}))'
    # Número de registros do arquivo
    r'(?P<num_registros>(\d{11}))'
    # Reserva
    r'[\s]*'
    # Fim
    r'$'
)

regex_cotacao = (
    # Início
    r'^'
    # Tipo registro (01 - Cotação)
    r'01'
    # Data do pregão: AAAAMMDD
    r'(?P<data_pregao>(\d{8}))'
    # Código BDI
    r'(?P<cod_bdi>(\d{2}))'
    # Código do papel
    r'(?P<cod_papel>([0-9a-zA-Z ]{12}))'
    # Tipo de mercado
    r'(?P<tp_merc>(\d{3}))'
    # Nome resumido - Emissora do papel
    r'(?P<nome_resum>(.{12}))'
    # Especicifação do papel
    r'(?P<espec_papel>(.{10}))'
    # Prazo em dias do Merc. a Termo
    r'(?P<prazo_dias_termo>([\d]{3}|[ ]{3}))'
    # Moeda de referência
    r'(?P<moeda>(.{4}))'
    # Preço de abertura: N(11)V99
    r'(?P<preco_abertura>(\d{13}))'
    # Preço máximo: N(11)V99
    r'(?P<preco_maximo>(\d{13}))'
    # Preço mínimo: N(11)V99
    r'(?P<preco_minimo>(\d{13}))'
    # Preço médio: N(11)V99
    r'(?P<preco_medio>(\d{13}))'
    # Preço do último negócio: N(11)V99
    r'(?P<preco_ultimo>(\d{13}))'
    # Preço da melhor compra: N(11)V99
    r'(?P<preco_melhor_compra>(\d{13}))'
    # Preço da melhor venda: N(11)V99
    r'(?P<preco_melhor_venda>(\d{13}))'
    # Número de negócios realizados
    r'(?P<num_negocios>(\d{5}))'
    # Quantidade total de títulos negociados: N(16)V99
    r'(?P<qtde_titulos>(\d{18}))'
    # Volume de titulos: N(16)V99
    r'(?P<vol_titulos>(\d{18}))'
    # Preço de exercício para o mercado de opções ou valor do contrato para
    # o mercado de termo secundário: N(11)V99
    r'(?P<preco_exerc>(\d{13}))'
    # Indicador de correção de preços de exercícios ou valores de contrato
    # para os mercados de opções ou termo secundário
    r'(?P<indicador_correcao>(\d{1}))'
    # Data do vencimento para os mercados de opções ou termo secundário:
    # AAAAMMDD
    r'(?P<data_vencimento>(\d{8}))'
    # Fator de cotação do papel:
    # 1 - Cotação unitária
    # 1000 - Cotação por lote de mil ações
    r'(?P<fator_cotacao>(\d{7}))'
    # Preço de exercício em pontos para opções referenciadas em dólar ou
    # valor de contrato em pontos para termo secundário: N(7)V999999
    r'(?P<preco_exerc_pontos>(\d{13}))'
    # Código do papel no sistema ISIN a partir de 15/05/1995
    r'(?P<cod_isi>([\w\d]{12}))'
    # Número de sequência do papel correspondente ao estado de direito
    # vigente
    r'(?P<distribuicao_papel>(\d{3}))'
    # Fim
    r'$'
)
