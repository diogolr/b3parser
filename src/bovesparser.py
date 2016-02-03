# -*- encoding: utf-8 -*-
import csv
import json
import locale
import operator
import re

from datetime import datetime
from bson import json_util
from pymongo import MongoClient
from src.linecount import rawbigcount
from src.regex import regex_cabecalho
from src.regex import regex_cauda
from src.regex import regex_cotacao
from tqdm import tqdm


class BovesParser( object ):
    # --------------------------------------------------------------------------
    # Atributos estáticos
    # --------------------------------------------------------------------------
    formato_sql = [
        'postgresql',
        'pgsql',
    ]

    operadores = {
        '==': operator.eq,
        '!=': operator.ne,
        '>=': operator.ge,
        '<=': operator.le,
        '>': operator.gt,
        '<': operator.le,
        'in': operator.contains,
    }

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
        self.num_linhas = rawbigcount( endereco_arquivo )


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


    def colunas( self ):
        return [
            'data_pregao',
            'cod_bdi',
            'cod_papel',
            'tp_merc',
            'nome_resum',
            'espec_papel',
            'prazo_dias_termo',
            'moeda',
            'preco_abertura',
            'preco_maximo',
            'preco_minimo',
            'preco_medio',
            'preco_ultimo',
            'preco_melhor_compra',
            'preco_melhor_venda',
            'num_negocios',
            'qtde_titulos',
            'vol_titulos',
            'preco_exerc',
            'indicador_correcao',
            'data_vencimento',
            'fator_cotacao',
            'preco_exerc_pontos',
            'cod_isi',
            'distribuicao_papel',
        ]


    def dados( self ):
        dados = []

        for i, item in enumerate( self.cols_sel ):
            dados.append( getattr( self, item ) )

        return dados


    def exportar_mongodb(
        self,
        usuario = None,
        senha = None,
        host = None,
        porta = None,
        banco_dados = None,
        colecao = None,
    ):
        '''
        Exporta os dados interpretados para um banco de dados MongoDB através
        do driver pymongo.

        "usuario": Nome do usuário que será utilizado para acessar o banco de
                   dados
        "senha": Senha do usuário que será utilizado para acessar o banco de
                 dados
        "host": Host em que se encontra o banco de dados
        "porta": Porta de conexão com o host do banco de dados
        "banco_dados": Nome do banco de dados que será acessado
        "colecao": Nome da coleção em que os dados serão inseridos
        '''

        # Dados
        array = []

        print( 'Exportando para o MongoDB...' )

        for i, linha in enumerate( zip( *self.dados() ) ):
            dicionario = {}

            for j, item in enumerate( linha ):
                dicionario[ self.cols_sel[ j ] ] = item

            array.append( dicionario )

        cliente = MongoClient(
            'mongodb://'
            '{usuario}'
            ':'
            '{senha}'
            '@'
            '{host}'
            ':'
            '{porta}'
            '/'
            '{banco_dados}'.format(
                usuario = usuario,
                senha = senha,
                host = host,
                porta = porta,
                banco_dados = banco_dados,
            )
        )

        db = cliente[ banco_dados ]
        colecao = db[ colecao ]

        return colecao.insert_many( array )


    def exportar_csv(
        self,
        endereco_arquivo = None,
        delimitador = ';',
        quote = '|',
        incluir_cabecalho = True,
    ):
        '''
        Exporta os dados interpretados para o formato CSV.
        '''

        if endereco_arquivo is None:
            print(
                'O endereço do arquivo não foi especificado. Especifique o '
                'endereço do arquivo e tente novamente.'
            )
            return

        endereco = endereco_arquivo

        # Adicionando a extensão *.csv caso não tenha sido especificada
        if not endereco.endswith( '.csv' ):
            endereco += '.csv'

        try:
            arquivo = open(
                file = endereco, mode = 'w', newline = '', encoding = 'utf-8'
            )

        except OSError:
            print(
                'Ocorreu um erro durante o processo de escrita do arquivo '
                '"{0}". Verifique se você possui permissão de escrita ou se '
                'o arquivo está aberto e tente novamente.'.format( endereco )
            )
            return

        writer = csv.writer(
            arquivo,
            delimiter = delimitador,
            quotechar = quote,
            quoting = csv.QUOTE_MINIMAL
        )

        if incluir_cabecalho:
            writer.writerow( self.cols_sel )

        print( 'Exportando para o formato CSV...' )

        barra_progresso = tqdm(
            iterable = False,
            total = len( getattr( self, self.cols_sel[0] ) )
        )

        for item in zip( *self.dados() ):
            writer.writerow( item )
            barra_progresso.update()

        arquivo.close()
        barra_progresso.close()


    def exportar_json(
        self,
        endereco_arquivo = None,
    ):
        '''
        Exporta os dados interpretados para o formato JSON.
        '''

        if endereco_arquivo is None:
            print(
                'O endereço do arquivo não foi especificado. Especifique o '
                'endereço do arquivo e tente novamente.'
            )
            return

        endereco = endereco_arquivo

        # Adicionando a extensão *.json caso não tenha sido especificada
        if not endereco.endswith( '.json' ):
            endereco += '.json'

        try:
            arquivo = open(
                file = endereco, mode = 'w', newline = '', encoding = 'utf-8'
            )

        except OSError:
            print(
                'Ocorreu um erro durante o processo de escrita do arquivo '
                '"{0}". Verifique se você possui permissão de escrita ou se '
                'o arquivo está aberto e tente novamente.'.format( endereco )
            )
            return

        array = []

        print( 'Exportando para o formato JSON...' )

        barra_progresso = tqdm(
            iterable = False,
            total = len( getattr( self, self.cols_sel[0] ) )
        )

        for i, linha in enumerate( zip( *self.dados() ) ):
            dicionario = {}

            for j, item in enumerate( linha ):
                dicionario[ self.cols_sel[ j ] ] = item

            array.append( dicionario )
            barra_progresso.update()

        json.dump( array, arquivo, indent = 2, default = json_util.default )

        arquivo.close()
        barra_progresso.close()


    def exportar_sql(
        self,
        endereco_arquivo = None,
        nome_tabela = 'cotacoes',
        formato = 'PostgreSQL',
    ):
        '''
        Exporta os dados interpretados para o formato SQL de acordo com o
        formato de banco de dados.
        '''

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
            arquivo = open( file = endereco, mode = 'w', encoding = 'utf-8' )

        except OSError:
            print(
                'Ocorreu um erro durante o processo de escrita do arquivo '
                '"{0}". Verifique se você possui permissão de escrita ou se '
                'o arquivo está aberto e tente novamente.'.format( endereco )
            )
            return

        # PostgreSQL
        if formato.lower() == 'postgresql' or formato.lower() == 'pgsql':
            arquivo.write(
                'INSERT INTO {0} ({1}) '
                'VALUES\n'.format(
                    nome_tabela,
                    ','.join( self.cols_sel )
                )
            )

            dados = list( zip( *self.dados() ) )

            print( 'Exportando para o formato SQL (PostgreSQL)...' )

            for i, linha in tqdm(
                enumerate( dados ), total = len( dados )
            ):
                string = '({0})'

                substring = ''

                for j, item in enumerate( linha ):
                    substring += '{0}{1}{2}'

                    if self.cols_sel[ j ] in [
                        'data_pregao',
                        'cod_bdi',
                        'cod_papel',
                        'tp_merc',
                        'nome_resum',
                        'espec_papel',
                        'moeda',
                        'data_vencimento',
                        'preco_exerc_pontos',
                        'cod_isi',
                        'distribuicao_papel',
                    ]:
                        substring = substring.format( '\'', item, '\'' )

                    else:
                        substring = substring.format( '', item, '' )

                    if j < len( linha ) - 1:
                        substring += ','

                string = string.format( substring )

                arquivo.write( string )

                if i < len( dados ) - 1:
                    arquivo.write( ',\n' )
                else:
                    arquivo.write( ';' )

        arquivo.close()


    def exportar_xlsx( self, endereco_arquivo = None ):
        pass


    def ler_arquivo( self, cols_sel = None, filtros = None ):
        '''
        Lê o arquivo configurado no construtor do objeto de acordo com os
        cols_sel selecionados.

        "cols_sel": Lista com os nomes das colunas que devem ser consideradas.
                    Se a lista não for configurada, serão consideradas todas as
                    colunas pré-configuradas (ver método colunas()).
        "filtros": Dicionário contendo os filtros que serão aplicados em cada
                   uma das colunas selecionadas. Exemplo:
                       filtros = {
                           'preco_ultimo': ( '>=', 10 ),
                           'preco_minimo': ( '<', 2 ),
                           'cod_bdi': ( 'in', [ '02', '96' ] ),
                           'tp_merc': ( 'in', [ '010' ] ),
                       }
        '''
        if self.arquivo is None:
            print(
                'O arquivo não foi aberto corretamente.'
            )
            exit( 1 )

        # Configuração do padrão de hora local
        # Windows --------------------------------------------------------------
        # https://msdn.microsoft.com/en-us/library/39cwe7zf(vs.71).aspx
        # http://msdn.microsoft.com/en-us/library/cdax410z%28VS.71%29.aspx
        locale.setlocale( locale.LC_ALL, 'ptb' )

        regex_cab = re.compile( regex_cabecalho )
        regex_cau = re.compile( regex_cauda )
        regex_cot = re.compile( regex_cotacao )

        # Determinando as colunas que serão filtradas
        self.cols_sel = self.colunas()

        if cols_sel is not None:
            lista = self.colunas()

            for i, item in enumerate( lista ):
                if item not in cols_sel:
                    del self.cols_sel[ self.cols_sel.index( item ) ]

        print( 'Lendo o arquivo...' )

        # Lendo o arquivo
        for i, linha in enumerate(
            tqdm(
                self.arquivo,
                total = self.num_linhas,
            )
        ):
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

            # Selecionando as colunas
            for chave, valor in dicionario.items():
                if (
                    chave == 'ano_historico' and
                    self.ano_historico is None
                ):
                    self.ano_historico = int( valor )

                elif (
                    chave == 'data_criacao' and
                    self.data_criacao is None
                ):
                    self.data_criacao = datetime.strptime( valor, '%Y%m%d' )

                elif chave == 'num_registros':
                    self.num_registros = int( valor )

                elif (
                    chave == 'data_pregao' and
                    'data_pregao' in self.cols_sel
                ):
                    self.data_pregao.append(
                        datetime.strptime( valor, '%Y%m%d' )
                    )

                elif (
                    chave == 'cod_bdi' and
                    'cod_bdi' in self.cols_sel
                ):
                    self.cod_bdi.append( valor.strip() )

                elif (
                    chave == 'cod_papel' and
                    'cod_papel' in self.cols_sel
                ):
                    self.cod_papel.append( valor.strip() )

                elif (
                    chave == 'tp_merc' and
                    'tp_merc' in self.cols_sel
                ):
                    self.tp_merc.append( valor.strip() )

                elif (
                    chave == 'nome_resum' and
                    'nome_resum' in self.cols_sel
                ):
                    self.nome_resum.append( valor.strip() )

                elif (
                    chave == 'espec_papel' and
                    'espec_papel' in self.cols_sel
                ):
                    self.espec_papel.append( valor.strip() )

                elif (
                    chave == 'prazo_dias_termo' and
                    'prazo_dias_termo' in self.cols_sel
                ):
                    if valor.strip() is None or valor.strip() == '':
                        self.prazo_dias_termo.append( 0 )
                    else:
                        self.prazo_dias_termo.append(
                            int( valor.strip() )
                        )

                elif (
                    chave == 'moeda' and
                    'moeda' in self.cols_sel
                ):
                    self.moeda.append( valor.strip() )

                elif (
                    chave == 'preco_abertura' and
                    'preco_abertura' in self.cols_sel
                ):
                    self.preco_abertura.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'preco_maximo' and
                    'preco_maximo' in self.cols_sel
                ):
                    self.preco_maximo.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'preco_minimo' and
                    'preco_minimo' in self.cols_sel
                ):
                    self.preco_minimo.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'preco_medio' and
                    'preco_medio' in self.cols_sel
                ):
                    self.preco_medio.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'preco_ultimo' and
                    'preco_ultimo' in self.cols_sel
                ):
                    self.preco_ultimo.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'preco_melhor_compra' and
                    'preco_melhor_compra' in self.cols_sel
                ):
                    self.preco_melhor_compra.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'preco_melhor_venda' and
                    'preco_melhor_venda' in self.cols_sel
                ):
                    self.preco_melhor_venda.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'num_negocios' and
                    'num_negocios' in self.cols_sel
                ):
                    self.num_negocios.append(
                        float( valor.strip() )
                    )

                elif (
                    chave == 'qtde_titulos' and
                    'qtde_titulos' in self.cols_sel
                ):
                    self.qtde_titulos.append(
                        float( valor.strip() )
                    )

                elif (
                    chave == 'vol_titulos' and
                    'vol_titulos' in self.cols_sel
                ):
                    self.vol_titulos.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'preco_exerc' and
                    'preco_exerc' in self.cols_sel
                ):
                    self.preco_exerc.append(
                        float( valor.strip() ) / 1e2
                    )

                elif (
                    chave == 'indicador_correcao' and
                    'indicador_correcao' in self.cols_sel
                ):
                    self.indicador_correcao.append( valor.strip() )

                elif (
                    chave == 'data_vencimento' and
                    'data_vencimento' in self.cols_sel
                ):
                    self.data_vencimento.append(
                        datetime.strptime( valor, '%Y%m%d' )
                    )

                elif (
                    chave == 'fator_cotacao' and
                    'fator_cotacao' in self.cols_sel
                ):
                    self.fator_cotacao.append(
                        int( valor.strip() )
                    )

                elif (
                    chave == 'preco_exerc_pontos' and
                    'preco_exerc_pontos' in self.cols_sel
                ):
                    self.preco_exerc_pontos.append(
                        float( valor.strip() ) / 100e6
                    )

                elif (
                    chave == 'cod_isi' and
                    'cod_isi' in self.cols_sel
                ):
                    self.cod_isi.append( valor.strip() )

                elif (
                    chave == 'distribuicao_papel' and
                    'distribuicao_papel' in self.cols_sel
                ):
                    self.distribuicao_papel.append( valor.strip() )

        # Aplicando os filtros
        print( 'Aplicando os filtros...' )

        linhas_remover = []

        for chave, ( operador, valor_filtro ) in filtros.items():
            # Verifica se a chave está entre as colunas selecionadas e se o
            # operador do filtro é um dos operadores possíveis (self.operadores)
            if (
                chave not in self.cols_sel or
                operador not in self.operadores
            ):
                print(
                    'A chave "{0}" não foi selecionada no parâmetro '
                    '"cols_cel" ou o operador "{1}"" não é um operador '
                    'válido. O filtro será ignorado.'.format(
                        chave,
                        operador,
                    )
                )

                continue

            print(
                '\tColuna {0}: Operador "{1}" com valor(es) de filtro '
                '{2}.'.format(
                    chave,
                    operador,
                    valor_filtro
                )
            )

            barra_progresso = tqdm(
                total = len( getattr( self, chave ) )
            )

            # Percorre os itens da coluna selecionada pela chave
            for i, item in enumerate( getattr( self, chave ) ):
                resultado = None

                if operador == 'in':
                    resultado = self.operadores[ operador ](
                        valor_filtro, item
                    )
                else:
                    resultado = self.operadores[ operador ](
                        item, valor_filtro
                    )

                if not resultado:
                    linhas_remover.append( i )

                barra_progresso.update()

            barra_progresso.close()

        print( 'Removendo as linhas não desejadas...' )
        barra_progresso = tqdm(
            total = (
                len( self.cols_sel ) *
                len( getattr( self, self.cols_sel[ 0 ] ) )
            )
        )

        # Removendo a referencia das linhas duplicadas na lista de linhas à
        # remover
        linhas_remover = set( linhas_remover )

        for col in self.cols_sel:
            coluna = getattr( self, col )

            nova_coluna = []

            for i in range( len( coluna ) ):
                if i not in linhas_remover:
                    nova_coluna.append( coluna[ i ] )

                barra_progresso.update()

            setattr( self, col, nova_coluna )

        barra_progresso.close()


    # --------------------------------------------------------------------------
    # Atributos
    # --------------------------------------------------------------------------
    arquivo = None
    endereco_arquivo = None
    num_linhas = None

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

    cols_sel = []
