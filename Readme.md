# Organização dos arquivos

* Bds: Os bancos de dados gerados
* mongo-db: Scripts para detectar registros com problemas no arquivo de bd mongo
* rest-api: Api para consulta dos dados obtidos das sumulas
* Scripts: Os códigos escritos para as atividades da primeira parte do projeto

# soccer-scraper

Scraper escrito em python para coletar e armazenar em um bd dados de jogos de fultebol do site betexplorer.

### Modo de usar

Após executar o arquivo main.py serão exibidas as opções de campeonatos disponíveis, você deve escolher uma das opções de 1-6:

* 1 - Premier League
* 2 - Serie A (Italy)
* 3 - Bundesliga
* 4 - LaLiga
* 5 - Ligue 1
* 6 - Série A (Brazil)

Digite a temporada que deseja começar (ex: 2020-2021), por último, digite o número de temporadas anteriores que deseja coletar (de forma retroativa).

### Arquivos

* db.py: contém as funções que criam/consultam/modificam o banco de dados.
* my_exceptions.py: possui uma exceção específica para informar falha ao adicionar um registro no banco de dados.
* scraper.py: contém a classe Scraper com as funções responsáveis por coletar os dados.
* main.py: contém a função principal utilizada para executar o programa.

### Requisitos

* beautifulsoup4
* requests
* selenium
* geckodriver
* firefox

_*As versões específicas de cada lib estão no arquivo requirements.txt._

### Observações

* É necessário passar o caminho do geckodriver.exe no arquivo scraper.py.

* Em caso de problemas verificar o arquivo scraper_log.txt que é gerado ao final de uma execução com falha.

### Arquitetura do BD

<p align="center">
<img width="847" height="795" src="imagens/db_logic.png">
</p>