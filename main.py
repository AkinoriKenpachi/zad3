import requests
import unittest

code_list = ["USD", "EUR"]

def check(temp):
    try:
        float(temp[0])
    except IndexError:
        print("Musisz podać wartość")
        return 0
    except ValueError:
        print("Wartosc musi być liczbą")
        return 1
    try:
        temp[1].upper().isdigit() or code_list[0].index(temp[1].upper())
    except IndexError:
        print("Musisz podać walute")
        return 2
    except ValueError:
        print("Błędnie podana waluta albo brak jej na liście")
        return 3



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


def interface(text):
    while True:
        print(code_list)
        temp = input(f"Podaj wartość {text} oraz walute z podanych powyżej \nFormat: np. 100 USD:\n").split()
        #check(temp)


class Test(unittest.TestCase):

    def test_date(self):
        self.assertEqual(date("2024-01-02"), 388.62)
        self.assertFalse(date("2026-03-20"))

    def test_check(self):
        temp = []
        self.assertEqual(check(temp), 0)

        temp = [' ', "USD"]
        self.assertEqual(check(temp), 1)

        temp = [100]
        self.assertEqual(check(temp), 2)

        temp = [100, " "]
        self.assertEqual(check(temp), 3)

        temp = [100, "USD"]
        self.assertIsNone(check(temp))


if __name__ == '__main__':
    unittest.main()
