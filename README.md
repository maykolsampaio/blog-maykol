# blog-maykol
Desenvolvimento de um simples blog contendo usuários e postagens
Projeto: Postagens de um Blog

````
├── app/ # Diretório principal da aplicação Flask
│ ├── init.py # Inicializa o aplicativo Flask e configura o app
│ ├── routes.py # Define as rotas da aplicação
│ ├── config.py # Configurações da aplicação
│ ├── models/ # Conexões e interações com o Firebase
│ │ └── firebase.py # Operações com o banco de dados Firebase (Firestore)
│ ├── services/ # Camada de lógica de negócios
│ │ ├── post_service.py # Serviços relacionados a posts (criação, leitura, atualização, exclusão)
│ │ └── user_service.py # Serviços relacionados a usuários (autenticação, gerenciamento de perfil)
│ └── templates/ # Diretório contendo os templates HTML da aplicação
│ ├── home.html # Template para a página inicial
│ ├── profile.html # Template para a página de perfil do usuário
│ └── posts.html # Template para exibir posts
│
└── run.py # Arquivo principal para iniciar a aplicação Flask
````

**Explicação dos Diretórios e Arquivos:**

*   **`app/`:** Este diretório contém todos os arquivos relacionados à aplicação Flask.

    *   **`__init__.py`:** Este arquivo é o ponto de entrada do pacote `app`. Ele inicializa o aplicativo Flask, configura as extensões e registra as rotas.

    *   **`routes.py`:** Este arquivo define as rotas da aplicação, associando URLs a funções que lidam com as requisições. Ele também lida com o rendering de templates e a manipulação de dados.

    *   **`config.py`:** Este arquivo contém as configurações da aplicação, como a chave secreta, as credenciais do banco de dados e outras variáveis de ambiente.

    *   **`models/`:** Este diretório contém os modelos de dados, que representam as entidades da aplicação.

        *   **`firebase.py`:** Este arquivo contém a lógica para interagir com o banco de dados Firebase (Firestore), como funções para criar, ler, atualizar e deletar dados.

    *   **`services/`:** Este diretório contém os serviços da aplicação, que encapsulam a lógica de negócios.

        *   **`post_service.py`:** Este arquivo contém a lógica para lidar com posts, como criar, ler, atualizar e deletar posts.

        *   **`user_service.py`:** Este arquivo contém a lógica para lidar com usuários, como autenticação, gerenciamento de perfil e outras operações relacionadas a usuários.

    *   **`templates/`:** Este diretório contém os templates HTML da aplicação.

        *   **`home.html`:** Template para a página inicial.

        *   **`profile.html`:** Template para a página de perfil do usuário.

        *   **`posts.html`:** Template para exibir posts.

*   **`run.py`:** Este arquivo é o ponto de entrada principal da aplicação. Ele importa a instância do aplicativo Flask do pacote `app` e inicia o servidor de desenvolvimento.



## Requisitos

*   Python 3.7+
*   Firebase Admin SDK
*   Flask
*   Werkzeug

## Instalação

1.  Clone o repositório:

    ```bash
    git clone https://github.com/maykolsampaio/blog-maykol.git
    cd blog-projeto
    ```

2.  Crie um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv venv
    venv\Scripts\activate  # Se for Windows
    source venv/bin/activate  # Se for Linux/macOS
    ```

3.  Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

    (Certifique-se de ter um arquivo `requirements.txt` listando as dependências)

4.  Configure as credenciais do Firebase:

    *   Crie um projeto no Firebase Console.
    *   Gere um arquivo de chave de conta de serviço (serviceAccountKey.json).
    *   Defina a variável de ambiente em config.py ` FIREBASE_CREDENTIALS` para apontar para o caminho do arquivo.

    ```bash
     FIREBASE_CREDENTIALS="/caminho/para/serviceAccountKey.json"
    ```

## Execução

```bash
python run.py

Acesse a aplicação no seu navegador em http://localhost:5000.

