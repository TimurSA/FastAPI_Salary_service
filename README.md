Инструкция по работе с сервисом:

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

Вставьте данные о своей PostgreSql базе данных,на котором есть таблица такого формата:

Id SERIAL PRIMARY KEY,
username VARCHAR(64) NOT NULL,
password VARCHAR(64) NOT NULL,
salary integer NOT NULL,
promotion_date date NOT NULL

employees = collect_data(dbname='', user='', password='')

или же можете запустить с данными из примера

Запустить модуль main.
Или же прописать в консоль: uvicorn main:app --reload

Перейти по ссылке: http://127.0.0.1:8000
Потом на ссылку: http://127.0.0.1:8000/docs

Передайте в запрос POST логин и пароль.
Полученный токен вписывайте в get запоросы по получению информации о зарплате и дате повышения.
Внимание каждый токен действует 30 минут. Поистечению токена будет не возможно получить информацию с get запросов.
