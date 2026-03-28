
# AutoPrak-App

###### Apresentamos AutoPrak um protótipo para gerenciamento de estacionamento, que utiliza tecnologias RFID e ESP32 para um controle preciso de entrada e saída de veículos, integrado a um sistema web robusto desenvolvido em Python Flask com HTML, JavaScript e CSS. Este projeto redefine a eficiência e segurança na administração de estacionamentos.

###### Protótipo desenvolvido para trabalho de graduação Fatec de Cruzeiro-SP.

## Bibliotecas e Ferramentas

### Backend

* 🐍 [Python](https://www.python.org/)
* 🧪 [Flask](https://flask.palletsprojects.com/en/2.3.x/)
* ⚗️  [SQLAlchemy (Object Relational Mapper - ORM)](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

### Frontend
* [![HTML5](https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/HTML5_logo_and_wordmark.svg/50px-HTML5_logo_and_wordmark.svg.png)](https://developer.mozilla.org/en-US/docs/Glossary/HTML5)
* [![CSS Icon](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/CSS3_logo_and_wordmark.svg/50px-CSS3_logo_and_wordmark.svg.png)](https://developer.mozilla.org/en-US/docs/Web/CSS)
* [![JavaScript Icon](https://github.com/Djonatan01/AutoPark/assets/103201121/5f6f6e3b-3c7a-4af8-ab59-b5603657e9e0)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* [![Bootstrap Icon](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Bootstrap_logo.svg/50px-Bootstrap_logo.svg.png)](https://getbootstrap.com/)

## Organização do Projeto

* O protótipo foi desenvolvido usando o padrão Model-View-Controller (MVC):

#### Visão (Diretório que contém as classes para as atividades do protótipo)

* [Uusários](Src/View/User.py), [Tráfego](Src/View/Traffic.py), [Login](Src/View/Login.py), [Página Inicial](Src/View/Home.py) and [Sobre](Src/View/About.py)

#### Controlador (Métodos de ação)

* [Users](Src/Controller/Users.py), [Vagas](Src/Controller/Vagas.py) and [RFID](Src/Controller/RFID.py)


#### Modelo (A estrutura lógica de um banco de dados)
* Nosso sistema WEB é impulsionado por um único arquivo de banco de dados SQLite3, onde reside todas as entidades, tecendo uma teia intricada de dados com as tabelas e seus respectivos relacionamentos.
[BancoDados](Src/Model/BancoDados.py)

#### Configuração do Projeto
* Primeiro, crie um ambiente virtual para hospedar as dependências do projeto.
Instale as dependências necessárias com os seguintes comandos:

#### Linux:

```bash
cd ~/Documentos  # Navega até o diretório "Documents"

python3 -m venv .venv  # Cria um ambiente virtual chamado ".venv"
source .venv/bin/activate  # Ativa o ambiente virtual

pip install -r requirements.txt  # Instala as dependências listadas no arquivo "requirements.txt"
```

#### Windows:

```bash
cd C:\Users\SeuUsuario\Documentos  # Navega até o diretório "Documents"

python -m venv .venv  # Cria um ambiente virtual chamado ".venv"
.venv\Scripts\activate  # Ativa o ambiente virtual

pip install -r requirements.txt  # Instala as dependências listadas no arquivo "requirements.txt"

```

#### Então, inicialize o servidor da API:

```bash
python main.py
```

## Atualizações de segurança aplicadas

- Adicionado controle de acesso via `flask_login` em rotas críticas:
  - `User`: list, listCodUser, createUser, updateUser, removeUser
  - `vagas`: Cadastrar, cadastro, consultaVagas, reserva
  - `CartoesRFID`: cadastroCartao, atualizarCartao, ListCartao, FiltrarUser
- Implementado decorator `admin_required` em rotas de administração (somente `ADMIN` pode alterar usuários/vagas/cartões).
- Mantido `Traffic.list` com `login_required`, `Traffic.register` continua pública para integração RFID (se necessário).
- Recomendado: colocar `debug=False` em produção e usar variáveis de ambiente seguras (`SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`).