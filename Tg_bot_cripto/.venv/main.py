from notification_manager import Messeger
import asyncio
import json
import time
import threading
from scraper_manager import get_x_page_element_image
from api_handler import get_image_url
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from datetime import datetime

# Конфігурація
ADMIN_ID = 643930225
user_ids = set()
old_image_element_link = 'https://pbs.twimg.com/profile_images/1822199929986510848/UYFSJ2NM.png'
last_time_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Завантажити збережені ID
try:
    with open("user_ids.json", "r") as file:
        user_ids = set(json.load(file))
except FileNotFoundError:
    pass


def save_user_ids():
    with open("user_ids.json", "w") as file:
        json.dump(list(user_ids), file)


async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_user_ids()

    if user_id == ADMIN_ID:
        keyboard = [
            [KeyboardButton("Список користувачів")],
            [KeyboardButton("Показати аватарку")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Ласкаво просимо, адміне!", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Ласкаво просимо!")

async def send_curet_image(update: Update, context: CallbackContext):
    """Надсилає поточну аватарку"""
    global old_image_element_link
    await update.message.reply_photo(photo=old_image_element_link, caption=f"Ось поточна аватарка. Останій час запиту: {last_time_update}")

async def show_users(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Доступ заборонено!")
        return

    users_list = "\n".join(map(str, user_ids))
    await update.message.reply_text(f"📋 Список ID користувачів:\n{users_list}")


async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_user_ids()


def check_avatar_changes():
    global last_time_update
    global old_image_element_link
    switching_parsing_methods = True
    while True:
        try:
            # Виконуємо синхронний скрапінг
            if switching_parsing_methods:
                image_element_link = get_image_url(
                    "https://x.com/elonmusk/photo",
                    'css-9pa8cd'
                )
            else:
                image_element_link = get_x_page_element_image(
                    "https://x.com/elonmusk/photo",
                    'css-9pa8cd'
                )

            if image_element_link != old_image_element_link:
                print("🔄 Виявлено зміни! Відправляю повідомлення...")
                Messeger.send_telegram_message('', image_element_link)

                # update.message.reply_text(image_element_link)
                old_image_element_link = image_element_link
            else:
                print("⏳ Аватар не змінився")

            time.sleep(10)  # Перевірка кожні 10 секунд
            last_time_update = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} метод {switching_parsing_methods}'


        except Exception as e:
            print(Messeger.send_telegram_message('', f"🚨 Помилка при перевірці аватара Метод {switching_parsing_methods}: {str(e)}"))
            switching_parsing_methods = not switching_parsing_methods


def main():
    # Ініціалізація бота
    application = Application.builder().token("7376099399:AAG5FoywNJGKoZ3GlUhSECXSVb3YotywZ88").build()

    # Реєстрація обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r'^Список користувачів$'), show_users))
    application.add_handler(MessageHandler(filters.Regex(r'^Показати аватарку$'), send_curet_image))
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    # Запускаємо скрапінг у окремому потоці
    threading.Thread(target=check_avatar_changes, daemon=True).start()

    # Старт бота
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
