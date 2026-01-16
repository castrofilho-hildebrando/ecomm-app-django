# E-commerce API – FastAPI

Este projeto faz parte de um **showcase de backends** desenvolvidos em:

* **Python** (FastAPI – este repositório)
* **JavaScript** (Node.js / Express)
* **Java** (Spring Boot)

O objetivo é demonstrar **boas práticas de arquitetura**, resiliência, testes e padrões modernos aplicados em diferentes stacks.

---

## Visão Geral

Esta API foi migrada de Django para FastAPI com foco em:

* **Clean Architecture**
* **DDD-friendly**
* **Alta coesão e baixo acoplamento**
* **Testabilidade**
* **Resiliência operacional**

### Por que FastAPI?

FastAPI é **muito mais desacoplado** do que Django.

Enquanto o Django:

* Impõe padrões rígidos
* Centraliza lógica no framework
* Incentiva *fat models* e *fat views*
* Dificulta Clean Architecture e DDD

O FastAPI:

* Não força estrutura
* Permite controllers extremamente finos
* Facilita inversão de dependência
* Funciona como **adaptador HTTP**, não como núcleo do sistema

> Em resumo:
> **Django quer que você siga o Django.**
> **FastAPI permite que você siga a sua arquitetura.**

---

## Arquitetura

Seguimos **Clean Architecture** de forma estrita.

```
app/
├── main.py                    # Entry point
├── domain/                    # Núcleo do sistema
│   ├── entities/             # Regras de negócio puras
│   ├── repositories/         # Contratos (interfaces)
│   └── errors/               # Exceções de domínio
├── application/              # Casos de uso
│   ├── use_cases/           # Regras de aplicação
│   └── dtos/                # DTOs
├── infrastructure/           # Detalhes técnicos
│   ├── db/                  # Conexão / transações
│   ├── orm/                 # SQLAlchemy models
│   ├── repositories/        # Implementações
│   ├── outbox/              # Event Outbox Pattern
│   ├── resilience/          # Circuit breaker, retry
│   └── chaos/               # Chaos testing
├── interfaces/               # Interface com o mundo externo
│   ├── api/                 # Controllers
│   │   ├── routes/
│   │   └── dependencies/
│   └── schemas/             # Pydantic
└── config/
```

---

## Padrões Implementados

### Clean Architecture

* Controllers sem regra de negócio
* UseCases isolados
* Domínio sem dependência de framework
* Inversão de dependência real

### Event Outbox Pattern

* Eventos gravados no banco
* Publicação assíncrona via worker
* Garantia de entrega
* Tolerante a falhas

### Resiliência

* **Retry exponencial**
* **Dead Letter Queue (DLQ)**
* **Circuit Breaker**
* **Rate limit**
* **Chaos testing**

### Transações

* Transaction manager assíncrono
* Commit/rollback centralizado
* Consistência garantida

---

## Testes

* 100% **unitários**
* Sem banco
* Mocks e stubs
* Foco em regra de negócio

```
tests/
├── use_cases/
├── chaos/
└── resilience/
```

Executar:

```bash
pytest -v
```

---

## Instalação

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configurar:

```bash
cp .env.example .env
```

Rodar:

```bash
uvicorn main:app --reload
```

---

## Docker

```bash
docker-compose up --build
```

---

## Principais Diferenças Django → FastAPI

| Tema               | Django  | FastAPI |
| ------------------ | ------- | ------- |
| Arquitetura        | Imposta | Livre   |
| Clean Architecture | Difícil | Natural |
| DDD                | Fricção | Fluido  |
| DI                 | Manual  | Nativa  |
| Async              | Parcial | Nativo  |
| Controllers        | Pesados | Finos   |

---

## Endpoints

### Auth

* `POST /api/auth/register`
* `POST /api/auth/login`

### Products

* `GET /api/products`
* `POST /api/products/create`

### Cart

* `POST /api/cart/add`
* `POST /api/cart/remove`

### Orders

* `POST /api/orders/checkout`
* `GET /api/orders/my`

### Admin

* `GET /api/admin/stats`

Swagger:

```
http://localhost:8000/docs
```

---

## Destaques Técnicos

* SQLAlchemy async
* JWT stateless
* DTOs desacoplados
* Workers assíncronos
* Event-driven ready
* Código enterprise-grade

---

## Objetivo do Projeto

Este repositório **não é apenas um CRUD**.

Ele demonstra:

* Arquitetura limpa em produção
* Resiliência real
* Observabilidade pronta
* Padrões usados em empresas grandes

---

## Outros backends do showcase

* Node.js (Express e MongoDB)
* Java (Spring Boot e MongoDB)

---

## Autor

Projeto desenvolvido como parte de um **portfólio profissional de arquitetura backend**.

