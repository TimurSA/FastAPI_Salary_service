import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


@pytest.mark.asyncio
async def test_home():
    response = client.get("/")
    assert response.status_code == 200
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


@pytest.mark.asyncio
@pytest.mark.parametrize("name, password, token, salary", [("Alice", "123", "token_Alice", 5000),
                                                           ("Bob", "5235", "token_Bob", 6000),
                                                           ("Timur", "4124", "token_Timur", 1000000),
                                                           ("Aidar", "1997", "token_Aidar", 99999)])
async def test_get_salary(name, password, token, salary):
    response = client.post("/token", json={"username": name, "password": password})
    assert response.status_code == 200
    response = client.get(f"/salary/{name}?token={token}")
    assert response.status_code == 200
    assert response.json() == {'name': name,
                               'salary': salary}


@pytest.mark.asyncio
@pytest.mark.parametrize("name, password, token, promotion_date", [("Alice", "123", "token_Alice", "2023-07-07"),
                                                                   ("Bob", "5235", "token_Bob", "2023-08-17"),
                                                                   ("Timur", "4124", "token_Timur", "2023-07-04"),
                                                                   ("Aidar", "1997", "token_Aidar", "2023-09-09")])
async def test_get_promotion_date(name, password, token, promotion_date):
    response = client.post("/token", json={"username": name, "password": password})
    assert response.status_code == 200
    response = client.get(f"/promotion_date/{name}?token={token}")
    assert response.status_code == 200
    assert response.json() == {'name': name,
                               'promotion_date': promotion_date}
