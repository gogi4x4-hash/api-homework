"""Задание 2. Работа с параметрами запроса (OpenWeather API).

Программа спрашивает название города, отправляет GET-запрос к OpenWeather
и выводит текущую температуру и описание погоды.

Ключ API не хранится в коде: он берётся из переменной окружения
OPENWEATHER_API_KEY. Бесплатный ключ выдаётся на openweathermap.org/api
(активируется до 2 часов после регистрации).
"""

import os  # доступ к переменным окружения
import sys  # корректный выход с кодом ошибки

import requests  # библиотека для HTTP-запросов

URL = "https://api.openweathermap.org/data/2.5/weather"  # текущая погода


def get_api_key() -> str:
    """Взять ключ API из переменной окружения OPENWEATHER_API_KEY."""
    key = os.environ.get("OPENWEATHER_API_KEY", "").strip()
    if not key:
        sys.exit(
            "Не задан ключ API OpenWeather.\n"
            "Получите бесплатный ключ на https://openweathermap.org/api "
            "и задайте его в переменной окружения OPENWEATHER_API_KEY:\n"
            '  Windows PowerShell:  $env:OPENWEATHER_API_KEY = "ваш_ключ"\n'
            '  Linux/macOS:         export OPENWEATHER_API_KEY="ваш_ключ"'
        )
    return key


def get_weather(city: str, api_key: str) -> dict:
    """Отправить GET-запрос по городу и вернуть JSON-ответ в виде словаря."""
    params = {
        "q": city,           # параметр запроса: название города
        "appid": api_key,    # ключ доступа к API
        "units": "metric",   # температура в градусах Цельсия
        "lang": "ru",        # описание погоды на русском
    }

    # GET-запрос с параметрами: requests сам соберёт строку ?q=...&appid=...
    response = requests.get(URL, params=params, timeout=10)

    # Ошибку ключа/города API возвращает как JSON с кодом внутри, а не только
    # HTTP-статусом, поэтому сначала разбираем тело ответа
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()  # тело не JSON — падаем по HTTP-статусу
        raise

    # У OpenWeather поле cod — код результата: 200 у успеха, 401/404 у ошибок
    if str(data.get("cod")) != "200":
        # Сообщение сервера, например "city not found" или "Invalid API key"
        raise RuntimeError(data.get("message", "неизвестная ошибка API"))

    return data


def main():
    # Название города принимаем от пользователя
    city = input("Введите название города: ").strip()
    if not city:
        sys.exit("Город не указан.")

    api_key = get_api_key()

    try:
        data = get_weather(city, api_key)
    except requests.RequestException as error:  # сеть, таймаут, плохой HTTP-статус
        sys.exit(f"Ошибка запроса: {error}")
    except RuntimeError as error:  # ошибка на стороне API
        sys.exit(f"API вернул ошибку: {error}")

    # Разбираем нужные поля JSON-ответа
    temperature = data["main"]["temp"]                # температура, °C
    description = data["weather"][0]["description"]   # текстовое описание
    feels_like = data["main"]["feels_like"]           # ощущается как, °C
    humidity = data["main"]["humidity"]               # влажность, %
    wind = data["wind"]["speed"]                      # скорость ветра, м/с
    city_name = data.get("name", city)                # название, как его знает API

    print(f"\nПогода в городе {city_name}:")
    print(f"Температура: {temperature:.1f} °C (ощущается как {feels_like:.1f} °C)")
    print(f"Описание: {description}")
    print(f"Влажность: {humidity} %, ветер: {wind} м/с")


if __name__ == "__main__":
    main()
