import requests
import unittest
import csv
import os.path


code_list: list = []


def code_list_select(res):
    clist: list = []
    temp: list = []
    for x in res:
        temp.append(x['rates'])
    for x in temp:
        for y in range(len(x)):
            clist.append(x[y]['code'])
    return clist


def code_list_create(cl):
    communication = requests.get(
        f'https://api.nbp.pl/api/exchangerates/tables/c/?format=json')
    response = communication.json()
    cl.append(code_list_select(response))
    if not os.path.isfile("codelist.txt"):
        with open('codelist.txt', 'w', newline='', encoding='UTF8') as code_file:
            csv.writer(code_file).writerow(cl[0])
            code_file.close()


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
        code_list_create(code_list)
        print(open('codelist.txt').read())
        temp = input(f"Podaj wartość {text} oraz walute z podanych powyżej "
                     f"\nw format [waluta kod-waluty np. 100 USD]\n").split()
        check(temp)


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
    # unittest.main()
    interface("faktury")
