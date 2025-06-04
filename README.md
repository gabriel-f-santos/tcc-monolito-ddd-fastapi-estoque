# README.md
# Sistema de Gerenciamento de Estoque

Sistema desenvolvido como TCC para comparação entre arquiteturas monolítica e microsserviços utilizando Domain-Driven Design (DDD).

## 🚀 Tecnologias Utilizadas

### Monolito
- **Framework**: FastAPI
- **Banco de Dados**: PostgreSQL + SQLAlchemy
- **Autenticação**: JWT (PyJWT)
- **Deploy**: EC2
- **Containerização**: Docker

### Microsserviços (Fase 2)
- **Compute**: AWS Lambda
- **Banco de Dados**: DynamoDB
- **API Gateway**: AWS API Gateway
- **IaC**: Terraform
- **Runtime**: Python 3.11

## 🏗️ Arquitetura

O sistema foi projetado seguindo os princípios do Domain-Driven Design (DDD) com 4 bounded contexts:

1. **Identity & Access Management** - Autenticação e autorização
2. **Inventory Management** - Gestão de produtos e estoque
3. **Reporting & Analytics** - Relatórios e análises

## 🛠️ Setup do Projeto

### Pré-requisitos
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/gabriel-f-santos/inventory-system.git
cd inventory-system
```

2. **Crie o ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements-dev.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Inicie os serviços com Docker:**
```bash
docker-compose up -d postgres redis
```

6. **Execute as migrações:**
```bash
alembic upgrade head
```

7. **Inicie a aplicação:**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
```

## 📊 Coleta de Dados para TCC

### Métricas Monitoradas

#### Performance
- Latência média de resposta (ms)
- Throughput (requests/segundo)
- P95/P99 de latência
- Disponibilidade (uptime %)

#### Recursos
- Uso de CPU (%)
- Uso de memória (MB)
- Conexões de banco de dados
- I/O de disco

#### Custos
- Custo por request
- Custo mensal de infraestrutura
- Custo por usuário ativo

### Ferramentas de Monitoramento
- **Prometheus**: Coleta de métricas
- **Grafana**: Visualização de dados
- **Locust**: Testes de carga
- **CloudWatch**: Métricas AWS (microsserviços)

## 🧪 Testes

### Executar todos os testes:
```bash
pytest
```

### Testes por categoria:
```bash
# Testes unitários
pytest tests/unit/ -m unit

# Testes de integração
pytest tests/integration/ -m integration

# Testes end-to-end
pytest tests/e2e/ -m e2e
```

### Coverage:
```bash
pytest --cov=src --cov-report=html
```

## 🚀 Deploy

### Monolito (EC2)
```bash
# Build da imagem Docker
docker build -t inventory-system .

# Deploy no EC2 (script automatizado)
bash scripts/deploy_ec2.sh
```

### Microsserviços (Lambda)
```bash
# Deploy com Terraform
cd terraform/
terraform init
terraform plan
terraform apply
```

## 📈 Resultados Preliminares

### Métricas Coletadas (Exemplo)

| Métrica | Monolito | Microsserviços |
|---------|----------|----------------|
| Latência média | 45ms | 120ms (cold start) / 25ms (warm) |
| Throughput | 1000 req/s | 800 req/s |
| Disponibilidade | 99.8% | 99.9% |
| Custo/mês (1k users) | $50 | $35 |

## 🔗 Endpoints da API

### Autenticação
- `POST /api/v1/auth/login` - Login do usuário
- `POST /api/v1/auth/register` - Registro de usuário
- `POST /api/v1/auth/refresh` - Refresh token

### Produtos
- `GET /api/v1/produtos` - Listar produtos
- `POST /api/v1/produtos` - Criar produto
- `GET /api/v1/produtos/{id}` - Buscar produto
- `PUT /api/v1/produtos/{id}` - Atualizar produto
- `DELETE /api/v1/produtos/{id}` - Remover produto

### Estoque
- `GET /api/v1/estoque` - Consultar estoque
- `POST /api/v1/estoque/entrada` - Entrada de estoque
- `POST /api/v1/estoque/saida` - Saída de estoque
- `POST /api/v1/estoque/ajuste` - Ajuste de estoque

### Movimentações
- `GET /api/v1/movimentacoes` - Histórico de movimentações
- `GET /api/v1/movimentacoes/{produto_id}` - Movimentações por produto

### Relatórios
- `GET /api/v1/relatorios/estoque` - Relatório de estoque atual
- `GET /api/v1/relatorios/baixo-estoque` - Produtos com estoque baixo
- `GET /api/v1/relatorios/movimentacoes` - Relatório de movimentações

## 📝 Estrutura DDD

### Bounded Contexts

#### Identity Context
```
src/identity/
├── domain/
│   ├── entities/usuario.py
│   ├── value_objects/email.py
│   └── services/auth_service.py
├── infrastructure/
│   ├── repositories/sqlalchemy_usuario_repository.py
│   └── models/usuario_model.py
└── application/
    ├── services/auth_application_service.py
    └── dto/auth_dto.py
```

#### Inventory Context
```
src/inventory/
├── domain/
│   ├── entities/produto.py
│   ├── entities/estoque_produto.py
│   ├── value_objects/sku.py
│   └── services/estoque_service.py
├── infrastructure/
│   ├── repositories/sqlalchemy_produto_repository.py
│   └── models/produto_model.py
└── application/
    ├── services/produto_application_service.py
    └── dto/produto_dto.py
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Gabriel Figueiredo dos Santos**
- Email: gabriel@example.com
- LinkedIn: [seu-linkedin](https://linkedin.com/in/seu-perfil)
- GitHub: [@seu-usuario](https://github.com/seu-usuario)

## 🎓 TCC - MBA Engenharia de Software

Este projeto faz parte do Trabalho de Conclusão de Curso do MBA em Engenharia de Software, orientado pelo Prof. Ugo Henrique Pereira da Silva.

**Objetivo**: Analisar o impacto da aplicação do Domain-Driven Design na modelagem de microsserviços implementados em arquitetura serverless, comparando com uma implementação monolítica em termos de performance, escalabilidade e custos.