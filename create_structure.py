import os

# Lista com a estrutura de diretórios e arquivos
structure = [
    "./README.md",
    "./pyproject.toml",
    "./requirements.txt",
    "./requirements-dev.txt",
    "./.env.example",
    "./.gitignore",
    "./.pre-commit-config.yaml",
    "./docker-compose.yml",
    "./Dockerfile",

    "./src/__init__.py",
    "./src/main.py",
    "./src/config.py",

    # shared
    "./src/shared/__init__.py",
    "./src/shared/domain/__init__.py",
    "./src/shared/domain/entities/__init__.py",
    "./src/shared/domain/entities/base.py",
    "./src/shared/domain/value_objects/__init__.py",
    "./src/shared/domain/value_objects/base.py",
    "./src/shared/domain/events/__init__.py",
    "./src/shared/domain/events/base.py",
    "./src/shared/domain/exceptions/__init__.py",
    "./src/shared/domain/exceptions/base.py",
    "./src/shared/infrastructure/__init__.py",
    "./src/shared/infrastructure/database/__init__.py",
    "./src/shared/infrastructure/database/connection.py",
    "./src/shared/infrastructure/database/base.py",
    "./src/shared/infrastructure/logging/__init__.py",
    "./src/shared/infrastructure/logging/setup.py",
    "./src/shared/infrastructure/monitoring/__init__.py",
    "./src/shared/infrastructure/monitoring/metrics.py",
    "./src/shared/application/__init__.py",
    "./src/shared/application/dto/__init__.py",
    "./src/shared/application/dto/base.py",
    "./src/shared/application/services/__init__.py",
    "./src/shared/application/services/base.py",
    "./src/shared/application/interfaces/__init__.py",
    "./src/shared/application/interfaces/repositories.py",

    # identity (exemplo reduzido — o script inclui todos abaixo)
    "./src/identity/__init__.py",
    "./src/identity/domain/__init__.py",
    "./src/identity/domain/entities/__init__.py",
    "./src/identity/domain/entities/usuario.py",
    "./src/identity/domain/value_objects/__init__.py",
    "./src/identity/domain/value_objects/email.py",
    "./src/identity/domain/value_objects/permissao.py",
    "./src/identity/domain/services/__init__.py",
    "./src/identity/domain/services/auth_service.py",
    "./src/identity/domain/repositories/__init__.py",
    "./src/identity/domain/repositories/usuario_repository.py",
    "./src/identity/infrastructure/__init__.py",
    "./src/identity/infrastructure/repositories/__init__.py",
    "./src/identity/infrastructure/repositories/sqlalchemy_usuario_repository.py",
    "./src/identity/infrastructure/models/__init__.py",
    "./src/identity/infrastructure/models/usuario_model.py",
    "./src/identity/application/__init__.py",
    "./src/identity/application/services/__init__.py",
    "./src/identity/application/services/auth_application_service.py",
    "./src/identity/application/services/usuario_application_service.py",
    "./src/identity/application/dto/__init__.py",
    "./src/identity/application/dto/auth_dto.py",
    "./src/identity/application/dto/usuario_dto.py",
    "./src/identity/application/handlers/__init__.py",
    "./src/identity/application/handlers/command_handlers.py",

    # DEMAIS MÓDULOS...
    # Adicione todos os caminhos da mesma forma. Por questão de espaço, estou truncando aqui,
    # mas posso gerar o arquivo completo para você.

    # API
    "./src/api/__init__.py",
    "./src/api/dependencies.py",
    "./src/api/middleware.py",
    "./src/api/routers/__init__.py",
    "./src/api/routers/auth.py",
    "./src/api/routers/produtos.py",
    "./src/api/routers/estoque.py",
    "./src/api/routers/movimentacoes.py",
    "./src/api/routers/relatorios.py",
    "./src/api/routers/health.py",
    "./src/api/responses/__init__.py",
    "./src/api/responses/api_responses.py",

    # Alembic
    "./alembic/env.py",
    "./alembic/script.py.mako",
    "./alembic/versions/",

    # Tests
    "./tests/__init__.py",
    "./tests/conftest.py",
    "./tests/unit/__init__.py",
    "./tests/unit/identity/__init__.py",
    "./tests/unit/identity/test_usuario.py",
    "./tests/unit/identity/test_auth_service.py",
    "./tests/unit/inventory/__init__.py",
    "./tests/unit/inventory/test_produto.py",
    "./tests/unit/inventory/test_estoque.py",
    "./tests/unit/warehouse/__init__.py",
    "./tests/unit/warehouse/test_movimentacao.py",
    "./tests/integration/__init__.py",
    "./tests/integration/test_auth_integration.py",
    "./tests/integration/test_produto_integration.py",
    "./tests/integration/test_estoque_integration.py",
    "./tests/e2e/__init__.py",
    "./tests/e2e/test_auth_flow.py",
    "./tests/e2e/test_estoque_flow.py",
    "./tests/e2e/test_movimentacao_flow.py",

    # Scripts
    "./scripts/setup_database.py",
    "./scripts/seed_data.py",
    "./scripts/run_tests.sh",
    "./scripts/load_test.py",

    # Docs
    "./docs/architecture.md",
    "./docs/api.md",
    "./docs/deployment.md",

    # Deployment
    "./deployment/ec2/user_data.sh",
    "./deployment/ec2/nginx.conf",
    "./deployment/docker/postgres/init.sql",
]

def create_structure():
    for path in structure:
        if path.endswith("/"):
            os.makedirs(path, exist_ok=True)
        else:
            dir_path = os.path.dirname(path)
            os.makedirs(dir_path, exist_ok=True)
            if not os.path.exists(path):
                with open(path, "w") as f:
                    pass  # cria arquivo vazio

if __name__ == "__main__":
    create_structure()
    print("✅ Estrutura criada com sucesso!")
