# Dockerfile mínimo para rodar apenas o que é necessário em produção

FROM python:3.13.0-slim-bookworm

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Diretório de trabalho
WORKDIR /app

# Instalar dependências de sistema necessárias (somente libpq-dev para PostgreSQL e curl para healthcheck)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar apenas o código-fonte da aplicação (sem testes, migrations ou scripts auxiliares)
COPY src/ ./src

# (Opcional) Se você precisar rodar migrações no container, copie também o arquivo de configuração do Alembic:
# COPY alembic.ini .
# COPY alembic/ ./alembic/

# Criar usuário não-root e ajustar permissões
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expor porta do FastAPI
EXPOSE 8080

# Healthcheck básico (supondo que exista rota /api/v1/health/ em src/main.py)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/api/v1/health/ || exit 1

# Comando padrão para iniciar a aplicação via Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
