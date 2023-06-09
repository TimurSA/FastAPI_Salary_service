"""
Need:
pip install fastapi
pip install pydantic
pip install uvicorn
pip install psycopg2
pip install pytest
pip install pytest-asyncio
pip install httpx
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import asyncio
import uvicorn
from datetime import datetime, timedelta
from DataBase_Connection import collect_data

app = FastAPI()

# # Вставьте данные о своей базы данных,на котором есть таблица такого формата:
#     Id SERIAL PRIMARY KEY,
#     username VARCHAR(64) NOT NULL,
#     password VARCHAR(64) NOT NULL,
# 	  salary integer NOT NULL,
# 	  promotion_date date NOT NULL
# employees = collect_data(dbname='', user='', password='')


# В данном примере используется словарь для иллюстрации
employees = {
    "Alice": {"password": "123", "salary": 5000, "promotion_date": "2023-07-07"},
    "Bob": {"password": "5235", "salary": 6000, "promotion_date": "2023-08-17"},
    "Timur": {"password": "4124", "salary": 1000000, "promotion_date": "2023-07-04"},
    "Aidar": {"password": "1997", "salary": 99999, "promotion_date": "2023-09-09"},
}


# Модель класса аундетификации
class LoginData(BaseModel):
    username: str
    password: str


html_home = '''
        <html>
<head>
    <title>Salary Service</title>
</head>
<body>
    <h1>Welcome to the Salary Service!</h1>
    <h2>Please go to <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a> in order to operate the service<h2>


</body>
</html>
    '''

# Здесь хранятся зарегистрировашиеся токены и дата их конца действия
tokens = {}


def generate_token(username: str) -> str:
    # Генерация токена, который будет действителен в течение 30 минут
    # Здесь расположена хеш-функция, но для примера просто будет простая строка
    token = "token_" + username
    expiration = datetime.now() + timedelta(minutes=30)
    tokens[token] = expiration
    return token


# Проверка дейстивителен ли токен или нет
def validate_token(token: str):
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")
    now = datetime.now()
    if tokens[token] < now:
        raise HTTPException(status_code=401, detail="Token expired")
    return token


# Post запрос на получение токена (авторизация)
@app.post("/token")
async def get_token(login_data: LoginData):
    username = login_data.username
    password = login_data.password
    if username not in employees or password != employees[username]["password"]:
        raise HTTPException(status_code=401, detail="Неправильное имя пользователя или пароль")

    token = generate_token(username)

    return {"token": token}


# Возращает главную страницу
@app.get("/")
async def get():
    return HTMLResponse(html_home)


# Информация о зарплате
# Сначала мы всегда проверяем дейтсвует ли еще токен
@app.get("/salary/{name}")
async def get_salary(name: str, token: str = Depends(validate_token)):
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Недействительный токен")

    username = token.split("_", 1)[1]
    salary = await asyncio.to_thread(lambda: employees[username]["salary"])

    return {"name": username,
            "salary": salary}


# Информация о дате повышение
# Здесь тоже мы проверяем дейтсвует ли еще токен
@app.get("/promotion_date/{name}")
async def get_promotion_date(token: str = Depends(validate_token)):
    username = token.split("_", 1)[1]
    promotion_date = await asyncio.to_thread(lambda: employees[username]["promotion_date"])
    return {"name": username,
            "promotion_date": promotion_date}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
