import time

import config
from PrimeNowChecker import PrimeNowChecker


def get_merchants_to_check():
    print('Merchants to check:\n')

    print('[0] All')
    print('\n'.join(['[' + str(index + 1) + '] ' + merchant['name'] for index, merchant in enumerate(config.primenow_merchants)]))

    merchants_to_check = int(input('\nEnter selection [0 - ' + str(len(config.primenow_merchants)) + '] (0): ') or '0')

    assert 0 <= merchants_to_check <= len(config.primenow_merchants), 'Error on select merchants to check'

    return [
        PrimeNowChecker(merchant)
        for index, merchant in enumerate(config.primenow_merchants)
        if merchants_to_check == 0 or merchants_to_check == (index + 1)
    ]


if __name__ == '__main__':
    merchants_checkers = get_merchants_to_check()
    seconds_between_requests = int(input('Set seconds between requests (60): ') or '60')

    while True:
        for merchant_checker in merchants_checkers:
            merchant_checker.check()
            time.sleep(seconds_between_requests)
