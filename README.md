# 📊 Sistema ERP de Gestão de Vendas com Business Intelligence

> API REST escalável + Dashboard analítico para controle completo de estoque, vendas e métricas de negócio em tempo real.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Sobre o Projeto

Sistema completo de gestão empresarial desenvolvido com arquitetura de microserviços, permitindo controle de inventário, processamento de vendas e análise de dados em tempo real através de dashboards interativos.

**Ideal para:** Lojas de móveis, e-commerce, controle de estoque e análise de performance de vendas.

### 🌟 Funcionalidades Principais

- ✅ **API REST completa** para gestão de produtos, fabricantes, clientes e vendas
- 📊 **Dashboard BI interativo** com KPIs e métricas de negócio
- 🔔 **Alertas inteligentes** de estoque baixo
- 📈 **Análise de vendas** por categoria, cliente e fabricante
- 🐳 **Totalmente containerizado** - rode em qualquer ambiente
- 🗄️ **Migrations automatizadas** com versionamento de banco de dados

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11** - Linguagem de programação
- **FastAPI** - Framework web de alta performance
- **SQLAlchemy** - ORM para manipulação de dados
- **Alembic** - Controle de versão do banco de dados
- **PostgreSQL 15** - Banco de dados relacional

### Frontend (Dashboard BI)
- **Streamlit** - Framework para dashboards interativos
- **Plotly Express** - Visualizações e gráficos
- **Pandas** - Manipulação e análise de dados

### DevOps
- **Docker & Docker Compose** - Containerização
- **Uvicorn** - Servidor ASGI de alta performance

---

## 🚀 Como Instalar e Rodar

### Pré-requisitos

- Docker e Docker Compose instalados
- Git (para clonar o repositório)

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/AndersonDeOliveiraSoares/product_sale_fastapi.git
cd product_sale_fastapi
```

### Passo 2: Suba os Containers

```bash
docker-compose up --build
```

Aguarde alguns minutos enquanto os containers são construídos e iniciados.

### Passo 3: Execute as Migrations

Em outro terminal, rode:

```bash
docker-compose exec web_fastapi alembic upgrade head
```

### Passo 4: Popule o Banco com Dados de Exemplo

```bash
docker-compose exec web_fastapi python seed.py
```

Este comando criará:
- 10 fabricantes
- 100 produtos (10 por fabricante)
- 30 clientes
- 200 vendas com histórico dos últimos 60 dias

### Passo 5: Acesse as Aplicações

- **API FastAPI:** http://localhost:8001
- **Documentação Interativa (Swagger):** http://localhost:8001/docs
- **Dashboard BI:** http://localhost:8501

---

## 📁 Estrutura do Projeto

```
product_sale_fastapi/
├── app/
│   ├── models/           # Modelos de dados (ORM)
│   │   ├── manufacturer.py
│   │   ├── product.py
│   │   ├── customer.py
│   │   └── sale.py
│   ├── routes/           # Endpoints da API
│   ├── database.py       # Configuração do banco
│   └── main.py           # Aplicação principal
├── alembic/              # Migrations do banco de dados
├── dashboard.py          # Dashboard Streamlit (BI)
├── seed.py               # Script de população de dados
├── docker-compose.yml    # Orquestração dos containers
├── Dockerfile            # Imagem Docker customizada
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

---

## 🎨 Dashboard - Business Intelligence

O dashboard oferece visualizações em tempo real para apoio à tomada de decisão:

### 📊 KPIs Principais
- **Faturamento Total** - Receita acumulada com variação
- **Total de Vendas** - Quantidade de pedidos processados
- **Ticket Médio** - Valor médio por transação

### 📈 Análises Disponíveis
- Distribuição de vendas por categoria (gráfico pizza)
- Top 5 clientes por faturamento (gráfico barras)
- Ranking de fabricantes por volume
- Alerta de produtos com estoque baixo

---

## 🔌 Endpoints da API

A API segue o padrão REST e está documentada automaticamente via Swagger.

### Principais Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/products` | Lista todos os produtos |
| `POST` | `/api/v1/products` | Cria novo produto |
| `GET` | `/api/v1/customers` | Lista todos os clientes |
| `POST` | `/api/v1/sales` | Registra nova venda |
| `GET` | `/api/v1/analytics/kpis` | Retorna KPIs principais |
| `GET` | `/api/v1/analytics/sales-by-category` | Vendas por categoria |
| `GET` | `/api/v1/analytics/top-customers` | Top clientes |

**Documentação completa:** http://localhost:8001/docs

---

## 🗃️ Modelo de Dados

### Entidades Principais

```
Manufacturer (Fabricante)
  ├── id
  ├── name
  └── contact_email

Product (Produto)
  ├── id
  ├── name
  ├── category
  ├── price
  ├── stock_quantity
  └── manufacturer_id (FK)

Customer (Cliente)
  ├── id
  ├── name
  ├── email
  └── document

Sale (Venda)
  ├── id
  ├── customer_id (FK)
  ├── sale_date
  └── total_price

SaleItem (Item de Venda)
  ├── id
  ├── sale_id (FK)
  ├── product_id (FK)
  ├── quantity
  └── unit_price
```

### Relacionamentos
- `Manufacturer` 1:N `Product`
- `Customer` 1:N `Sale`
- `Sale` N:N `Product` (através de `SaleItem`)

---

## 🧪 Testando a API

### Exemplo: Criar um Produto

```bash
curl -X POST "http://localhost:8001/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cadeira Escritório Premium",
    "category": "Cadeira",
    "price": 899.90,
    "stock_quantity": 50,
    "manufacturer_id": 1
  }'
```

### Exemplo: Registrar uma Venda

```bash
curl -X POST "http://localhost:8001/api/v1/sales" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 5, "quantity": 1}
    ]
  }'
```

---

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

Edite o arquivo `docker-compose.yml` para personalizar:

```yaml
environment:
  - POSTGRES_DB=seu_banco
  - POSTGRES_USER=seu_usuario
  - POSTGRES_PASSWORD=sua_senha
```

### Alterar Portas

No `docker-compose.yml`:

```yaml
ports:
  - "8001:8001"  # API
  - "8501:8501"  # Dashboard
  - "5433:5432"  # PostgreSQL
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Melhorias Futuras

- [ ] Autenticação JWT para endpoints protegidos
- [ ] Testes unitários e de integração
- [ ] Sistema de notificações por email
- [ ] Exportação de relatórios em PDF
- [ ] API de previsão de demanda com Machine Learning
- [ ] Deploy automatizado com CI/CD

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Anderson de Oliveira Soares**

- GitHub: [@AndersonDeOliveiraSoares](https://github.com/AndersonDeOliveiraSoares)
- LinkedIn: [Anderson Soares]https://www.linkedin.com/in/anderson-oliveira-soares/)
- Email: a.o.soares@hotmail.com

---
