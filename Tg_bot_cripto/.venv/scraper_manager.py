import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import Optional

BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def get_header() -> dict:
    """Генерує випадкові HTTP-заголовки"""
    headers = [
        # Ваш список заголовків з питання
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "TE": "Trailers"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/90.0.818.62 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "TE": "Trailers"
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.google.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        # ... інші заголовки
    ]
    return random.choice(headers)


def get_x_page_with_selenium(url: str) -> Optional[str]:
    """Отримує HTML через Selenium з випадковим User-Agent"""
    try:
        # Налаштування опцій Chrome
        chrome_options = Options()

        # Використовуємо User-Agent з вашої функції
        user_agent = get_header().get("User-Agent")
        print(user_agent)
        chrome_options.add_argument(f"user-agent={user_agent}")

        # Додаткові налаштування для уникнення блокування
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--headless")  # Робота у фоновому режимі
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Ініціалізація драйвера
        driver = webdriver.Chrome(options=chrome_options)

        # Відкриття сторінки
        driver.get(url)

        driver.set_page_load_timeout(5)
        # Чекаємо, доки сторінка завантажиться (можна додати явні очікування)
        driver.implicitly_wait(random.uniform(5, 11))  # 10 секунд очікування

        # Отримуємо HTML
        # html = driver.page_source
        #
        # Закриваємо браузер
        # driver.quit()
        return driver
    except Exception as e:
        print(f"Selenium помилка: {e}")
        driver.quit()
        time.sleep(10)
        raise Exception(e)
        # return None


def get_x_page_element_image(url: str, class_name: str):
    driver = get_x_page_with_selenium(url)
    element = driver.find_element(By.CLASS_NAME, class_name)

    img = element.get_attribute("src")

    driver.quit()

    return img


# Використання
# if __name__ == "__main__":
#     url = "https://x.com/v_malko31476/photo"
#     # поук елемента з зображенням через клас
#     old_image_element_link = 'https://pbs.twimg.com/profile_images/1822199929986510848/UYFSJ2NM_400x400.png'
#
#     image_element_link = get_x_page_element_image(url,'css-9pa8cd' )
#
#     if image_element_link != old_image_element_link:
#         print("відправити повідомлення!")
#
#     else:
#         print("не змінено аватарку")