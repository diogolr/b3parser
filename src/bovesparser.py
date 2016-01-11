# -*- encoding: utf-8 -*-
import re

from datetime import datetime

from src.regex import regex_cabecalho
from src.regex import regex_cauda
from src.regex import regex_cotacao


class BovesParser( object ):
    # --------------------------------------------------------------------------
    # Atributos estáticos
    # --------------------------------------------------------------------------
    formato_sql = [
        'postgresql',
        'pgsql',
    ]

    # --------------------------------------------------------------------------
    # Métodos
    # --------------------------------------------------------------------------
    def __init__( self, endereco_arquivo = None ):
        if endereco_arquivo is None or endereco_arquivo == '':
            print(
                'O endereço do arquivo não foi definido corretamente.'
            )
            exit( 1 )

        self.endereco_arquivo = endereco_arquivo

        self.abrir_arquivo()


    def __del__( self ):
        if self.arquivo is not None:
            self.arquivo.close()


    def abrir_arquivo( self ):
        try:
            self.arquivo = open( file = self.endereco_arquivo, mode = 'r', )

        except OSError:
            print(
                'Ocorreu um erro durante o processo de leitura do arquivo '
                '"{0}". Verifique se o arquivo existe e está localizado na '
                'pasta indicada.'.format( self.endereco_arquivo )
            )
            exit( 1 )


    def ler_arquivo( self ):
        if self.arquivo is None:
            print(
                'O arquivo não foi aberto corretamente.'
            )
            exit( 1 )

        regex_cab = re.compile( regex_cabecalho )
        regex_cau = re.compile( regex_cauda )
        regex_cot = re.compile( regex_cotacao )

        for i, linha in enumerate( self.arquivo ):
            # Cabeçalho
            match = regex_cab.match( linha )

            # Cauda
            if match is None:
                match = regex_cau.match( linha )

            # Cotação
            if match is None:
                match = regex_cot.match( linha )

            if match is None:
                print(
                    'Linha {0} não corresponde a nenhum tipo de informação '
                    'relevante para o arquivo. A linha será dispensada e a '
                    'análise do arquivo prosseguirá a partir da linha '
                    'seguinte.'.format( i + 1 )
                )

                continue

            # Dicionário de informações
            dicionario = match.groupdict()

            for chave, valor in dicionario.items():
                if chave == 'ano_historico' and self.ano_historico is None:
                    self.ano_historico = int( valor )

                elif chave == 'data_criacao' and self.data_criacao is None:
                    self.data_criacao = datetime.strptime( valor, '%Y%m%d' )

                elif chave == 'num_registros':
                    self.num_registros = int( valor )

                elif chave == 'data_pregao':
                    self.data_pregao.append(
                        datetime.strptime( valor, '%Y%m%d' )
                    )

                elif chave == 'cod_bdi':
                    self.cod_bdi.append( valor.strip() )

                elif chave == 'cod_papel':
                    self.cod_papel.append( valor.strip() )

                elif chave == 'tp_merc':
                    self.tp_merc.append( valor.strip() )

                elif chave == 'nome_resum':
                    self.nome_resum.append( valor.strip() )

                elif chave == 'espec_papel':
                    self.espec_papel.append( valor.strip() )

                elif chave == 'prazo_dias_termo':
                    if valor.strip() is None or valor.strip() == '':
                        self.prazo_dias_termo.append( 0 )
                    else:
                        self.prazo_dias_termo.append(
                            int( valor.strip() )
                        )

                elif chave == 'moeda':
                    self.moeda.append( valor.strip() )

                elif chave == 'preco_abertura':
                    self.preco_abertura.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'preco_maximo':
                    self.preco_maximo.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'preco_minimo':
                    self.preco_minimo.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'preco_medio':
                    self.preco_medio.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'preco_ultimo':
                    self.preco_ultimo.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'preco_melhor_compra':
                    self.preco_melhor_compra.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'preco_melhor_venda':
                    self.preco_melhor_venda.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'num_negocios':
                    self.num_negocios.append(
                        float( valor.strip() )
                    )

                elif chave == 'qtde_titulos':
                    self.qtde_titulos.append(
                        float( valor.strip() )
                    )

                elif chave == 'vol_titulos':
                    self.vol_titulos.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'preco_exerc':
                    self.preco_exerc.append(
                        float( valor.strip() ) / 1e2
                    )

                elif chave == 'indicador_correcao':
                    self.indicador_correcao.append( valor.strip() )

                elif chave == 'data_vencimento':
                    self.data_vencimento.append(
                        datetime.strptime( valor, '%Y%m%d' )
                    )

                elif chave == 'fator_cotacao':
                    self.fator_cotacao.append(
                        int( valor.strip() )
                    )

                elif chave == 'preco_exerc_pontos':
                    self.preco_exerc_pontos.append(
                        float( valor.strip() ) / 100e6
                    )

                elif chave == 'cod_isi':
                    self.cod_isi.append( valor.strip() )

                elif chave == 'distribuicao_papel':
                    self.distribuicao_papel.append( valor.strip() )


    def exportar_csv( self, endereco_arquivo = None ):
        pass


    def exportar_sql(
        self,
        endereco_arquivo = None,
        nome_tabela = 'cotacoes',
        formato = 'PostgreSQL',
        filtros = None,
    ):
        if endereco_arquivo is None:
            print(
                'O endereço do arquivo não foi especificado. Especifique o '
                'endereço do arquivo e tente novamente.'
            )
            return

        # Formatos de SQL suportados
        if formato.lower() not in self.formato_sql:
            print(
                'O formato SQL não suporta comando INSERT para o Banco de '
                'Dados {0}. Selecione um dos seguintes formatos: {1}'.format(
                    formato,
                    self.formato_sql,
                )
            )

        # Endereço do arquivo
        endereco = endereco_arquivo

        # Adicionando a extensão *.sql caso não tenha sido especificada
        if not endereco.endswith( '.sql' ):
            endereco += '.sql'

        try:
            arquivo = open( file = endereco, mode = 'w', )

        except OSError:
            print(
                'Ocorreu um erro durante o processo de escrita do arquivo '
                '"{0}". Verifique se você possui permissão de escrita ou se '
                'o arquivo está aberto e tente novamente.'.format( endereco )
            )
            return

        arquivo.write(
            'INSERT INTO {0} ( '
            'data_pregao, cod_bdi, cod_papel, tp_merc, nome_resum, '
            'espec_papel, prazo_dias_termo, moeda, preco_abertura, '
            'preco_maximo, preco_minimo, preco_medio, preco_ultimo, '
            'preco_melhor_compra, preco_melhor_venda, num_negocios, '
            'qtde_titulos, vol_titulos, preco_exerc, indicador_correcao, '
            'data_vencimento, fator_cotacao, preco_exerc_pontos, cod_isi, '
            'distribuicao_papel ) '
            'VALUES\n'.format( nome_tabela )
        )


        for i, item in enumerate( self.data_pregao ):
            arquivo.write(
                '('
                '\'{0}\', '   # data_pregao
                '\'{1}\', '   # cod_bdi
                '\'{2}\', '   # cod_papel
                '\'{3}\', '   # tp_merc
                '\'{4}\', '   # nome_resum
                '\'{5}\', '   # espec_papel
                '{6}, '   # prazo_dias_termo
                '\'{7}\', '   # moeda
                '{8}, '       # preco_abertura
                '{9}, '       # preco_maximo
                '{10}, '      # preco_minimo
                '{11}, '      # preco_medio
                '{12}, '      # preco_ultimo
                '{13}, '      # preco_melhor_compra
                '{14}, '      # preco_melhor_venda
                '{15}, '      # num_negocios
                '{16}, '      # qtde_titulos
                '{17}, '      # vol_titulos
                '{18}, '      # preco_exerc
                '{19}, '      # indicador_correcao
                '\'{20}\', '  # data_vencimento
                '{21}, '      # fator_cotacao
                '\'{22}\', '  # preco_exerc_pontos
                '\'{23}\', '  # cod_isi
                '\'{24}\''    # distribuicao_papel
                ')'.format(
                    self.data_pregao[ i ].isoformat(),
                    self.cod_bdi[ i ],
                    self.cod_papel[ i ],
                    self.tp_merc[ i ],
                    self.nome_resum[ i ],
                    self.espec_papel[ i ],
                    self.prazo_dias_termo[ i ],
                    self.moeda[ i ],
                    self.preco_abertura[ i ],
                    self.preco_maximo[ i ],
                    self.preco_minimo[ i ],
                    self.preco_medio[ i ],
                    self.preco_ultimo[ i ],
                    self.preco_melhor_compra[ i ],
                    self.preco_melhor_venda[ i ],
                    self.num_negocios[ i ],
                    self.qtde_titulos[ i ],
                    self.vol_titulos[ i ],
                    self.preco_exerc[ i ],
                    self.indicador_correcao[ i ],
                    self.data_vencimento[ i ].isoformat(),
                    self.fator_cotacao[ i ],
                    self.preco_exerc_pontos[ i ],
                    self.cod_isi[ i ],
                    self.distribuicao_papel[ i ],
                )
            )

            if i < len( self.data_pregao ) - 1:
                arquivo.write( ',\n' )
            else:
                arquivo.write( ';' )

        arquivo.close()



    def exportar_xlsx( self, endereco_arquivo = None ):
        pass

    # --------------------------------------------------------------------------
    # Atributos
    # --------------------------------------------------------------------------
    arquivo = None
    endereco_arquivo = None

    ano_historico = None
    data_criacao = None
    num_registros = None

    data_pregao = []
    cod_bdi = []
    cod_papel = []
    tp_merc = []
    nome_resum = []
    espec_papel = []
    prazo_dias_termo = []
    moeda = []
    preco_abertura = []
    preco_maximo = []
    preco_minimo = []
    preco_medio = []
    preco_ultimo = []
    preco_melhor_compra = []
    preco_melhor_venda = []
    num_negocios = []
    qtde_titulos = []
    vol_titulos = []
    preco_exerc = []
    indicador_correcao = []
    data_vencimento = []
    fator_cotacao = []
    preco_exerc_pontos = []
    cod_isi = []
    distribuicao_papel = []
