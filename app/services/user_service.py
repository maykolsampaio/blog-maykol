from app.models import firebase  # Importa o módulo firebase do pacote app.models
from werkzeug.security import generate_password_hash, check_password_hash  # Importa funções para hash de senhas

class UserService:
    """
    Classe que fornece serviços relacionados a usuários, como buscar, criar, atualizar e deletar.
    """

    def __init__(self):
        """
        Inicializa o UserService com uma referência ao módulo firebase.
        """
        self.fb = firebase  # Atribuindo o cliente do Firestore diretamente

    def get_all_users(self):
        """
        Obtém todos os usuários.

        Retorna:
            dict: Um dicionário onde as chaves são os nomes de usuário e os valores são os dados dos usuários.
        """
        # Retorna todos os usuários do Firebase
        return self.fb.get_users()  # Chama a função do firebase para obter os usuários

    def get_user(self, username):
        """
        Obtém os dados de um usuário específico.

        Args:
            username (str): O nome de usuário do usuário a ser obtido.

        Retorna:
            dict: Um dicionário contendo os dados do usuário, ou None se o usuário não for encontrado.
        """
        # Retorna os dados de um usuário específico
        return self.fb.get_user(username)  # Chama a função do firebase para obter o usuário

    def delete_user(self, username):
        """
        Deleta um usuário.

        Args:
            username (str): O nome de usuário do usuário a ser deletado.
        """
        # Deleta um usuário do Firebase
        self.fb.delete_user(username)  # Chama a função do firebase para deletar o usuário

    def create_or_update_user(self, username, data):
        """
        Cria um novo usuário ou atualiza um usuário existente.

        Args:
            username (str): O nome de usuário do usuário a ser criado ou atualizado.
            data (dict): Um dicionário contendo os dados do usuário.
                           Deve incluir 'tipo', 'nome', 'email', 'desc' (ou 'curso'/'area'/'cargo' dependendo do tipo),
                           e opcionalmente 'telefone' e 'password'.
        """
        # Determina o tipo de usuário e o campo dinâmico correspondente
        tipo = data.get("tipo")  # Obtém o tipo de usuário dos dados fornecidos
        chave_dinamica = {  # Define um dicionário para mapear tipos de usuário para campos dinâmicos
            "Aluno": "curso",  # Alunos têm um campo 'curso'
            "Professor": "area",  # Professores têm um campo 'area'
            "Visitante": "desc",  # Visitantes têm um campo 'desc'
            "Administrativo": "cargo",  # Administrativos têm um campo 'cargo'
            "Administrador": "cargo"   # Administradores têm um campo 'cargo'
        }.get(tipo, "desc")  # Obtém o campo dinâmico com base no tipo de usuário, usando 'desc' como padrão

        # Estrutura de dados do usuário
        user_data = {  # Cria um dicionário com a estrutura de dados do usuário
            "type": tipo,  # Define o tipo de usuário
            "info": {  # Define as informações do usuário
                "nome": data.get("nome"),  # Define o nome
                "email": data.get("email"),  # Define o email
                chave_dinamica: data.get("desc"),  # Define o campo dinâmico (curso/area/desc/cargo)
                "telefone": data.get("telefone", "Não informado")  # Define o telefone, usando "Não informado" como padrão
            }
        }

        # Só gerar a senha nova durante a criação de um novo usuário
        if 'password' in data:  # Verifica se uma senha foi fornecida nos dados
            user_data['password'] = generate_password_hash(data.get("password"))  # Criptografa a senha e a armazena

        # Cria ou atualiza o usuário no Firebase
        self.fb.create_or_update_user(username, user_data)  # Chama a função do firebase para criar ou atualizar o usuário