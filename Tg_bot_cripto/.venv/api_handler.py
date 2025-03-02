import time

import requests
import random

SERVER_IP = '3.121.200.85'

def send_scrape_request(server_url: str, target_url: str, class_name: str = 'css-9pa8cd'):
    """
    Відправляє запит до API сервера для отримання зображення

    Параметри:
    - server_url: URL вашого API сервера (наприклад, http://54.210.123.45:5000/scrape)
    - target_url: URL сторінки для скрапінгу
    - class_name: CSS клас елемента (за замовчуванням 'css-9pa8cd')
    """
    try:
        params = {
            'url': target_url,
            'class_name': class_name
        }

        response = requests.get(server_url, params=params, timeout=280)

        if response.status_code == 200:
            return response.json().get('image_url')
        else:
            return f"Помилка: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        print(f"Помилка з'єднання: {str(e)}")
        raise Exception(e)


# Приклад використання
def get_image_url(target_url: str, class_name: str):
    # Налаштування
    API_SERVER = f"http://{SERVER_IP}:5000/scrape"  # Замініть на реальний IP
    TARGET_URL = target_url  # Сайт для скрапінгу
    CLASS_NAME = class_name  # Необов'язковий параметр

    time.sleep(random.uniform(1, 4))

    result = send_scrape_request(API_SERVER, TARGET_URL, CLASS_NAME)

    return result