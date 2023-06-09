import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


@pytest.mark.asyncio
async def test_home():
    response = client.get("/")
    assert response.status_code == 200
    print(response.content)
    assert response.content == b'\n        <html>\n<head>\n    <title>Salary Service</title>\n</head>\n<body>\n    <h1>Welcome to the Salary Service!</h1>\n    <h2>Please go to <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a> in order to operate the service<h2>\n\n\n</body>\n</html>\n    '


@pytest.mark.asyncio
@pytest.mark.parametrize("name, password, expected", [("Alice", "123", "token_Alice"),
                                                      ("Bob", "5235", "token_Bob"),
                                                      ("Timur", "4124", "token_Timur"),
                                                      ("Aidar", "1997", "token_Aidar")])
async def test_post(name, password, expected):
    response = client.post("/token", json={"username": name, "password": password})
    assert response.status_code == 200
    assert response.json() == {"token": expected}
