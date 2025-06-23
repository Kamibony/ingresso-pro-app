# --- INÍCIO DA CORREÇÃO ---
# Adiciona a pasta raiz do projeto (concierge-pro-app) ao path do Python
# para que o Alembic possa encontrar a pasta 'app'.
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))
# --- FIM DA CORREÇÃO ---

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- INÍCIO DA CORREÇÃO 2 ---
# Importa a Base E O MÓDULO DOS MODELOS para que o Alembic os "enxergue"
from app.database import Base
from app.models import database_models
# --- FIM DA CORREÇÃO 2 ---


# Este é o objeto de configuração do Alembic, que dá acesso
# aos valores no arquivo .ini
config = context.config

# Seta a URL do banco de dados a partir da variável de ambiente (.env)
if os.getenv('DATABASE_URL'):
    config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))


# Interpreta o arquivo de configuração para o logging do Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adiciona o MetaData do seu modelo aqui para o suporte de 'autogenerate'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Roda as migrações em modo 'offline'.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Roda as migrações em modo 'online'.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
