import requests
import unittest


def date(date_test):
    try:
        # komunikacja z API
        communication = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/c/USD/{date_test}/?format=json')
        response = communication.json()
        exchange_rate = response['rates'][0]['bid']
        value_in_pln = 100 * exchange_rate

        return value_in_pln

    except ValueError:
        print("Brak kursu walut dla danego dnia, proszę wprowadzić inną datę.")


class Test(unittest.TestCase):

    def test_date(self):
        self.assertEqual(date("2024-01-02"), 388.62)
        self.assertFalse(date("2026-03-20"))


if __name__ == '__main__':
    unittest.main()
