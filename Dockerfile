# ===========================================================================
# Dockerfile — inclusive-health-api-lacrei
# Multi-stage: builder (compila/instala deps) -> runtime (imagem final magra)
# Stack: Python 3.14 · Django + DRF · Poetry · Gunicorn · PostgreSQL
# ===========================================================================

# ---- Stage 1: builder (gordo, descartável) --------------------------------
FROM python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# Ferramentas de compilação (rede de segurança caso o psycopg precise compilar).
# Ficam SÓ neste estágio — não entram na imagem final.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Copia apenas os manifests primeiro: aproveita o cache de camadas do Docker.
# A camada de install só é refeita quando as dependências mudam de fato.
COPY pyproject.toml poetry.lock ./

# Instala apenas as dependências de produção, num venv em /app/.venv.
# --only main  -> ignora deps de dev (pytest, ruff, etc.)
# --no-root    -> não instala o próprio projeto como pacote (é uma app, não lib)
RUN poetry install --only main --no-root

# ---- Stage 2: runtime (magro, vai para produção) --------------------------
FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Apenas a biblioteca de runtime do Postgres (não os headers de -dev).
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Usuário não-root: se a aplicação for comprometida, o atacante não tem root.
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /app

# Traz o virtualenv já pronto do builder (sem compilador, sem Poetry).
COPY --from=builder /app/.venv /app/.venv

# Copia o código da aplicação (o .dockerignore evita trazer .venv, .git, etc.).
COPY . .

RUN chown -R app:app /app
USER app

EXPOSE 8000

# Produção: aplica migrations e sobe o Gunicorn (servidor WSGI de produção).
# Em desenvolvimento, o docker-compose sobrescreve este comando pelo runserver.
# Ajuste "core" se o nome do seu projeto Django for outro.
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3"]