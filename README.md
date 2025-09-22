# Social Network API - Back-end

Esta é a API RESTful para o projeto de Rede Social, desenvolvida com Python, Django e Django Rest Framework.

**[Acesse a API online aqui](https://jhowjhow.pythonanywhere.com/)**

---

## Como Rodar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Jhowbrows/Final_project_social_back.git]
    cd Final_project_social_back
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplique as migrações e rode os testes:**
    ```bash
    python manage.py migrate
    python manage.py test
    ```

5.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```
    A API estará acessível em `http://127.0.0.1:8000/`.

---

## Documentação da API

### Autenticação
* `POST /api/users/register/` - Cadastro de novo utilizador.
* `POST /api/login/` - Login, retorna o token de autenticação.

### Perfis e Utilizadores
* `GET /api/users/me/` - Exibe os detalhes do perfil do utilizador logado.
* `PATCH /api/users/me/` - Atualiza o perfil (nome, foto).
* `POST /api/users/me/change-password/` - **(NOVO)** Altera a senha do utilizador. Requer `old_password` e `new_password`.
* `GET /api/users/` - Lista todos os utilizadores.
* `POST /api/users/{id}/follow/` - Seguir um utilizador.
* `POST /api/users/{id}/unfollow/` - Deixar de seguir um utilizador.

### Postagens e Feed
* `POST /api/posts/` - Criar um novo post.
* `GET /api/feed/` - Aceder ao feed de notícias personalizado.
* `POST /api/posts/{id}/like/` - Curtir ou descurtir um post.
* `POST /api/posts/{id}/comment/` - Adicionar um comentário a um post.