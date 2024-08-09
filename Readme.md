![logo medicar](https://i.postimg.cc/DZNPJSxk/Logo.png "logo medicar")
# Desafio Medicar  [ Backend ]
Descrição: Teste prático Intemed Backend

Autor: Eymard Neto ( [linkedin](https://www.linkedin.com/in/eymard-neto-216254207) )

# Tecnologias

- Backend
    - Python 3.12.4
    - Django 5.0.7
- Database
    - PostgresSql 16

# Pré-requisitos para Setup

- Git
- Docker
- Docker Compose


## Setup Backend
Este guia irá ajudá-lo a configurar e executar a aplicação backend em um ambiente Docker.

### 1. Clonar o repositório e atualizar arquivo de ambiente
Clone o repositório e navegue até a pasta `app`:

```bash
git clone <https://github.com/franciscoeymardneto/intmed-back.git>
cd app
```

Entre na pasta *app* e atualize o arquivo .env conforme necessário, veja o exemplo:

```bash
DEBUG=True
SECRET_KEY='django-insecure-rnt8312h=6^-nyf@&-ryd0ei+%34g1w04n2y4ne=ps8++8znto'
POSTGRES_DB=dev_db
POSTGRES_USER=tst_user
POSTGRES_PASSWORD=389ea411-db80-4af8-82fc-57912fa47d8f
DATABASE_HOST=db
DATABASE_PORT=5432
```

### 2. Levantar Containers
Volte para a raiz da pasta backend e execute o comando para iniciar os containers:

```bash
cd ..
docker compose up -d --build
```

Espere até que o build seja concluído e todos os containers estejam em execução.

### 3. Executar Migrações
Após os containers estarem ativos, execute as migrações do banco de dados:

```bash
docker compose exec api python manage.py makemigrations
docker compose exec api python manage.py migrate
```

### 4. Executar Testes
Para garantir que tudo esteja funcionando corretamente, execute os testes:

```bash
docker compose exec api python manage.py test intmed_api.tests
```

Neste ponto, a aplicação já estará rodando e funcional.

### 5. Criação do Superusuário
Agora, crie o superusuário do Django com as credenciais desejadas, ele será necessário para acessar o menu
de Admin do django para cadastrar Medicos, Agendas e os dados necessários para a aplicação:

```bash
docker compose exec api python manage.py createsuperuser
```

### 6. Acessos

- Acesse o painel de administração do Django através do endereço: http://localhost:8000/admin
- Acesse a documentação Swagger dos endpoints através do endereço: http://localhost:8000/swagger

## Setup Frontend

Para executar a aplicação frontend, siga as instruções clicando [Aqui!](https://github.com/franciscoeymardneto/intmed-front.git)