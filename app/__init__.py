from flask import Flask  # Importa a classe Flask do framework Flask
from app.routes import setup_routes  # Importa a função setup_routes do módulo app.routes, responsável por configurar as rotas
from app.config import Config  # Importa a classe Config do módulo app.config, que contém as configurações do aplicativo

app = Flask(__name__)  # Cria uma instância do aplicativo Flask.  __name__ é o nome do módulo atual.

# Carrega as configurações do aplicativo
app.config.from_pyfile('config.py')  # Carrega as configurações do arquivo config.py ou pode usar app.config.from_object(Config)  # Carrega as configurações da classe Config, sobrescrevendo as configurações de config.py (se houver conflitos)

# Configura as rotas da aplicação
setup_routes(app)  # Chama a função setup_routes para configurar as rotas do aplicativo