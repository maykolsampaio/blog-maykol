import firebase_admin  # Importa o módulo firebase_admin para interagir com o Firebase.
from app.config import Config  # Importa a classe Config do módulo app.config, que contém as configurações do aplicativo.
from firebase_admin import credentials, firestore  # Importa submódulos credentials e firestore de firebase_admin.
from datetime import datetime  # Importa o módulo datetime para trabalhar com datas e horários.

# Inicialização do Firebase
cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)  # Cria um objeto de credencial a partir do arquivo especificado em Config.FIREBASE_CREDENTIALS.
firebase_admin.initialize_app(cred)  # Inicializa o aplicativo Firebase usando as credenciais fornecidas.
db = firestore.client()  # Cria um cliente Firestore para interagir com o banco de dados.

# Definindo as coleções
users_collection = Config.USERS_COLLECTION  # Define a variável users_collection com o nome da coleção de usuários, buscando do objeto Config.
posts_collection = Config.POSTS_COLLECTION  # Define a variável posts_collection com o nome da coleção de posts, buscando do objeto Config.

# Funções relacionadas aos usuários

def get_users():
    """
    Obtém todos os usuários da coleção 'users' no Firestore.

    Retorna:
        dict: Um dicionário onde as chaves são os IDs dos documentos dos usuários
              e os valores são os dados de cada usuário (dicionários).
    """
    users_ref = db.collection(users_collection)  # Obtém uma referência para a coleção de usuários.
    docs = users_ref.stream()  # Obtém um stream de documentos (usuários) da coleção.
    users = {}  # Inicializa um dicionário para armazenar os usuários.
    for doc in docs:  # Itera sobre cada documento (usuário) no stream.
        user_data = doc.to_dict()  # Converte o documento para um dicionário.
        users[doc.id] = user_data  # Adiciona o dicionário do usuário ao dicionário 'users', usando o ID do documento como chave.
    return users  # Retorna o dicionário contendo todos os usuários.

def get_user(username):
    """
    Obtém os dados de um usuário específico da coleção 'users' com base no nome de usuário.

    Args:
        username (str): O nome de usuário do usuário a ser obtido.

    Retorna:
        dict: Um dicionário contendo os dados do usuário, ou None se o usuário não for encontrado.
    """
    user_ref = db.collection(users_collection).document(username)  # Obtém uma referência para o documento do usuário específico na coleção.
    doc = user_ref.get()  # Obtém o documento do usuário.
    if doc.exists:  # Verifica se o documento existe.
        user_data = doc.to_dict()  # Converte o documento para um dicionário.
        return user_data  # Retorna os dados do usuário.
    else:
        return None  # Retorna None se o usuário não for encontrado.

def create_or_update_user(username, data):
    """
    Cria um novo usuário ou atualiza um usuário existente na coleção 'users'.

    Args:
        username (str): O nome de usuário do usuário a ser criado ou atualizado.
        data (dict): Um dicionário contendo os dados do usuário a serem armazenados.
    """
    user_ref = db.collection(users_collection).document(username)  # Obtém uma referência para o documento do usuário específico na coleção.
    user_ref.set(data)  # Define os dados do usuário no documento. Se o documento já existir, ele será sobrescrito.

def delete_user(username):
    """
    Exclui um usuário da coleção 'users'.

    Args:
        username (str): O nome de usuário do usuário a ser excluído.
    """
    user_ref = db.collection(users_collection).document(username)  # Obtém uma referência para o documento do usuário específico na coleção.
    user_ref.delete()  # Exclui o documento do usuário.

# Funções relacionadas aos posts

