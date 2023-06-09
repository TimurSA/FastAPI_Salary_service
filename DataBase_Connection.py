import psycopg2
from psycopg2.extras import RealDictCursor, execute_values


def collect_data(*, dbname: str, user: str, password: str):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password)  # подключение к базе данных
    cur = conn.cursor()  # курсор для вып команд
    data = {}
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute("SELECT * FROM logins")
                for employee in curs.fetchall():
                    data[employee[1]] = {"password": employee[2], "salary": employee[3],
                                         "promotion_date": employee[4]}

    finally:
        conn.close()

    return data
