import requests
import re
from bs4 import BeautifulSoup

import config
from TelegramBot import TelegramBot


class PrimeNowChecker:
    PATHS = {
        'url': 'https://primenow.amazon.es/',
        'onboard': 'onboard/check?',
        'login': 'ap/signin',
        'checkout': 'checkout/enter-checkout?merchantId='
    }

    CHECKS = {
        'unavailable_windows': 'Actualmente no hay ventanas de entrega',
        'unavailable_products': '1 producto ya no está disponible',
    }

    def __init__(self):
        self.n_errors = 0

    def login(self):
        session = requests.Session()
        session.headers = self.get_headers()

        '''

        response = session.get(url=self.PATHS.get('url'))

        swapping_token = re.compile('data-location-select-form-click=".*?offerSwappingToken&quot;:&quot;(.*?)&quot;') \
            .search(response.text) \
            .group(1)
        cp = '28005'
        onboard_url = '{primenow_url}{onboard_path}postalCode={cp}&offerSwappingToken={swapping_token}'.format(
            primenow_url=self.PATHS.get('url'),
            onboard_path=self.PATHS.get('onboard'),
            cp=cp,
            swapping_token=swapping_token
        )
        response = session.get(url=onboard_url)

        session.get(url=response.json().get('url'))
        
        '''

        login_url = '{primenow_url}{login_path}'.format(
            primenow_url=self.PATHS.get('url'),
            login_path='signin'
        )
        print(login_url)

        response = session.get(
            url=login_url,
        )

        form = BeautifulSoup(response.text, 'html.parser').find('form', {'name': 'signIn'})
        data = {field.get('name'): field.get('value') for field in form.find_all('input')}
        data['email'] = 'marcoocram@gmail.com'
        data['password'] = 'BELLIMA8'
        url = form.get('action')
        #data['metadata1'] = 'ECdITeCs:X8MiJBj6ne/YXTfkw8Yl4ByLgpjIPY1bE4qqfLT7nC1P6y32b1YYmwo2+19Z/YpCVkf5zxpijy/IMdUvTrY6yb7JvgEvKLhZL5q1+ik8/6dZO0I1ZxIOPEHlm7cNuXjiQ+V02w5N03SWWbvWuFuflTBAOabZSgcavsOCxVEgCuAv7wmvbgT6LaXmmyZfLoCPhElzfDQxpHHbi0w1DYrJwe8TgiJp+6p3u1dbqDjZq1GT/LlsF1GVkfS9CTQtRLSHxKXUcYpx+oQQMgVGmcyypyBqNLlriQh2F1Jq8u3kLrVZmRd/MGiyghaP9W2jKFRqBq0it4S+b49MmwQwl7QUZsC/r/sds1vwsbcd3dQfuT1bo0dM9r+ZrxJqVsbjIVMqgIhPh9ZZiRfqX69ZcsvuMPbv2VJyNCsEW09gMiGMczNYQhH+Ah8p7bRTGd5iYZO7eCUSRuv/7TPotPqa/ZabxoJFlc2CVAOF9WiKoVzUHZdI1VrV2pHRct65elqAJPCTxO/EHctOZhskr3a2mlwcESljOQE2/ipSbDLU5+dyzN0dBXc5AhL7Bms8LMI+FUjwVbcB206nbRxzWRry8lQnJL2PHm+aNswwqU+jkJV3CAx43ugZdf1tgxDtB8SOOuH0cpW2c7J28Ta5Q8DhQsEvVhPMjRsBICzPRw1k6EUu7kc7aQLZpdthi8lnJwxNogOL2pyzfwi2fe6+uhdVJ1DFwCP7TJizzy9Pt8seDBXZIO765pVXoVUzSBlkXQKsNvibdYH6oXE+ea9HNTceW6Oi4+ZdwE1NUi0+S+20KEa9PhZk9jS6ESrHn0d3l/Hq0wdqFG5e6pN0nTOsdrYlqDqhYsKiZ2+jpeh6urgojF8oSh8gFTflUai5P4jvD4M5kE3PulMVC6DH0iBbMw0Iy6bKnd6ppydOaiiSz6an4raotGsfBRJbfWusjfmWLrXGpTC0eqDc03AFZG5Ymg7MEwu/kl+p3G7p+z/7nlLh9B1FXfrObiEBfvK9S5wPrDZ5U6mNc/gwDt7OeDmtNnCFn92n8z22BuosVExFEiAwDUjLApTcHPAxF1IiwMWI6M5iCjw5NwU3Rb8JAYYD38nX4TfZVsLtwKVW/cojOGxoMA8RKWyeZupyisNUHb+XbNuC3Jlucv77pHvEo2JWFNeaayl9hb8wkZIjZ2NfuMjnt4cpFWAGWl01Q01ebsTVl8NrqaKPaL2IoJCTl7+0XCcP+yP5UkbLCGNzurRVuL5Yrv4rS2cKJrd7JK0oexxd1uTbvsqhVliccEYAMAeBSr5zlBAgFWMGhGPwMu60TowaIFZU5zkDS6p9Y/4RM/sMRRu4RzKRajqatQgZdmtzNBeftPkUoa1Qn19jq8eAFoc3dF8SEvDFDSkaiT+BRSUdfbsxcuvqCRuCi7z1/GbTlcPzbc8MNf7VgEm8DDuCsIqnqqsoT6XTxtbBZ8OfQ4Z5Hprs1Ibv4bW+tbEsYll1Wk/llt/VBPUbCAtfy3zxJ0lE2CmDuZ27PoL7/JTaZayjmdm/U6pWZoqdVfBbIPVoCWBq/JWnMsTxgJsMcJzoDTjIbXk6cktWquBlmeT4aCwkdIKhngFyX0b3imiwO08v2Mxxdk661SIQrxcs0TaVwXAMU3n8XBeTeAiqmtgXJQVs4WRdONSK8rpbkvSqnIo3YQRI9OokYhuiQuH0kXAElXry/KVEaR8='

        print(data)

        response = session.post(
            url=url,
            data=data
        )

        print(response)
        print(dict(session.cookies))
        self.save_response(response, 'response_test.html')

    def check_merchant(self, merchant):
        print(f'Checking {merchant.get("name")}...')

        url = '{primenow_url}{checkout_path}{merchant_id}'.format(
            primenow_url=self.PATHS.get('url'),
            checkout_path=self.PATHS.get('checkout'),
            merchant_id=merchant.get('id')
        )

        response = requests.get(
            url=url,
            headers=self.get_headers(),
            cookies=config.cookie
        )

        available_windows = self.get_available_windows(response)

        if len(available_windows) > 0:
            message = f'¡Available windows on {merchant.get("name")}!\n\nAvailable windows:\n\n' + '\n'.join(
                available_windows)

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
        return {
            'User-Agent': 'Mozilla/5.0 (X11;Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,en;q=0.5',
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
