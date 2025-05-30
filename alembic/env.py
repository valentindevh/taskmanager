# alembic/env.py

from logging.config import fileConfig
import os
import asyncio

# Import for synchronous engine for Alembic
from sqlalchemy import create_engine, pool

# Import for async engine (even though we're not using it directly for Alembic's context)
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# This is the Base your models inherit from.
# Make sure this import path is correct for your project!
from app.models.base import Base # <--- IMPORTANT: VERIFY THIS IMPORT

# target_metadata contains all your SQLAlchemy model definitions.
target_metadata = Base.metadata

# Interpret the config file for Python logging.
fileConfig(context.config.config_file_name)

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an active connection.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise Exception("DATABASE_URL is not set for offline migrations.")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    This version uses a synchronous engine for Alembic's context,
    even though the application itself uses an async engine.
    This pattern is often necessary to avoid MissingGreenlet errors.
    """
    # Get the DATABASE_URL from environment variable
    database_url_async = os.environ.get("DATABASE_URL")
    if not database_url_async:
        raise Exception("DATABASE_URL is not set in environment variables.")

    # Convert the async URL to a synchronous URL for Alembic's internal use.
    # Replace 'postgresql+asyncpg' with 'postgresql+psycopg2'.
    # This requires `psycopg2-binary` to be installed.
    database_url_sync = database_url_async.replace("postgresql+asyncpg", "postgresql+psycopg2")

    # Create a synchronous engine directly for Alembic to use.
    # This engine will handle the `has_table` and other synchronous calls.
    # Use NullPool to ensure no pooling issues interfere.
    connectable = create_engine(
        database_url_sync,
        poolclass=pool.NullPool,
        echo=False # Set to True for verbose SQLAlchemy logging during migrations
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()