import requests
import logging

TELEGRAM_BOT_TOKEN="7376099399:AAG5FoywNJGKoZ3GlUhSECXSVb3YotywZ88"
TELEGRAM_CHAT_ID="643930225"

class Messeger():

    @staticmethod
    def send_telegram_message(message_subject: str, message_body: str) -> None:
        endpoint = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        max_length = 4000
        message_batches = []
        current_message = ""
        # Split messages into sections
        chunks = message_body.split("\n\n")
        for chunk in chunks:
            if len(current_message) + len(chunk) <= max_length:
                current_message += chunk + "\n\n"
            else:
                message_batches.append(current_message.strip())
                current_message = chunk + "\n\n"
        message_batches.append(current_message.strip())

        # Send each batch as a separate notification in the same chain
        for i, message_batch in enumerate(message_batches):
            if i == 0:
                message_text = f"{message_subject}\n\n{message_batch}"
            else:
                message_text = message_batch
            params = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message_text
            }
            params_pavlo = {
                "chat_id": "751066597",
                "text": message_text
                # "text": "пішов в дупу Павлик"
            }

            params_pavlo2 = {
                "chat_id": "751066597",
                "text": "повитерай пилисос Павлик"
            }

            try:
                response = requests.get(endpoint, params=params)
                # send pavlo message
                # requests.get(endpoint, params=params_pavlo)
                # requests.get(endpoint, params=params_pavlo2)

                response.raise_for_status()
                if response.json()["ok"]:
                    logging.info("Email notification sent successfully")
                else:
                    logging.error(
                        "Error sending Telegram notification")
            except requests.exceptions.RequestException as error:
                logging.error(f"Telegram connection error: {error}")
