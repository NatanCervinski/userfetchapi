# UserFetchAPI

UserFetchAPI é uma aplicação de exemplo criada com **FastAPI** e **SQLAlchemy** que consome a API do **Random User Generator**, armazena dados em um banco de dados relacional (SQLite ou MySQL) e oferece endpoints para consultar os dados.

## Funcionalidades

- **Obter 100 usuários aleatórios** da API Random User Generator.
- **Armazenar os usuários no banco de dados**, com suporte a **SQLite** ou **MySQL**.
- Endpoints para buscar usuários por **gênero** e **idade**.

## Requisitos

- **Python 3.10+**
- **[Poetry](https://python-poetry.org/)** (para gerenciar dependências e ambientes virtuais)

## Instalação

Siga estas instruções para configurar e rodar o projeto localmente.

### 1. Clone o repositório

```bash
git clone https://github.com/NatanCervinski/UserFetchAPI.git
cd UserFetchAPI
```

### 2. Instale o Poetry

Se ainda não tiver o Poetry instalado, rode o seguinte comando:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3.Após instalar o Poetry, rode o seguinte script:

```bash
chmod +x install.sh
./install.sh
```
Durante a execução, você será solicitado a:

   - Escolher o banco de dados (SQLite ou MySQL).
   - Informar os detalhes da conexão com o banco de dados (se MySQL for escolhido).
   - Definir o número de usuários para popular o banco de dados (padrão 100).

### 4. Execute o servidor FastAPI

Após a instalação e configuração, você pode iniciar o servidor FastAPI:
```bash
poetry run uvicorn userfetchapi.main:app --reload
```
O servidor estará disponível em [localhost:8000](http://127.0.0.1:8000).

A documentação da API estará disponível em [localhost:8000/docs](http://127.0.0.1:8000/docs).


