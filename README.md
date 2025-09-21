# Social Network API - Back-end

Esta é a API RESTful para o projeto de Rede Social, desenvolvida com Python, Django e Django Rest Framework.

**[Acesse a API online aqui](https://Jhowjhow.pythonanywhere.com/)**

---

## Como Rodar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/Jhowbrows/Final_project_social_back.git
    cd final_project_social_back
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  / venv/Scripts/activate  no windows
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