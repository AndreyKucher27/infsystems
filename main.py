from datetime import date

class Purchase:
    def __init__(self, supplier_name, part_article, part_name, part_price, quantity, purchase_date):
        self.supplier_name = self.validate_text_field(supplier_name)
        self.part_article = self.validate_text_field(part_article)
        self.part_name = self.validate_text_field(part_name)
        self.part_price = self.validate_price(part_price)
        self.quantity = self.validate_quantity(quantity)
        self.purchase_date = self.validate_date(purchase_date)


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
        return (f"Purchase(supplier_name='{self._supplier_name}', "
                f"part_article='{self._part_article}', part_name='{self._part_name}', "
                f"part_price={self._part_price}, quantity={self._quantity}, "
                f"purchase_date={self._purchase_date})")
