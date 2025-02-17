from flask import render_template, request, redirect, url_for, session  # Importa funções do Flask para lidar com rotas, templates, requisições e sessões
from app.services.post_service import PostService  # Importa a classe PostService para lidar com a lógica de posts
from app.services.user_service import UserService  # Importa a classe UserService para lidar com a lógica de usuários
from werkzeug.security import generate_password_hash, check_password_hash  # Importa funções para lidar com segurança de senhas

user_service = UserService()  # Cria uma instância do serviço de usuário
post_service = PostService()  # Cria uma instância do serviço de post

def setup_routes(app):
    """
    Configura as rotas do aplicativo Flask.

    Args:
        app: A instância do aplicativo Flask.
    """

    @app.route('/')
    def home():
        """
        Rota para a página inicial.
        Exibe uma lista de posts e mensagens.
        """
        posts = post_service.get_all_posts()  # Obtém todos os posts usando o serviço de post
        return render_template('home.html',  # Renderiza o template 'home.html'
                               message=request.args.get('message'),  # Passa a mensagem da query string para o template
                               message_type=request.args.get('message_type'),  # Passa o tipo de mensagem da query string para o template
                               logged=session.get('logged'),  # Passa o status de login para o template
                               posts=posts)  # Passa os posts para o template

    @app.route('/login', methods=['POST'])
    def login():
        """
        Rota para o processo de login.
        Verifica as credenciais do usuário e cria uma sessão se as credenciais forem válidas.
        """
        users = user_service.get_all_users()  # Obtém todos os usuários usando o serviço de usuário
        username = request.form.get('username')  # Obtém o nome de usuário do formulário
        password = request.form.get('password')  # Obtém a senha do formulário
        print(f"Tentativa de login com username: {username}, password: {password}")  # Imprime as credenciais para debug (REMOVER EM PRODUÇÃO)
        user = users.get(username)  # Obtém o usuário com base no nome de usuário

        if user:  # Se o usuário for encontrado
            print(f"Usuário encontrado: {user}")  # Imprime os dados do usuário para debug (REMOVER EM PRODUÇÃO)
            stored_password_hash = user.get('password')  # Obtém o hash da senha armazenada
            if stored_password_hash:  # Se o hash da senha estiver armazenado
                print(f"Hash da senha armazenada: {stored_password_hash}")  # Imprime o hash da senha para debug (REMOVER EM PRODUÇÃO)
                is_correct = check_password_hash(stored_password_hash, password)  # Verifica se a senha fornecida corresponde ao hash armazenado
                print(f"Senha correta: {is_correct}")  # Imprime o resultado da verificação para debug (REMOVER EM PRODUÇÃO)

                if is_correct:  # Se a senha for correta
                    session.update({  # Atualiza os dados da sessão
                        'username': username,  # Armazena o nome de usuário na sessão
                        'info_user': user['info'],  # Armazena as informações do usuário na sessão
                        'type': user['type'],  # Armazena o tipo de usuário na sessão
                        'logged': True,  # Define o status de login como True na sessão
                        'admin': (username == 'admin')  # Define se o usuário é um administrador na sessão
                    })
                    return redirect(url_for('profile', message=f"Seja bem-vindo, {user['info']['nome']}!", message_type='success'))  # Redireciona para a página de perfil com uma mensagem de boas-vindas
                else:
                    print("Senha incorreta!")  # Imprime uma mensagem de erro para debug (REMOVER EM PRODUÇÃO)
            else:
                print("Senha não definida para este usuário!")  # Imprime uma mensagem de erro para debug (REMOVER EM PRODUÇÃO)
        else:
            print("Usuário não encontrado!")  # Imprime uma mensagem de erro para debug (REMOVER EM PRODUÇÃO)

        return redirect(url_for('home', message='Credenciais inválidas. Tente novamente!', message_type='danger'))  # Redireciona para a página inicial com uma mensagem de erro

    @app.route('/profile')
    def profile():
        """
        Rota para a página de perfil do usuário.
        Exibe informações do usuário e seus posts (se estiver logado).
        """
        if 'username' not in session:  # Se o usuário não estiver logado
            return redirect(url_for('home', message='Faça login primeiro!', message_type='warning'))  # Redireciona para a página inicial com uma mensagem de aviso

        users = user_service.get_all_users() if session.get('admin') else None  # Obtém todos os usuários se o usuário for um administrador
        posts = post_service.get_user_posts(session['username']) if session['logged'] and session['type'] != 'Visitante' else None  # Obtém os posts do usuário se estiver logado e não for um visitante

        return render_template('profile.html',  # Renderiza o template 'profile.html'
                               users=users,  # Passa os usuários para o template
                               message=request.args.get('message'),  # Passa a mensagem da query string para o template
                               message_type=request.args.get('message_type'),  # Passa o tipo de mensagem da query string para o template
                               posts=posts)  # Passa os posts para o template

    @app.route('/excluir/<username>')
    def excluir(username):
        """
        Rota para excluir um usuário (somente para administradores).
        """
        if session.get('admin'):  # Se o usuário for um administrador
            user_service.delete_user(username)  # Exclui o usuário usando o serviço de usuário
            return redirect(url_for('profile', message=f'Usuário {username} excluído com sucesso!', message_type='success'))  # Redireciona para a página de perfil com uma mensagem de sucesso
        return redirect(url_for('profile', message='Permissão negada!', message_type='danger'))  # Redireciona para a página de perfil com uma mensagem de erro

    @app.route('/alterar/<username>', methods=['POST', 'PUT'])
    def alterar(username):
        """
        Rota para alterar os dados de um usuário (somente para administradores).
        """
        if session.get('admin') and user_service.get_user(username):  # Se o usuário for um administrador e o usuário existir
            user_service.create_or_update_user(username, request.form)  # Atualiza os dados do usuário usando o serviço de usuário
            return redirect(url_for('profile', message=f'Usuário {username} atualizado com sucesso!', message_type='success'))  # Redireciona para a página de perfil com uma mensagem de sucesso
        return redirect(url_for('profile', message='Usuário não encontrado!', message_type='danger'))  # Redireciona para a página de perfil com uma mensagem de erro

    @app.route('/inserir', methods=['POST'])
    def inserir():
        """
        Rota para inserir um novo usuário (somente para administradores).
        """
        if session.get('admin'):  # Se o usuário for um administrador
            user_service.create_or_update_user(request.form.get('username'), request.form)  # Cria um novo usuário usando o serviço de usuário
            return redirect(url_for('profile', message='Usuário inserido com sucesso!', message_type='success'))  # Redireciona para a página de perfil com uma mensagem de sucesso
        return redirect(url_for('profile', message='Permissão negada!', message_type='danger'))  # Redireciona para a página de perfil com uma mensagem de erro

    @app.route('/logout')
    def logout():
        """
        Rota para o processo de logout.
        Limpa a sessão do usuário.
        """
        session.clear()  # Limpa a sessão
        return redirect(url_for('home', message='Você saiu com sucesso!', message_type='success'))  # Redireciona para a página inicial com uma mensagem de sucesso

    @app.route('/posts/create', methods=['GET', 'POST'])
    def create_post():
        """
        Rota para criar um novo post (somente para usuários logados que não são visitantes).
        """
        if not session.get('logged') or session['type'] == 'Visitante':  # Se o usuário não estiver logado ou for um visitante
            return redirect(url_for('home', message='Você precisa estar logado para criar posts!', message_type='warning'))  # Redireciona para a página inicial com uma mensagem de aviso

        if request.method == 'POST':  # Se a requisição for do tipo POST
            title = request.form.get('title')  # Obtém o título do formulário
            content = request.form.get('content')  # Obtém o conteúdo do formulário
            author = session['username']  # Obtém o nome de usuário da sessão

            post_service.create_post(author, title, content)  # Cria um novo post usando o serviço de post
            return redirect(url_for('profile', message='Post criado com sucesso!', message_type='success'))  # Redireciona para a página de perfil com uma mensagem de sucesso

        return render_template('create_post.html')  # Renderiza o template 'create_post.html'

    @app.route('/posts/edit/<post_id>', methods=['GET', 'POST'])
    def edit_post(post_id):
        """
        Rota para editar um post existente (somente para o autor do post).
        """
        if not session.get('logged'):  # Se o usuário não estiver logado
            return redirect(url_for('home', message='Você precisa estar logado para editar posts!', message_type='warning'))  # Redireciona para a página inicial com uma mensagem de aviso
        if session['type'] == 'Visitante':  # Se o usuário for um visitante
            return redirect(url_for('home', message='Visitantes não podem editar posts!', message_type='warning'))  # Redireciona para a página inicial com uma mensagem de aviso

        user_posts = post_service.get_user_posts(session['username'])  # Obtém os posts do usuário usando o serviço de post
        post = user_posts.get(post_id)  # Obtém o post com base no ID

        if not post or post['author'] != session['username']:  # Se o post não existir ou o usuário não for o autor
            return redirect(url_for('profile', message='Você não tem permissão para editar este post!', message_type='danger'))  # Redireciona para a página de perfil com uma mensagem de erro

        if request.method == 'POST':  # Se a requisição for do tipo POST
            title = request.form.get('title')  # Obtém o título do formulário
            content = request.form.get('content')  # Obtém o conteúdo do formulário

            if post_service.update_post(post_id, title, content):  # Atualiza o post usando o serviço de post
                return redirect(url_for('profile', message='Post atualizado com sucesso!', message_type='success'))  # Redireciona para a página de perfil com uma mensagem de sucesso
            else:
                return redirect(url_for('profile', message='Erro ao atualizar o post!', message_type='danger'))  # Redireciona para a página de perfil com uma mensagem de erro

        return render_template('edit_post.html', post=post, post_id=post_id)  # Renderiza o template 'edit_post.html'

    @app.route('/posts/delete/<post_id>')
    def delete_post(post_id):
        """
        Rota para deletar um post existente (somente para o autor do post).
        """
        if not session.get('logged'):  # Se o usuário não estiver logado
            return redirect(url_for('home', message='Você precisa estar logado para deletar posts!', message_type='warning'))  # Redireciona para a página inicial com uma mensagem de aviso
        if session['type'] == 'Visitante':  # Se o usuário for um visitante
            return redirect(url_for('home', message='Visitantes não podem deletar posts!', message_type='warning'))  # Redireciona para a página inicial com uma mensagem de aviso

        post_service.delete_post(post_id)  # Deleta o post usando o serviço de post
        return redirect(url_for('profile', message='Post deletado com sucesso!', message_type='success'))  # Redireciona para a página de perfil com uma mensagem de sucesso

    @app.route('/user/<username>')
    def user_posts(username):
        """
        Rota para exibir os posts de um usuário específico.
        """
        user = user_service.get_user(username)  # Obtém o usuário usando o serviço de usuário
        if not user:  # Se o usuário não for encontrado
            return redirect(url_for('home', message='Usuário não encontrado!', message_type='danger'))  # Redireciona para a página inicial com uma mensagem de erro
        posts = post_service.get_user_posts(username)  # Obtém os posts do usuário usando o serviço de post
        return render_template('user_posts.html', username=username, posts=posts)  # Renderiza o template 'user_posts.html'

    @app.route('/post/<post_id>')
    def post_detail(post_id):
        """
        Rota para exibir os detalhes de um post específico.
        """
        post = post_service.get_post(post_id)

        if not post:
            return redirect(url_for('home', message='Post não encontrado!', message_type='danger'))
        return render_template('post_detail.html', post_id=post_id, post=post)

    @app.route('/reset_admin_password', methods=['GET'])  # Remova o método POST e mude para GET
    def reset_admin_password():
        """
        REMOVA ISSO ANTES DE IMPLANTAR EM PRODUÇÃO!
        Redefine a senha do usuário 'admin' para 'admin'.
        APENAS PARA USO EM DESENVOLVIMENTO LOCAL.
        """
        admin_username = 'admin'  # Adapte, caso o nome do usuário admin seja outro
        new_password = 'admin'
        hashed_password = generate_password_hash(new_password)

        # Atualize o usuário no banco de dados diretamente (evitando o serviço)
        # Isso é um atalho PERIGOSO para essa situação emergencial
        from app.models import firebase  # Importe aqui para evitar dependência cíclica

        firebase.db.collection(firebase.users_collection).document(admin_username).update({'password': hashed_password})

        print("SENHA DO ADMIN REDEFINIDA PARA 'admin'!")
        return redirect(url_for('home', message='Senha do admin redefinida para "admin". REMOVA ESSA ROTA!', message_type='warning'))