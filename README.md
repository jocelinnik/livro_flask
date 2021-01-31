# Livro Flask

Este é um simples repositório de estudo sobre o livro **Flask de A a Z**.

## Instalando o projeto

### Gerando um ambiente virtual Python

Crie um novo ambiente virtual Python, através do comando `virtualenv venv`. 
Em seguida, ative o seu ambiente virtual executando o arquivo binário, através de `venv\bin\activate` ou `./venv/bin/activate`.

### Instalando dependências do projeto

Para instalar as dependências do projeto, rode o comando `pip install -r requirements`. O PyPI vai ler o arquivo, que contém as informações sobre as dependências usadas, e instalar os módulos necessários.

### Gerando o banco de dados

O projeto usa o SQLite como banco de dados. Para gerar o banco de dados, rode os seguintes comandos, na ordem descrita:

* `python migrate.py db init`
* `python migrate.py db migrate`
* `python migrate.py db upgrade`

Serão gerados alguns diretórios:

* `database/`: nesse diretório estará o arquivo que representa o banco de dados usado no projeto
* `migrations/`: aqui estarão os arquivos de migração do banco de dados, usado pelo framework

## Rodando o projeto

Para rodar o projeto, primeiro você precisa definir uma variável de ambiente chamada **FLASK_ENV**, onde o seu valor será o ambiente onde estará sendo executado: *development*, *test* ou *production*. Para tanto, rode `export FLASK_ENV=/valor/` (Linux) ou `SET FLASK_ENV=/valor/` (Windows).
Agora, rode o projeto com o comando `python run.py`.
