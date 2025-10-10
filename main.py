from datetime import date


class Purchase:
    def __init__(self, supplier_name=None, part_article=None, part_name=None, part_price=None, quantity=None,
                 purchase_date=None):
        self._supplier_name = None
        self._part_article = None
        self._part_name = None
        self._part_price = None
        self._quantity = None
        self._purchase_date = None

        if supplier_name is not None:
            self.supplier_name = supplier_name
        if part_article is not None:
            self.part_article = part_article
        if part_name is not None:
            self.part_name = part_name
        if part_price is not None:
            self.part_price = part_price
        if quantity is not None:
            self.quantity = quantity
        if purchase_date is not None:
            self.purchase_date = purchase_date

    @property
    def supplier_name(self):
        return self._supplier_name

    @supplier_name.setter
    def supplier_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Название поставщика не может быть пустым")
        self._supplier_name = value.strip()

    @property
    def part_article(self):
        return self._part_article

    @part_article.setter
    def part_article(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Артикул детали не может быть пустым")
        self._part_article = value.strip()

    @property
    def part_name(self):
        return self._part_name

    @part_name.setter
    def part_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Название детали не может быть пустым")
        self._part_name = value.strip()

    @property
    def part_price(self):
        return self._part_price

    @part_price.setter
    def part_price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Цена детали должна быть положительным числом")
        self._part_price = float(value)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Количество должно быть положительным целым числом")
        self._quantity = value

    @property
    def purchase_date(self):
        return self._purchase_date

    @purchase_date.setter
    def purchase_date(self, value):
        if not isinstance(value, date):
            raise ValueError("Дата должна быть объектом datetime.date")
        if value > date.today():
            raise ValueError("Дата закупки не может быть в будущем")
        self._purchase_date = value

    def get_total_cost(self):
        if self._part_price is None or self._quantity is None:
            return 0.0
        return self._quantity * self._part_price

    def __str__(self):
        date_str = self._purchase_date.strftime("%d.%m.%Y") if self._purchase_date else "не указана"
        total_cost = self.get_total_cost()

        return (f"Закупка: {self._part_name} (арт. {self._part_article})\n"
                f"Поставщик: {self._supplier_name}\n"
                f"Количество: {self._quantity} шт. × {self._part_price} руб.\n"
                f"Общая стоимость: {total_cost} руб.\n"
                f"Дата: {date_str}")

    def __repr__(self):
        return (f"Purchase(supplier_name='{self._supplier_name}', "
                f"part_article='{self._part_article}', part_name='{self._part_name}', "
                f"part_price={self._part_price}, quantity={self._quantity}, "
                f"purchase_date={self._purchase_date})")

