import os
import pytest
from fastapi.testclient import TestClient
from redis import Redis

from sqlmodel import Session as OrmSession
from sqlmodel import SQLModel


from atropos.main import app
from atropos.db import engine

# Constants for test data
TEST_TASK_QUEUE = "test:task:queue"


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    SQLModel.metadata.create_all(engine)


# FastAPI client
@pytest.fixture
def client():
    return TestClient(app)


# Isolated DB session (auto rollback)
@pytest.fixture
def db_session():
    """
    Yields a session wrapped in a rollback-only transaction.
    No changes persist after the test finishes.
    """
    connection = engine.connect()
    trans = connection.begin()
    session = OrmSession(bind=connection)

    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()


# Redis cleanup
@pytest.fixture(autouse=True)
def clear_redis_queue():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis = Redis.from_url(redis_url)
    redis.delete(TEST_TASK_QUEUE)
    yield
    redis.delete(TEST_TASK_QUEUE)


def get_redis_client():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return Redis.from_url(redis_url)


@pytest.fixture(autouse=True)
def clear_redis_queue():
    redis = get_redis_client()
    redis.delete(TEST_TASK_QUEUE)
    yield
    redis.delete(TEST_TASK_QUEUE)
