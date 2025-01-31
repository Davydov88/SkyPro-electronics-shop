import os
from csv import DictReader


class Item:
    """
    Класс для представления товара в магазине.
    """
    pay_rate = 1.0
    all = []

    def __init__(self, name: str, price: int, quantity: int) -> None:
        """
        Создание экземпляра класса item.

        :param name: Название товара.
        :param price: Цена за единицу товара.
        :param quantity: Количество товара в магазине.
        """
        if not isinstance(name, str):
            raise ValueError("Название должно быть строкой")
        else:
            self.__name = name

        if not isinstance(price, int):
            raise ValueError("Цена должна быть целым числом")
        else:
            self.price = price

        if not isinstance(quantity, int):
            raise ValueError("Кол-во должно быть целым числом")
        else:
            self.quantity = quantity

        self.all.append(self)

    def __repr__(self):
        return f"Item('{self.name}', {self.price}, {self.quantity})"

    def __str__(self):
        return f"{self.name}"

    def __add__(self, other):
        """ Переопределяет метод сложения количества товаров"""
        if not isinstance(other, self.__class__):
            raise ValueError("Невозможно сложить разные товары")
        return self.quantity + other.quantity

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def calculate_total_price(self) -> float:
        """
        Рассчитывает общую стоимость конкретного товара в магазине.

        :return: Общая стоимость товара.
        """
        total_item_price = self.price * self.quantity
        return total_item_price

    def apply_discount(self) -> None:
        """
        Применяет установленную скидку для конкретного товара.
        """
        self.price = self.price * self.pay_rate

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name):
        try:
            if len(name) <= 10:
                self.__name: str = name
        except:
            raise Exception(f"Длина наименования товара {name} превышает 10 симвовов")

    @staticmethod
    def load_csv() -> list:
        filedir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filedir, 'items.csv')
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Отсутствует файл {filename}")

        data = []
        with open(filename, 'r+', encoding='windows-1251') as csv_file:
            csv_reader = DictReader(csv_file)
            for item in csv_reader:
                data.append(item)
        return data

    @classmethod
    def instantiate_from_csv(cls) -> None:
        try:
            cls.all = []
            data = Item.load_csv()
            for line in data:
                cls(
                    line['name'],
                    cls.string_to_number(line['price']),
                    cls.string_to_number(line['quantity'])
                )
        except FileNotFoundError:
            raise FileNotFoundError("Отсутствует файл item.csv")
        except:
            raise InstantiateCSVError("Файл item.csv поврежден")

    @staticmethod
    def string_to_number(string) -> int:
        if "." in string:
            str_to_float: float = float(string)
            str_to_int: int = int(str_to_float)
        else:
            str_to_int: int = int(string)
        return str_to_int

    def test_instantiate_from_csv(self):
        Item.instantiate_from_csv()
        assert len(Item.all) == 5

class InstantiateCSVError(Exception):
    pass