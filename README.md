# Social Network API - Back-end

Esta é a API RESTful para o projeto de Rede Social, desenvolvida com Python, Django e Django Rest Framework. Ela serve como a base para todas as funcionalidades da aplicação.

**API em Produção:** [https://jhowjhow.pythonanywhere.com/](https://jhowjhow.pythonanywhere.com/)

---

## Como Usar

Existem duas maneiras de executar este projeto: localmente para desenvolvimento ou acedendo ao servidor de produção.

### 1. Executar Localmente

Siga os passos abaixo para configurar e executar o projeto no seu ambiente de desenvolvimento.

**Pré-requisitos:**
* Python 3.10+
* Git

**Passos:**
1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Jhowbrows/final_project_social_back.git]
    cd final_project_social_back
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

### 2. Usar o Servidor de Produção (PythonAnywhere)

A API já está com deploy e acessível publicamente no PythonAnywhere. O front-end da aplicação deve ser configurado para fazer pedidos para o seguinte URL base:
`https://jhowjhow.pythonanywhere.com/api/`

Este servidor está configurado com um webhook para **Implantação Contínua (Continuous Deployment)**. Qualquer `push` para a branch `main` irá acionar uma atualização automática do servidor.

---

## Documentação da API

A API inclui endpoints para:
* **Autenticação:** Registo (`/register/`) e Login (`/login/`).
* **Perfis:** Ver e atualizar o perfil do utilizador (`/users/me/`), alterar a senha, nome de usuario e a foto de perfil.
* **Sistema Social:** Listar seguidores (`/users/`), seguir e deixar de seguir.
* **Posts:** Criar posts (`/posts/`), curtir e comentar.
* **Feed:** Obter um feed personalizado com os posts dos usuarios seguidos (`/feed/`).