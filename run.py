from app import app  # Importa a instância do aplicativo Flask do pacote app
from app.config import Config  # Importa a classe Config do módulo app.config, que contém as configurações do aplicativo


if __name__ == '__main__':
    """
    Este bloco de código é executado apenas quando o script run.py é executado diretamente.
    Ele inicia o servidor de desenvolvimento do Flask.
    """
    app.secret_key = Config.SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True)  # Inicia o servidor de desenvolvimento do Flask
    #   - debug=True: Ativa o modo de depuração, que fornece informações de erro detalhadas e recarrega o servidor automaticamente quando o código é alterado.
    #     **IMPORTANTE:** Não use debug=True em produção!