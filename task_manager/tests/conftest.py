import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio # Import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.base import Base
from app.main import app
from app.api.dependencies import get_db # Assuming get_db is your dependency for the database session

# Ensure that settings are loaded, especially DATABASE_URL
# In a real application, settings might be loaded via environment variables
# or a specific configuration loading mechanism.
# For tests, it's crucial that settings.DATABASE_URL is correctly set.

# Use a separate database for testing to avoid data corruption in your development database.
# This assumes 'taskdb' is the default and 'testdb' is for tests.
TEST_DATABASE_URL = settings.DATABASE_URL.replace("taskdb", "testdb")

engine = create_async_engine(TEST_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session") # Changed to pytest_asyncio.fixture
async def test_db_setup():
    """
    Sets up and tears down the test database tables for the entire test session.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture # Changed to pytest_asyncio.fixture
async def db(test_db_setup) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session for each test.
    The session is rolled back after each test to ensure isolation.
    """
    async with async_session() as session:
        yield session
        await session.rollback() # Rollback changes after each test

@pytest_asyncio.fixture # Changed to pytest_asyncio.fixture
async def client(db) -> AsyncGenerator[AsyncClient, None]:
    """
    Provides an asynchronous HTTP client for testing FastAPI endpoints.
    It overrides the application's database dependency to use the test database session.
    """
    # Override the get_db dependency in your FastAPI app to use the test database session
    app.dependency_overrides[get_db] = lambda: db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides = {} # Clear overrides after the test