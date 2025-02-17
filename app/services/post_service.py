from app.models import firebase  # Importa o módulo firebase do pacote app.models

class PostService:
    """
    Classe que fornece serviços relacionados a posts, como buscar, criar, atualizar e deletar.
    """

    def __init__(self):
        """
        Inicializa o PostService com uma referência ao módulo firebase.
        """
        self.fb = firebase  # Referência ao módulo firebase

    def get_all_posts(self):
        """
        Obtém todos os posts, ordenados pela data de criação (mais recente primeiro).

        Retorna:
            dict: Um dicionário onde as chaves são os IDs dos posts e os valores são os dados dos posts.
                  Ordenado pela data de criação, do mais recente para o mais antigo.
        """
        posts = self.fb.get_posts()  # Obtém todos os posts do Firebase
        # Ordenando os posts pela data de criação, do mais recente para o mais antigo
        # Certifique-se de que 'created_at' exista e seja comparável
        # Além disso, 'created_at' agora é um objeto Timestamp do Firestore
        return dict(sorted(posts.items(), key=lambda item: item[1]['created_at'], reverse=True))  # Ordena os posts pela data de criação e retorna

    def get_post(self, post_id):
        """
        Obtém um post específico pelo ID.

        Args:
            post_id (str): O ID do post a ser obtido.

        Retorna:
            dict: Um dicionário contendo os dados do post, ou None se o post não for encontrado.
        """
        all_posts = self.get_all_posts()  # Obtém todos os posts
        if post_id in all_posts:  # Verifica se o post com o ID especificado existe
            return all_posts[post_id]  # Retorna os dados do post
        else:
            return None  # Retorna None se o post não for encontrado

    def get_user_posts(self, username):
        """
        Obtém todos os posts de um usuário específico.

        Args:
            username (str): O nome de usuário do autor dos posts.

        Retorna:
            dict: Um dicionário onde as chaves são os IDs dos posts e os valores são os dados dos posts
                  do usuário especificado.
        """
        # Retorna os posts de um usuário específico
        return self.fb.get_user_posts(username)  # Obtém os posts do usuário do Firebase

    def create_post(self, author, title, content):
        """
        Cria um novo post.

        Args:
            author (str): O nome de usuário do autor do post.
            title (str): O título do post.
            content (str): O conteúdo do post.

        Retorna:
            str: O ID do novo post criado.
        """
        # Criação do post no Firestore
        post_id = self.fb.create_post(author, title, content)  # Cria o post no Firebase e obtém o ID
        return post_id  # Retorna o ID do post

    def update_post(self, post_id, title, content):
        """
        Atualiza um post existente.

        Args:
            post_id (str): O ID do post a ser atualizado.
            title (str): O novo título do post.
            content (str): O novo conteúdo do post.

        Retorna:
            bool: True se a atualização for bem-sucedida.
        """
        self.fb.update_post(post_id, title, content)  # Atualiza o post chamando o método do fb
        return True  # Retorna True para indicar sucesso

    def delete_post(self, post_id):
        """
        Deleta um post.

        Args:
            post_id (str): O ID do post a ser deletado.
        """
        # Deleta o post com o ID fornecido
        self.fb.delete_post(post_id)  # Deleta o post chamando o método do fb