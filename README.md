# 🐍 Academia Dev Python

> Um sistema completo de gestão acadêmica desenvolvido com Django, DRF e Docker

Bem-vindo! Este projeto foi criado como parte do Desafio Técnico Python/Django para o Estágio 2026.1. Aqui você encontrará uma solução completa para gerenciar alunos, cursos e matrículas, com API REST robusta, interface administrativa intuitiva e relatórios dinâmicos.

## 📌 Tecnologias Utilizadas

- **Python 3.12** - Linguagem base do projeto
- **Django 6.0** - Framework web poderoso e escalável
- **Django Rest Framework** - Construção de APIs RESTful
- **PostgreSQL 15** - Banco de dados relacional (containerizado)
- **Docker & Docker Compose** - Ambiente de desenvolvimento isolado e reproduzível
- **Bootstrap 5** - Interface responsiva e moderna

## 🚀 Como Rodar o Projeto

### Pré-requisitos

Certifique-se de ter instalado:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1️⃣ Iniciando a aplicação

Clone o repositório e navegue até a pasta do projeto, então execute:

```bash
docker compose up --build
```

O container `web` irá automaticamente:
1. ✅ Aguardar o PostgreSQL estar pronto
2. ✅ Executar as migrações do banco (`python manage.py migrate`)
3. ✅ Iniciar o servidor Django em http://localhost:8000

### 2️⃣ Acessando a aplicação

| Serviço | URL |
|---------|-----|
| 🏠 Dashboard | http://localhost:8000 |
| 📊 Relatório SQL | http://localhost:8000/reports/sql/ |
| 👤 Histórico do Aluno | http://localhost:8000/students/`<id>`/history/ |
| 🔌 API | http://localhost:8000/api/ |
| ⚙️ Admin | http://localhost:8000/admin/ |


## 🧪 Como Testar a Aplicação

### 1️⃣ Subir o Projeto

```bash
docker compose up --build
```

Aguarde até ver a mensagem indicando que o servidor está rodando em `http://0.0.0.0:8000`.

### 2️⃣ Criar um Superusuário

Em outro terminal, execute:

```bash
docker compose exec web python manage.py createsuperuser
```

Preencha os dados solicitados (username, email e senha).

### 3️⃣ Acessar a Área Administrativa

Abra o navegador e acesse:
```
http://localhost:8000/admin/
```

Faça login com as credenciais criadas no passo anterior.

### 4️⃣ Criar Dados de Teste

No Django Admin, cadastre:

**Alunos:**
- Nome completo, email, CPF e data de matrícula

**Cursos:**
- Nome, carga horária, valor da matrícula
- ✅ Marque o curso como **ativo**

**Matrículas:**
- Vincule alunos aos cursos
- Status inicial: **pending**

### 5️⃣ Testar a API com cURL

**Listar todos os alunos:**
```bash
curl http://localhost:8000/api/students/
```

**Listar todos os cursos:**
```bash
curl http://localhost:8000/api/courses/
```

**Listar todas as matrículas:**
```bash
curl http://localhost:8000/api/enrollments/
```

**Criar uma nova matrícula:**
```bash
curl -X POST http://localhost:8000/api/enrollments/ \
  -H "Content-Type: application/json" \
  -d '{"student": 1, "course": 1}'
```

### 6️⃣ Marcar Matrícula como Paga

```bash
curl -X POST http://localhost:8000/api/enrollments/1/mark_as_paid/
```

> Substitua `1` pelo ID da matrícula que deseja marcar como paga.

### 7️⃣ Acessar o Relatório SQL

Abra no navegador:
```
http://localhost:8000/reports/sql/
```

Você verá o relatório financeiro com os totais pagos e devidos por aluno.

### 8️⃣ Visualizar Histórico do Aluno

```
http://localhost:8000/students/1/history/
```

> Substitua `1` pelo ID do aluno que deseja visualizar.

Esta página mostrará todas as matrículas do aluno, valores pagos e pendentes.
