# blog-maykol
Desenvolvimento de um simples blog contendo usuários e postagens
Projeto: Postagens de um Blog

Estrutura do Projeto

blog/
├── app/
│   ├── __init__.py        # Inicializa o Flask e configura o app
│   ├── routes.py          # Define as rotas da aplicação
│   ├── config.py          # Configurações da aplicação
│   ├── models/            # Conexões e interações com o Firebase
│   │   ├── firebase.py    # Operações com o banco de dados Firebase
│   ├── services/          # Lógica de negócios
│   │   ├── post_service.py
│   │   ├── user_service.py
│   ├── templates/         # Templates HTML
│   │   ├── home.html
│   │   ├── profile.html
│   │   ├── posts.html
├── run.py                 # Arquivo principal para rodar o app

Estrutura detalhada:
__init__.py Inicializa a aplicação Flask. É onde configuramos extensões (como Firebase) e registramos as rotas.
routes.py Define as rotas da aplicação, ou seja, as URLs que os usuários podem acessar e as funções associadas.
config.py Armazena configurações da aplicação, como chaves de API, configurações do Firebase, etc.
models/ Armazena a lógica de dados, como a comunicação com bancos de dados (firebase.py).
services/ Contém a lógica de negócios, separada do restante da aplicação. São os "cérebro" das funções, onde implementamos como os dados serão processados. post_service.py: Lida com operações relacionadas a "posts". user_service.py: Lida com operações relacionadas a “usuários".
templates/ Armazena os arquivos HTML da aplicação. Esses arquivos são usados para renderizar as páginas que o usuário vê no navegador.
run.py É o arquivo principal, onde a aplicação Flask será iniciada. Ele é responsável por rodar o servidor.

Instale todas as dependências via pip seguir:
flask
requests==1.1.0
firebase_admin
datetime

