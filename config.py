import dotenv
import os
import json

dotenv.load_dotenv()

telegram_active = bool(int(os.getenv('TELEGRAM_BOT_ACTIVE')))
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_BOT_ID')

cookie = {
    'ubid-acbes': os.getenv('COOKIE_UBID'),
    'x-acbes': os.getenv('COOKIE_X_ACBES'),
    'at-acbes': os.getenv('COOKIE_AT_ACBES'),
    'sess-at-acbes': os.getenv('COOKIE_SESS_AT_ACBES'),
}

with open('merchants.json', 'r') as file:
    primenow_merchants = json.load(file)
