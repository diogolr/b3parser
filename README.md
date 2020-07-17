# B3Parser
Um parser para os arquivos de histórico de cotações da B3

##### Exemplo de utilização (main.py)

```python
from b3parser import B3Parser

if __name__ == '__main__':
    cols_sel = [
        'data_pregao',
        'cod_bdi',
        'cod_papel',
        'tp_merc',
        'nome_resum',
        'espec_papel',
        'preco_ultimo',
        'fator_cotacao',
    ]

    cods_bdi = [
        '02',  # LOTE PADRÃO
        '12',  # FUNDOS IMOBILIÁRIOS
        '96',  # FRACIONÁRIO
    ]

    tps_merc = [
        '010',  # VISTA
        '020',  # FRACIONÁRIO
    ]

    filtros = {
       'cod_bdi': ( 'in', cods_bdi ),
       'tp_merc': ( 'in', tps_merc ),
    }

    ano = 2015

    parser = B3Parser( 'data/COTAHIST_A{0}.TXT'.format( ano ) )

    parser.ler_arquivo( cols_sel = cols_sel, filtros = filtros )

    parser.exportar_json( 'data/{0}.json'.format( ano ) )
    #parser.exportar_sql( 'data/{0}.sql'.format( ano ) )
    #parser.exportar_csv( 'data/{0}.csv'.format( ano ) )
```

##### Links úteis
###### Dependências
* [pymongo](https://github.com/mongodb/mongo-python-driver) - Driver MongoDb
* [psycopg2](https://www.psycopg.org/) - Driver PostgreSQL
* [tqdm](https://github.com/tqdm/tqdm) - Barra de progresso

###### Cotações históricas
* [Cotações Históricas](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/cotacoes-historicas/) - Busca por cotações históricas
* [Layout](http://www.b3.com.br/data/files/C8/F3/08/B4/297BE410F816C9E492D828A8/SeriesHistoricas_Layout.pdf) das cotações históricas

###### Arquivos de cotações históricas
* [Anuais](http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_AAAAA.ZIP): Formato `COTAHIST_A`**`AAAA`**`.ZIP`
* [Mensais](http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_MMMAAAA.ZIP) (*últimos 12 meses*): Formato `COTAHIST_M`**`MMAAAA`**`.ZIP`
* [Diárias](http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_DDDMMAAAA.ZIP) (*ano corrente*): Formato `COTAHIST_D`**`DDMMAAAA`**`.ZIP`

###### Títulos negociáveis
* [Títulos Negociáveis](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-a-vista/titulos-negociaveis/): Busca por títulos negociáveis
* [Títulos Negociados](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/arquivos-para-download/): Títulos negociados atualmente
* [Glossário](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/arquivos-para-download/glossario/) dos títulos negociáveis

###### Projetos similares no GitHub
* [Busca 1](https://github.com/search?utf8=%E2%9C%93&q=bovespa)
* [Busca 2](https://github.com/search?utf8=%E2%9C%93&q=bovespa+c)
