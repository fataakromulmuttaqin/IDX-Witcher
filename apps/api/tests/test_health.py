"""Tests for health endpoint."""

import pytest
from fastapi.testclient import TestClient

from IDX Witcher_api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "IDX Witcher-api"


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"
