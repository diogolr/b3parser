# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(
    0,
    os.path.abspath( os.path.join( os.path.dirname( __file__ ), '..' ) )
)

from b3parser import B3Parser

if __name__ == '__main__':
    cols_sel = [
        'data_pregao',
        'cod_bdi',
        'cod_papel',
        'tp_merc',
        'nome_resum',
        'espec_papel',
        # 'prazo_dias_termo',
        # 'moeda',
        # 'preco_abertura',
        # 'preco_maximo',
        # 'preco_minimo',
        # 'preco_medio',
        'preco_ultimo',
        # 'preco_melhor_compra',
        # 'preco_melhor_venda',
        # 'num_negocios',
        # 'qtde_titulos',
        # 'vol_titulos',
        # 'preco_exerc',
        # 'indicador_correcao',
        # 'data_vencimento',
        'fator_cotacao',
        # 'preco_exerc_pontos',
        # 'cod_isi',
        # 'distribuicao_papel',
    ]

    cods_bdi = [
        '02',  # LOTE PADRÃO
        # '06',  # CONCORDATÁRIAS
        # '10',  # DIREITOS E RECIBOS
        '12',  # FUNDOS IMOBILIÁRIOS
        # '14',  # CERTIFIC. INVESTIMENTO / DEBÊNTURES / TÍTULOS DIVIDA PÚBLICA
        # '18',  # OBRIGAÇÕES
        # '22',  # BÔNUS (PRIVADOS)
        # '26',  # APÓLICES / BÔNUS / TÍTULOS PÚBLICOS
        # '32',  # EXERCÍCIO DE OPÇÕES DE COMPRA DE ÍNDICE
        # '33',  # EXERCÍCIO DE OPÇÕES DE VENDA DE ÍNDICE
        # '38',  # EXERCÍCIO DE OPÇÕES DE COMPRA
        # '42',  # EXERCÍCIO DE OPÇÕES DE VENDA
        # '46',  # LEILÃO DE TÍTULOS NÃO COTADOS
        # '48',  # LEILÃO DE PRIVATIZAÇÃO
        # '50',  # LEILÃO
        # '51',  # LEILÃO FINOR
        # '52',  # LEILÃO FINAM
        # '53',  # LEILÃO FISET
        # '54',  # LEILÃO DE AÇÕES EM MORA
        # '56',  # VENDAS POR ALVARÁ JUDICIAL
        # '58',  # OUTROS
        # '60',  # PERMUTA POR AÇÕES
        # '61',  # META
        # '62',  # TERMO
        # '66',  # DEBÊNTURES COM DATA DE VENCIMENTO ATÉ 3 ANOS
        # '68',  # DEBÊNTURES COM DATA DE VENCIMENTO MAIOR QUE 3 ANOS
        # '70',  # FUTURO COM MOVIMENTAÇÃO CONTÍNUA
        # '71',  # FUTURO COM RETENÇÃO DE GANHO
        # '74',  # OPÇÕES DE COMPRA DE ÍNDICES
        # '75',  # OPÇÕES DE VENDA DE ÍNDICES
        # '78',  # OPÇÕES DE COMPRA
        # '82',  # OPÇÕES DE VENDA
        # '83',  # DEBÊNTURES E NOTAS PROMISSÓRIAS
        '96',  # FRACIONÁRIO
        # '99',  # TOTAL GERAL
    ]

    tps_merc = [
        '010',  # VISTA
        # '012',  # EXERCÍCIO DE OPÇÕES DE COMPRA
        # '013',  # EXERCÍCIO DE OPÇÕES DE VENDA
        # '017',  # LEILÃO
        '020',  # FRACIONÁRIO
        # '030',  # TERMO
        # '050',  # FUTURO COM RETENÇÃO DE GANHO
        # '060',  # FUTURO COM MOVIMENTAÇÃO CONTÍNUA
        # '070',  # OPÇÕES DE COMPRA
        # '080',  # OPÇÕES DE VENDA
    ]

    filtros = {
       'cod_bdi': ( 'in', cods_bdi ),
       'tp_merc': ( 'in', tps_merc ),
    }

    ano = 2015
    # mes = None
    # dia = None

    parser = B3Parser( 'data/COTAHIST_A{0}.TXT'.format( ano ) )

    parser.ler_arquivo( cols_sel = cols_sel, filtros = filtros )

    parser.exportar_json( 'data/{0}.json'.format( ano ) )
    parser.exportar_sql( 'data/{0}.sql'.format( ano ) )
    parser.exportar_csv( 'data/{0}.csv'.format( ano ) )
