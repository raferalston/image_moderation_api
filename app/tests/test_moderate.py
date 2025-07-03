import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock

from main import app

client = TestClient(app)


@pytest.mark.asyncio
@patch("services.moderate.httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_moderate_nsfw_detected(mock_post):
    """Тест для NSFW контента"""
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "nudity": {"none": 0.1}  # NSFW high
    }
    mock_post.return_value = mock_response

    with open("tests/sample_image.jpg", "rb") as f:
        response = client.post(
            "/moderate",
            files={"file": ("sample_image.jpg", f, "image/jpeg")}
        )

    assert response.status_code == 200
    assert response.json() == {"status": "REJECTED", "reason": "NSFW content"}
    assert mock_post.await_count == 1



@pytest.mark.asyncio
@patch("services.moderate.httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_moderate_safe_content(mock_post):
    """Тест для безопасного контента."""

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "nudity": {"none": 0.95}  # NSFW low
    }
    mock_post.return_value = mock_response

    with open("tests/sample_image.jpg", "rb") as f:
        response = client.post(
            "/moderate",
            files={"file": ("sample_image.jpg", f, "image/jpeg")}
        )

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
    assert mock_post.await_count == 1


def test_moderate_no_file():
    """Тест на случай, если файл не передан (ожидаем 422 Unprocessable Entity)."""
    response = client.post("/moderate")
    
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["type"] == "missing"
    assert data["detail"][0]["loc"] == ["body", "file"]