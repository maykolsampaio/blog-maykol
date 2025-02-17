import os  # Importa o módulo os, que fornece funções para interagir com o sistema operacional

class Config:
    """
    Classe que define as configurações do aplicativo.
    """

    SECRET_KEY = "ifpi2025"  # Define a chave secreta do aplicativo.  **IMPORTANTE:** Substitua isso por uma chave forte e aleatória em produção!

    # FIREBASE_URL = "https://post-login-dcd05-default-rtdb.firebaseio.com"  # Não é necessário para o Firestore
    # FIREBASE_API_KEY = "AIzaSyCLMLXRsLqzWPieFYUf-spO4-3YGeypj2I"  # Não é necessário para o Firestore
    # FIREBASE_EMAIL = "maykolsampaio@ifpi.edu.br"  # Não é necessário para o Firestore
    # Comentários: Essas configurações são para o Firebase Realtime Database, que não está sendo usado neste projeto.

    # Firestore Collection Names
    USERS_COLLECTION = "users"  # Define o nome da coleção de usuários no Firestore
    POSTS_COLLECTION = "posts"  # Define o nome da coleção de posts no Firestore

    # For local use
    FIREBASE_CREDENTIALS = os.path.join(os.path.dirname(__file__), '/home/user/login-basico/post-login-dcd05-firebase-adminsdk-fbsvc-1222308305.json')  # Define o caminho para o arquivo de credenciais do Firebase (para uso local)
    # Explicação:  `os.path.join(os.path.dirname(__file__), ...)` constrói um caminho absoluto para o arquivo de credenciais,
    # garantindo que o aplicativo encontre o arquivo mesmo que seja executado de um diretório diferente.

    # FIREBASE_CREDENTIALS = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json') #Remove for production, set GOOGLE_APPLICATION_CREDENTIALS env variable
    # Comentários:
    # 1.  Essa linha é comentada porque é para uso local e deve ser removida antes da produção.
    # 2.  Em produção, a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS deve ser definida, apontando para o arquivo de credenciais.
    # 3. Usar variáveis de ambiente para gerenciar credenciais é uma prática mais segura do que incluir o arquivo diretamente no código.