def get_posts():
    """
    Obtém todos os posts da coleção 'posts' no Firestore.

    Retorna:
        dict: Um dicionário onde as chaves são os IDs dos documentos dos posts
              e os valores são os dados de cada post (dicionários).
    """
    posts_ref = db.collection(posts_collection)  # Obtém uma referência para a coleção de posts.
    docs = posts_ref.stream()  # Obtém um stream de documentos (posts) da coleção.
    posts = {}  # Inicializa um dicionário para armazenar os posts.
    for doc in docs:  # Itera sobre cada documento (post) no stream.
        posts[doc.id] = doc.to_dict()  # Converte o documento para um dicionário e adiciona ao dicionário 'posts', usando o ID do documento como chave.
    return posts  # Retorna o dicionário contendo todos os posts.

def get_post(post_id):
    """
    Obtém um post específico da coleção 'posts' com base no ID do post.

    Args:
        post_id (str): O ID do post a ser obtido.

    Retorna:
        dict: Um dicionário contendo os dados do post, ou None se o post não for encontrado.
    """
    post_ref = db.collection(posts_collection).document(post_id)  # Obtém uma referência para o documento do post específico na coleção.
    doc = post_ref.get()  # Obtém o documento do post.
    if doc.exists:  # Verifica se o documento existe.
        post_data = doc.to_dict()  # Converte o documento para um dicionário.
        return post_data  # Retorna os dados do post.
    else:
        return None  # Retorna None se o post não for encontrado.

def get_user_posts(username):
    """
    Obtém todos os posts de um usuário específico da coleção 'posts'.

    Args:
        username (str): O nome de usuário do autor dos posts a serem obtidos.

    Retorna:
        dict: Um dicionário onde as chaves são os IDs dos documentos dos posts
              e os valores são os dados de cada post (dicionários).
    """
    posts_ref = db.collection(posts_collection)  # Obtém uma referência para a coleção de posts.
    query = posts_ref.where("author", "==", username)  # Cria uma consulta para filtrar os posts, obtendo apenas aqueles onde o autor corresponde ao nome de usuário fornecido.
    docs = query.stream()  # Executa a consulta e obtém um stream de documentos (posts) que correspondem aos critérios.
    posts = {}  # Inicializa um dicionário para armazenar os posts.
    for doc in docs:  # Itera sobre cada documento (post) no stream.
        posts[doc.id] = doc.to_dict()  # Converte o documento para um dicionário e adiciona ao dicionário 'posts', usando o ID do documento como chave.
    return posts  # Retorna o dicionário contendo os posts do usuário especificado.

def create_post(author, title, content):
    """
    Cria um novo post na coleção 'posts'.

    Args:
        author (str): O nome de usuário do autor do post.
        title (str): O título do post.
        content (str): O conteúdo do post.
    """
    post_ref = db.collection(posts_collection).document()  # Cria uma referência para um novo documento (com ID automático) na coleção de posts.
    now = datetime.now().isoformat()  # Obtém a data e hora atual em formato ISO 8601.
    post_ref.set({  # Define os dados do novo post no documento.
        'author': author,  # Define o autor do post.
        'title': title,  # Define o título do post.
        'content': content,  # Define o conteúdo do post.
        'created_at': now  # Define a data de criação do post.
    })

def update_post(post_id, title, content):
    """
    Atualiza um post existente na coleção 'posts'.

    Args:
        post_id (str): O ID do post a ser atualizado.
        title (str): O novo título do post.
        content (str): O novo conteúdo do post.
    """
    post_ref = db.collection(posts_collection).document(post_id)  # Obtém uma referência para o documento do post específico na coleção.
    now = datetime.now().isoformat()  # Obtém a data e hora atual em formato ISO 8601.
    post_ref.update({  # Atualiza os dados do post no documento.
        'title': title,  # Atualiza o título do post.
        'content': content,  # Atualiza o conteúdo do post.
        'updated_at': now  # Define a data de atualização do post.
    })

def delete_post(post_id):
    """
    Exclui um post da coleção 'posts'.

    Args:
        post_id (str): O ID do post a ser excluído.
    """
    post_ref = db.collection(posts_collection).document(post_id)  # Obtém uma referência para o documento do post específico na coleção.
    post_ref.delete()  # Exclui o documento do post.