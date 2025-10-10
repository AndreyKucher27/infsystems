import json
from datetime import date, datetime

class Purchase:
    def __init__(self, supplier_name, part_article, part_name, part_price, quantity, purchase_date):
        self.supplier_name = supplier_name
        self.part_article = part_article
        self.part_name = part_name
        self.part_price = part_price
        self.quantity = quantity
        self.purchase_date = purchase_date

    @staticmethod
    def validate_text_field(value):
        if not value or not isinstance(value, str):
            raise ValueError("Поле должно быть непустой строкой")
        return value.strip()

    @staticmethod
    def validate_price(value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Цена должна быть положительным числом")
        return float(value)

    @staticmethod
    def validate_quantity(value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Количество должно быть положительным целым числом")
        return value

    @staticmethod
    def validate_date(value):
        if not isinstance(value, date):
            raise ValueError("Дата должна быть объектом datetime.date")
        if value > date.today():
            raise ValueError("Дата не может быть в будущем")
        return value

    @property
    def supplier_name(self):
        return self._supplier_name

    @supplier_name.setter
    def supplier_name(self, value):
        self._supplier_name = self.validate_text_field(value)

    @property
    def part_article(self):
        return self._part_article

    @part_article.setter
    def part_article(self, value):
        self._part_article = self.validate_text_field(value)

    @property
    def part_name(self):
        return self._part_name

    @part_name.setter
    def part_name(self, value):
        self._part_name = self.validate_text_field(value)

    @property
    def part_price(self):
        return self._part_price

    @part_price.setter
    def part_price(self, value):
        self._part_price = self.validate_price(value)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = self.validate_quantity(value)

    @property
    def purchase_date(self):
        return self._purchase_date

    @purchase_date.setter
    def purchase_date(self, value):
        self._purchase_date = self.validate_date(value)

    def get_total_cost(self):
        return self._quantity * self._part_price

    def __str__(self):
        return (f"Закупка: {self._part_name} (арт. {self._part_article})\n"
                f"Поставщик: {self._supplier_name}\n"
                f"Количество: {self._quantity} шт. × {self._part_price} руб.\n"
                f"Общая стоимость: {self.get_total_cost()} руб.\n"
                f"Дата: {self._purchase_date.strftime('%d.%m.%Y')}")

    def __repr__(self):
        return (f"Purchase({self._supplier_name!r}, {self._part_article!r}, {self._part_name!r}, "
                f"{self._part_price}, {self._quantity}, {self._purchase_date!r})")

    def __eq__(self, other):
        """Сравнение"""
        if not isinstance(other, Purchase):
            return False
        return (self.supplier_name == other.supplier_name and
                self.part_article == other.part_article and
                self.part_name == other.part_name and
                self.part_price == other.part_price and
                self.quantity == other.quantity and
                self.purchase_date == other.purchase_date)

    #Перегрузка
    @classmethod
    def from_string(cls, data_str):
        parts = data_str.split(';')
        if len(parts) != 6:
            raise ValueError("Строка должна содержать 6 полей, разделённых ';'")
        supplier, article, name, price, quantity, date_str = parts
        purchase_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        return cls(supplier, article, name, float(price), int(quantity), purchase_date)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        purchase_date = datetime.strptime(data['purchase_date'], "%d.%m.%Y").date()
        return cls(
            data['supplier_name'],
            data['part_article'],
            data['part_name'],
            float(data['part_price']),
            int(data['quantity']),
            purchase_date
        )

from datetime import date

# Обычный 
p1 = Purchase("Поставщик А", "123", "Фильтр", 500, 10, date(2025, 10, 11))

# Данные из строки
p2 = Purchase.from_string("Поставщик Б;456;Свеча;300;5;10.10.2025")

# Данные из JSON
p3 = Purchase.from_json('{"supplier_name":"Поставщик В","part_article":"789","part_name":"Тормоз","part_price":1200,"quantity":2,"purchase_date":"11.10.2025"}')

# Полная версия
print(p1)

# Краткая
print(repr(p2))

# Сравнение
print(p1 == p2)
print(p1 == Purchase("Поставщик А", "123", "Фильтр", 500, 10, date(2025, 10, 11)))  # True
