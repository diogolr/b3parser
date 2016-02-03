# BovesParser
Um parser para os arquivos de histórico de cotações da BM&amp;F Bovespa

##### Dependências
* [pymongo](https://github.com/mongodb/mongo-python-driver) - Driver MongoDb
* [tqdm](https://github.com/tqdm/tqdm) - Barra de progresso

##### Links úteis
###### Cotações históricas
* [Cotações Históricas](http://www.bmfbovespa.com.br/pt-br/cotacoes-historicas/FormSeriesHistoricas.asp) - Busca por cotações históricas
* [Layout](http://www.bmfbovespa.com.br/pt-br/download/SeriesHistoricas_Layout.pdf) das cotações históricas

###### Arquivos de cotações históricas
* [Anuais](http://www.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_AYYYY.ZIP): Formato `COTAHIST_A`**`AAAA`**`.ZIP`
* [Mensais](http://www.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_MMMAAAA.ZIP) (*últimos 12 meses*): Formato `COTAHIST_M`**`MMAAAA`**`.ZIP`
* [Diárias](http://www.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_DDDMMAAAA.ZIP) (*ano corrente*): Formato `COTAHIST_D`**`DDMMAAAA`**`.ZIP`

###### Títulos negociáveis
* [Títulos Negociáveis](http://www.bmfbovespa.com.br/cias-listadas/titulos-negociaveis/BuscaTitulosNegociaveis.aspx): Busca por títulos negociáveis
* [Títulos Negociados](http://www.bmfbovespa.com.br/suplemento/ExecutaAcaoDownload.asp?arquivo=Titulos_Negociaveis.zip&server=L): Títulos negociados atualmente
* [Layout](http://www.bmfbovespa.com.br/suplemento/doc/Titulos_Negociaveis.PDF) dos títulos negociáveis

###### Projetos similares no GitHub
* [Busca 1](https://github.com/search?utf8=%E2%9C%93&q=bovespa)
* [Busca 2](https://github.com/search?utf8=%E2%9C%93&q=bovespa+c)
