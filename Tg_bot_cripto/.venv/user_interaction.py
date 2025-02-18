import json
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Конфігурація
ADMIN_ID = 643930225  # Ваш Telegram ID
user_ids = set()

# Завантажити збережені ID
try:
    with open("user_ids.json", "r") as file:
        user_ids = set(json.load(file))
except FileNotFoundError:
    pass


# Зберегти ID
def save_user_ids():
    with open("user_ids.json", "w") as file:
        json.dump(list(user_ids), file)


# Обробник /start
async def start(update, context):
    user_id = update.message.from_user.id

    # Додаємо користувача в базу
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_user_ids()

    # Створюємо клавіатуру ТІЛЬКИ для адміна
    if user_id == ADMIN_ID:
        keyboard = [[KeyboardButton("Список користувачів")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Ласкаво просимо, адміне!", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Ласкаво просимо!")


# Обробник кнопки
async def show_users(update, context):
    user_id = update.message.from_user.id

    # Перевірка прав доступу
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔ Доступ заборонено!")
        return

    # Оновлення бази
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_user_ids()

    # Формування списку
    users_list = "\n".join(map(str, user_ids))
    await update.message.reply_text(f"📋 Список ID користувачів:\n{users_list}")


# Обробник інших повідомлень
async def handle_message(update, context):
    user_id = update.message.from_user.id
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_user_ids()


def main():
    application = Application.builder().token("7376099399:AAG5FoywNJGKoZ3GlUhSECXSVb3YotywZ88").build()

    # Реєстрація обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r'^Список користувачів$'), show_users))
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()