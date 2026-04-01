# 💻 Software para Comparação de Preços de Notebooks — TechHub

O **TechHub** é uma solução de software robusta desenvolvida para auxiliar usuários na análise técnica e financeira de notebooks. Através de uma interface moderna e intuitiva, a plataforma permite filtrar dispositivos por hardware específico, comparar faixas de preço e gerenciar uma base de conhecimento colaborativa através de comentários e notas técnicas.

---

## 🛠️ Pré-requisitos do Sistema

Antes de rodar o projeto, certifique-se de ter instalado em sua máquina:

1.  **Python 3.13+**: Linguagem base do projeto. [Download aqui](https://www.python.org/).
2.  **Git**: Para clonagem e controle de versão. [Download aqui](https://git-scm.com/).
3.  **Ambiente de Desenvolvimento**: Sugerido VS Code com extensão Python instalada.
4.  **Pip**: Gerenciador de pacotes do Python (instalado automaticamente com o Python).

---

## 🚀 Tecnologias e Ferramentas

* **Backend:** [Django 6.0.3](https://www.djangoproject.com/) (Framework Web de alto nível).
* **Frontend:** HTML5, CSS3 (Grid & Flexbox) e JavaScript Vanilla.
* **Banco de Dados:** SQLite3 (Persistência de avaliações e métricas).
* **Arquitetura:** MVT (Model-View-Template) com Camada de Serviço (Service Layer).

---

## 🛠️ Arquitetura e Funcionalidades

### 📂 Camadas do Sistema
* **`models.py`**: Define a estrutura do banco de dados para as avaliações (`notebook_id`, `texto`, `estrelas`).
* **`services.py`**: Camada de serviço que processa a lógica de hardware e implementa o **Fallback de Imagem**.
* **`views.py`**: Gerencia as requisições, filtros de busca e o cálculo da **Média Móvel**.

### 🌟 Diferenciais Técnicos
1.  **Lógica de Visibilidade de Novos Itens**: Notebooks sem avaliações ("Novos") ignoram as restrições de filtro de estrelas, garantindo que novos produtos entrem no fluxo de descoberta.
2.  **Layout de Detalhes Dinâmico**: Painel lateral (Drawer) que exibe especificações completas e badges de hardware sem necessidade de refresh na página.

---

## 🏃 Como Rodar o Projeto (Passo a Passo)

Siga exatamente estes comandos no seu terminal:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/techhub.git](https://github.com/seu-usuario/techhub.git)
    cd techhub
    ```

2.  **Crie o Ambiente Virtual (Isolamento):**
    ```bash
    python -m venv venv
    ```

3.  **Ative o Ambiente Virtual:**
    * **Windows:** `.\venv\Scripts\activate`
    * **Mac/Linux:** `source venv/bin/activate`

4.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Prepare o Banco de Dados (Migrações):**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Crie um Administrador (Opcional - para acessar /admin):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```
    Acesse: `http://127.0.0.1:8000/`

---

## 👤 Desenvolvedora

**Raquiel Ribeiro Alexandre**
* Graduanda em Engenharia de Software.
* Foco em Desenvolvimento Backend, APIs REST e Engenharia de Requisitos.
