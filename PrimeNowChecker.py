import requests
from bs4 import BeautifulSoup

import config
from TelegramBot import TelegramBot


class PrimeNowChecker:
    PATHS = {
        'url': 'https://primenow.amazon.es/',
        'checkout': 'checkout/enter-checkout?merchantId='
    }

    CHECKS = {
        'unavailable_windows': 'Actualmente no hay ventanas de entrega',
        'unavailable_products': '1 producto ya no está disponible',
    }

    def __init__(self):
        self.n_errors = 0

    def check_merchant(self, merchant):
        print(f'Checking {merchant.get("name")}...')

        url = self.PATHS.get('url') + self.PATHS.get('checkout') + merchant.get('id')

        response = requests.get(
            url=url,
            headers=self.get_headers(),
            cookies=config.cookie
        )

        available_windows = self.get_available_windows(response)

        if len(available_windows) > 0:
            message = f'¡Available windows on {merchant.get("name")}!\n\nAvailable windows:\n\n' + '\n'.join(available_windows)

            self.notify(message)

            self.save_response(response, 'response_ranges.html')

            exit()
        elif self.CHECKS.get('unavailable_windows') in response.text:
            self.reset_errors()

            print(f'Not available windows on {merchant.get("name")}')
        elif self.CHECKS.get('unavailable_products') in response.text:
            self.reset_errors()

            self.notify('One product has been deleted from your cart')
        else:
            self.n_errors += 1

            if self.n_errors == 3:
                self.notify('Error on check windows')

                self.save_response(response, 'response_error.html')

                exit(-1)

    def get_headers(self):
        user_agent = 'Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'

        return {
            'User-Agent': user_agent,
        }

    def reset_errors(self):
        self.n_errors = 0

    def get_available_windows(self, response):
        html_response = BeautifulSoup(response.text, 'html.parser')

        available_windows = html_response.select('[data-a-input-name="delivery-window-radio"] span.a-color-base')

        return [window.text.replace('\n', '').strip() for window in available_windows]

    def notify(self, message):
        print(message)

        if config.telegram_active:
            TelegramBot.send_message(message)

    def save_response(self, response, filename):
        with open(f'responses/{filename}', 'w') as file:
            file.write(response.text)
