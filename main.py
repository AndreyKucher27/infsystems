import json
from datetime import date, datetime

class PurchaseBase:
    def __init__(self, supplier_name, part_article, part_name, quantity):
        self.supplier_name = supplier_name
        self.part_article = part_article
        self.part_name = part_name
        self.quantity = quantity

    @staticmethod
    def validate_text_field(value):
        if not value or not isinstance(value, str):
            raise ValueError("Поле должно быть непустой строкой")
        return value.strip()

    @staticmethod
    def validate_quantity(value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Количество должно быть положительным целым числом")
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
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = self.validate_quantity(value)

    def __eq__(self, other):
        if not isinstance(other, PurchaseBase):
            return False
        return (self.supplier_name == other.supplier_name and
                self.part_article == other.part_article and
                self.part_name == other.part_name and
                self.quantity == other.quantity)


class PurchaseSummary(PurchaseBase):
    def __str__(self):
        return (f"Закупка (кратко): {self.part_name} (арт. {self.part_article})\n"
                f"Поставщик: {self.supplier_name}\n"
                f"Количество: {self.quantity} шт.")

    def __repr__(self):
        return (f"PurchaseSummary({self.supplier_name!r}, {self.part_article!r}, "
                f"{self.part_name!r}, {self.quantity})")

    @classmethod
    def from_purchase(cls, purchase_obj):
        return cls(
            supplier_name=purchase_obj.supplier_name,
            part_article=purchase_obj.part_article,
            part_name=purchase_obj.part_name,
            quantity=purchase_obj.quantity
        )

class Purchase(PurchaseBase):
    def __init__(self, supplier_name, part_article, part_name, part_price, quantity, purchase_date):
        super().__init__(supplier_name, part_article, part_name, quantity)
        self.part_price = part_price
        self.purchase_date = purchase_date

    @staticmethod
    def validate_price(value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Цена должна быть положительным числом")
        return float(value)

    @staticmethod
    def validate_date(value):
        if not isinstance(value, date):
            raise ValueError("Дата должна быть объектом datetime.date")
        if value > date.today():
            raise ValueError("Дата не может быть в будущем")
        return value

    @property
    def part_price(self):
        return self._part_price

    @part_price.setter
    def part_price(self, value):
        self._part_price = self.validate_price(value)

    @property
    def purchase_date(self):
        return self._purchase_date

    @purchase_date.setter
    def purchase_date(self, value):
        self._purchase_date = self.validate_date(value)

    def get_total_cost(self):
        return self.quantity * self.part_price

    def __str__(self):
        return (f"Закупка: {self.part_name} (арт. {self.part_article})\n"
                f"Поставщик: {self.supplier_name}\n"
                f"Количество: {self.quantity} шт. × {self.part_price} руб.\n"
                f"Общая стоимость: {self.get_total_cost()} руб.\n"
                f"Дата: {self.purchase_date.strftime('%d.%m.%Y')}")

    def __repr__(self):
        return (f"Purchase({self.supplier_name!r}, {self.part_article!r}, {self.part_name!r}, "
                f"{self.part_price}, {self.quantity}, {self.purchase_date!r})")

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

# Полная версия
p1 = Purchase("Поставщик А", "123", "Фильтр", 500, 10, date(2025, 10, 11))

# Данные из строки
p2 = Purchase.from_string("Поставщик Б;456;Свеча;300;5;10.10.2025")

# Данные из JSON
p3 = Purchase.from_json('{"supplier_name":"Поставщик В","part_article":"789","part_name":"Тормоз","part_price":1200,"quantity":2,"purchase_date":"11.10.2025"}')

# Вывод полной версии
print(p1)
print(repr(p2))

# Сравнение полной версии
print(p1 == p2)
print(p1 == Purchase("Поставщик А", "123", "Фильтр", 500, 10, date(2025, 10, 11)))  # True

# Краткая версия через наследование
summary1 = PurchaseSummary.from_purchase(p1)
summary2 = PurchaseSummary.from_purchase(p2)

print(summary1)          # читаемая краткая версия
print(repr(summary2))    # краткая версия для разработчика
