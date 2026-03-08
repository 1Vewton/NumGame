# Project dependencies
from numgame.server import app
from numgame.config import settings
# Test dependencies
from fastapi.testclient import TestClient
import pytest
import fakeredis


# Overwrite Redis
# Create fake redis client
@pytest.fixture
def fake_redis():
    server = fakeredis.FakeServer()
    client = fakeredis.FakeRedis(server=server,
                                 decode_responses=True)

    # Define aclose to prevent attribution error
    async def aclose():
        pass

    client.aclose = aclose
    return client


# Auto change the redis to fakeredis
@pytest.fixture(autouse=True)
def mock_redis_client(monkeypatch, fake_redis):
    async def mock_create_redis_client():
        return fake_redis

    monkeypatch.setattr("numgame.server.create_redis_client",
                        mock_create_redis_client)


# test client
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# Test Random Name generation
def test_random_name(client):
    response = client.get("/api/utils/generateUserName")
    assert response.status_code == 200


# Test simple bot management
def test_simple_bot_name(client):
    response = client.post("/api/user/userLogin",
                           json={"player_name": settings.simple_bot_name})
    assert response.status_code == 403


# User Management Test Class
class TestUserManagement:
    # Initialization
    cookie = None
    test_name = "test"

    # Test user registration
    def test_register(self, client):
        response = client.post("/api/user/userRegister",
                               json={"player_name": self.test_name})
        assert response.status_code == 201
        assert response.json()["user_name"] == self.test_name

    # Test user login
    def test_login(self, client):
        response = client.post("/api/user/userLogin",
                               json={"player_name": self.test_name})
        assert response.status_code == 200
        assert response.json()["user_name"] == self.test_name
