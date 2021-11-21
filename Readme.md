# soccer-scraper

Scraper escrito em python para coletar dados de jogos de fultebol do site betexplorer.

### Modos de execução

O scraper possui dois modos de execução:
* 1 - Adicionar ao banco de dados novos dados
* 2 - Gerar um txt com os dados atuais no banco de dados

### Modo de usar

A partir do terminal de comando digitar o nome do aquivo principal e informar o modo de execução:

python main.py [1,2]

Caso o primeiro modo de execução tenha sido escolhido, digitar um número entre 1 - 5 que corresponda a um dos campeotanos listados:

* 1 - Premier League
* 2 - Serie A (Italy)
* 3 - Bundesliga
* 4 - LaLiga
* 5 - Ligue 1

Por último, digite o números de temporadas anteriores à temporada 2020-2021 que deseja coletar.

_*caso escolha o segundo modo execução, um arquivo matches.txt e um odds.txt serão criados no diretório em que o programa estiver localizado._

### Arquivos

* db.py: contém as funções que criam/consultam/modificam o banco de dados.
* my_exceptions.py: possui uma exceção específica para informar falha ao adicionar um registro no banco de dados.
* scraper.py: contém a classe Scraper.
* main.py: contém a função principal utilizada para executar o programa.

### Requisitos

* beautifulsoup4
* requests
* selenium

_*As versões específicas de cada lib estão no arquivo requirements.txt._

### Observações

* Em caso de problemas verificar o arquivo scraper_log.txt que é gerado ao final de uma execução com falha.