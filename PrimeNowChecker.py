import requests
import re
from bs4 import BeautifulSoup

import config
from TelegramBot import TelegramBot


class PrimeNowChecker:
    PATHS = {
        'url': 'https://primenow.amazon.es/',
        'checkout': 'checkout/enter-checkout?merchantId='
    }

    merchant = None
    n_errors = 0
    products = []

    def __init__(self, merchant):
        self.merchant = merchant

    def check(self):
        print(f'Checking {self.merchant.get("name")}...')

        url = self.PATHS['url'] + self.PATHS['checkout'] + self.merchant['id']

        response = requests.get(
            url=url,
            headers=self.get_headers(),
            cookies=config.cookie
        )

        try:
            available_windows = self.get_available_windows(response)
        except AssertionError:
            self.n_errors += 1

            self.save_response(response, 'response_error.html')

            if self.n_errors == 3:
                self.notify('Error on check windows')

                raise Exception('Error on check windows')

            return

        self.check_products(response)

        if len(available_windows) > 0:
            message = f'¡Available windows on {self.merchant.get("name")}!\n\nAvailable windows:\n\n' + '\n'.join(available_windows)

            self.notify(message)

            self.save_response(response, 'response_ranges.html')

            return True
        else:
            self.reset_errors()

            print(f'Not available windows on {self.merchant.get("name")}')

        return False

    def get_headers(self):
        user_agent = 'Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'

        return {
            'User-Agent': user_agent,
        }

    def reset_errors(self):
        self.n_errors = 0

    def get_available_windows(self, response):
        html_response = BeautifulSoup(response.text, 'html.parser')

        assert len(html_response.select('form#delivery-slot-form')) == 1, 'Not checkout page'

        available_windows = html_response.select('[data-a-input-name="delivery-window-radio"] span.a-color-base')

        return [window.text.replace('\n', '').strip() for window in available_windows]

    def notify(self, message):
        print(message)

        if config.telegram_active:
            TelegramBot.send_message(message)

    def save_response(self, response, filename):
        with open(f'responses/{filename}', 'w') as file:
            file.write(response.text)

    def check_products(self, response):
        cart_items = self.get_products_from_response(response)

        products_removed = []
        products_quantity_removed = []

        for product in self.products:
            item = next((item for item in cart_items if item['product'] == product['product']), None)

            if item is None:
                products_removed.append(product)
            elif item['quantity'] < product['quantity']:
                products_quantity_removed.append(item)

        alerts = ''

        if len(products_removed) > 0:
            alerts += f'The next product/s has been removed from your cart ({self.merchant.get("name")}):\n\n'
            alerts += '\n'.join(['- ' + product['product'] for product in products_removed]) + '\n\n'

        if len(products_quantity_removed) > 0:
            alerts += f'The next product/s has been decrease the quantity from your cart ({self.merchant.get("name")}):\n\n'
            alerts += '\n'.join(['- ' + product['product'] + f" ({product['quantity']})" for product in products_quantity_removed]) + '\n\n'

        if alerts != '':
            self.notify(alerts)

        self.products = cart_items

    def get_products_from_response(self, response):
        html_response = BeautifulSoup(response.text, 'html.parser')

        return [{
            'product': item.select('.a-text-bold')[0].text.replace('\n', '').strip(),
            'quantity': re.match(".*?Cant.: ([0-9]*)", item.text.replace('\n', '')).groups()[0]
        } for item in html_response.select('.checkout-item-container')]
