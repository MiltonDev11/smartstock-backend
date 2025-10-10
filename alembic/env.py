from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

from app.db.session import Base
from app.models.user import User
from app.core.config import settings

# Configuración de logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Aquí está la metadata de tus modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Migraciones en modo offline (usa solo la URL)."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Migraciones en modo online (usa un engine real)."""
    connectable = create_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
