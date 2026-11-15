"""Задание 1. Получение данных из публичного API (JSONPlaceholder).

Скрипт отправляет GET-запрос к /posts и выводит заголовок и тело первых 5 постов.
"""

import requests  # библиотека для HTTP-запросов

URL = "https://jsonplaceholder.typicode.com/posts"  # адрес публичного API
PARAMS = {"_limit": 5}  # параметр запроса: сервер вернёт только 5 записей

def main():
    # GET-запрос; params кодируются в строку вида ?_limit=5
    response = requests.get(URL, params=PARAMS, timeout=10)

    # Проверяем HTTP-статус: 200 — успех, 4xx/5xx — ошибка.
    # raise_for_status() выбросит исключение при плохом статусе.
    response.raise_for_status()

    # JSON-ответ превращается в список словарей Python
    posts = response.json()

    print(f"Получено постов: {len(posts)}\n")

    # Перебираем первые 5 постов (срез на случай, если сервер вернул больше)
    for post in posts[:5]:
        print(f"ID: {post['id']}")
        print(f"Заголовок: {post['title']}")
        print(f"Текст: {post['body']}")
        print("-" * 60)  # разделитель между постами


if __name__ == "__main__":
    main()
