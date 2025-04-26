# Sistema de Pagamentos

### 🚀 Descrição
O **Sistema de Pagamentos** é uma aplicação web desenvolvida para gerenciar e otimizar o processo de vendas, produtos e pagamentos de clientes. A API REST foi projetada para permitir a gestão de produtos, clientes, pedidos e pagamentos, além de gerar relatórios de vendas e automatizar o envio de notificações por e-mail quando houver alteração de preços de produtos já adquiridos por um cliente.

### ⚡ Funcionalidades
- **Cadastro de Produtos e Clientes**: Gerenciamento completo dos dados dos produtos e clientes.
- **Pedido e Pagamento**: Criação e acompanhamento de pedidos, incluindo o status de pagamentos.
- **Notificação de Alteração de Preços**: Envio assíncrono de e-mails para clientes quando um produto adquirido tiver o preço alterado para um valor inferior.
- **Relatório de Vendas**: Geração de relatórios em PDF das vendas realizadas para um cliente, utilizando filtros por CNPJ ou Razão Social.

### 📋 Pré-requisitos
Antes de rodar o projeto, você precisa ter os seguintes itens instalados em seu ambiente de desenvolvimento:
- **Python 3.x**
- **Django 5.x**
- **Celery** para tarefas assíncronas
- **RabbitMQ** (ou Docker para rodar o RabbitMQ)
- **Redis** como broker para Celery
- **django.core.mail** para envio de e-mails
- **PostgreSQL** (ou outro banco de dados relacional de sua escolha)
- **Docker**: Para rodar o RabbitMQ.

### 🔧 Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/joaovitormessias/sistema-pagamentos.git
   cd sistema-pagamentos

2. **Crie e ative um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt

4. **Crie um arquivo ```.env``` para armazenar suas credenciais**
   ```bash
   EMAIL_HOST_USER='seu-email@gmail.com'
   EMAIL_HOST_PASSWORD='sua-senha'

5. **Rodar as migrações**
   ```bash
   python manage.py migrate

6. **Criar um super Superusuário** para acessar o painel administrativo do Django:
   ```bash
   python manage.py runserver

7. **Subir o servidor de desenvolvimento.** Lembre-se de consultar os endpoints para o acesso completo da API.
   ```bash
   python manage.py runserver

### 🐳 Uso do Docker
Para rodar o **RabbitMQ** e configurar o **Celery** em seu projeto, você pode usar o **Docker**. O **RabbitMQ** será utilizado como broker de mensagens para o **Celery**.

1. **Rodar o RabbitMQ com Docker.** Se você ainda não tem o RabbitMQ rodando, pode usar o seguinte comando para iniciar o RabbitMQ com o Docker:
   ```bash
   docker run -it --rm --name rabbitmq -p 15672:15672 rabbitmq:3.13-management

2. **Inicar o Celery Worker.**Inicie o worker do Celery, que irá processar as tarefas assíncronas:
   ```bash
   celery -A sistema_pagamentos.celery_app worker --loglevel=info -P gevent

### 📝 Documentação da API
A documentação da API foi configurada usando o **drf_spectacular** para gerar uma documentação automática e interativa.
- Acesse a documentação da API gerada automaticamente em:
  ```bash
    http://localhost:8000/api/swagger/

Essa URL irá fornecer uma interface interativa para testar e visualizar os endpoints da sua API.

### 🛠️ Tecnologias utilizadas

- **Django 5.x:** Framework web utilizado para desenvolvimento da API.

- **Celery:**: Utilizado para envio assíncrono de e-mails quando houver alteração de preços.

- **RabbitMQ:** Usado como broker de mensagens para Celery, gerenciado via Docker.

- **Redis:** Broker de mensagens utilizado pelo Celery.

- **SendGrid:** Serviço para envio de e-mails.

- **drf_spectacular:** Utilizado para gerar a documentação da API.

- **Django REST Framework (DRF):** Para construção de APIs RESTful.

- **JWT (JSON Web Token):** Usado para autenticação, através do pacote rest_framework_simplejwt.

- **Django Jazzmin:** Para uma interface de administração personalizada.

### 🧑‍💻 Autores

- **João Vitor Messias:** *Desenvolvedor Principal*

### 📄 Licença
Este projeto está sob a licença MIT - veja o arquivo LICENSE para detalhes.

### 🎁 Agradecimentos
- Agradecemos à comunidade do Django, Celery, RabbitMQ, DRF, e outras bibliotecas utilizadas, pela excelente documentação e suporte.
