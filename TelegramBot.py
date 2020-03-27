import requests

import config


class TelegramBot:
    TELEGRAM_URL = 'https://api.telegram.org'

    @staticmethod
    def send_message(message):
        url = '{telegram_url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}'.format(
            telegram_url=TelegramBot.TELEGRAM_URL,
            token=config.telegram_token,
            chat_id=config.telegram_chat_id,
            message=message
        )

        return requests.get(url)
