import hashlib


def sha256_hash(data):
    # Создаем объект хеша SHA-256
    hash_code = hashlib.sha256()

    # Обновляем хеш с данными
    hash_code.update(data.encode('utf-8'))

    # Получаем и возвращаем хеш в шестнадцатеричном формате
    return hash_code.hexdigest()

