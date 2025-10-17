import re
import json

class Supplier:
    """Класс, представляющий поставщика компании."""

    def __init__(self, supplier_id, name, contact_name, phone, email, city, address, inn):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_name = contact_name
        self.phone = phone
        self.email = email
        self.city = city
        self.address = address
        self.inn = inn

    def __set_field(self, field_name, value, validator, error_message):
        """Приватный метод для установки полей с проверкой данных."""
        if not validator(value):
            raise ValueError(error_message)
        setattr(self, field_name, value)


    @property
    def supplier_id(self): return self._supplier_id
    @supplier_id.setter
    def supplier_id(self, value):
        self.__set_field('_supplier_id', value, self.validate_supplier_id,
                         "Идентификатор поставщика должен быть положительным числом.")

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value):
        self.__set_field('_name', value, self.validate_name, "Название поставщика не может быть пустым.")

    @property
    def contact_name(self): return self._contact_name
    @contact_name.setter
    def contact_name(self, value):
        self.__set_field('_contact_name', value, self.validate_contact_name,
                         "Контактное лицо не может быть пустым.")

    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, value):
        self.__set_field('_phone', value, self.validate_phone, "Некорректный формат телефона.")

    @property
    def email(self): return self._email
    @email.setter
    def email(self, value):
        self.__set_field('_email', value, self.validate_email, "Некорректный адрес электронной почты.")

    @property
    def city(self): return self._city
    @city.setter
    def city(self, value):
        self.__set_field('_city', value, self.validate_city,
                         "Город не может быть пустым и должен содержать только буквы и пробелы.")

    @property
    def address(self): return self._address
    @address.setter
    def address(self, value):
        self.__set_field('_address', value, self.validate_address, "Адрес не может быть пустым.")

    @property
    def inn(self): return self._inn
    @inn.setter
    def inn(self, value):
        self.__set_field('_inn', value, self.validate_inn, "ИНН должен содержать 10 или 12 цифр.")

    @classmethod
    def from_string(cls, data_str):
        """Создание объекта из строки, разделённой ';'."""
        supplier_id, name, contact_name, phone, email, city, address, inn = data_str.split(';')
        return cls(int(supplier_id), name, contact_name, phone, email, city, address, inn)

    @classmethod
    def from_json(cls, json_str):
        """Создание объекта из JSON-строки."""
        data = json.loads(json_str)
        return cls(
            int(data['supplier_id']),
            data['name'],
            data['contact_name'],
            data['phone'],
            data['email'],
            data['city'],
            data['address'],
            data['inn']
        )

    def display_info(self):
        """Вывод полной информации о поставщике."""
        print(f"Поставщик: {self.name}")
        print(f"Контактное лицо: {self.contact_name}")
        print(f"Телефон: {self.phone}, Email: {self.email}")
        print(f"Город: {self.city}, Адрес: {self.address}")
        print(f"ИНН: {self.inn}")

    def short_info(self):
        """Краткая версия объекта."""
        return f"{self.name} ({self.contact_name}) — Тел: {self.phone}, Email: {self.email}"

    def __str__(self):
        """Полная строковая версия объекта."""
        return (f"{self.name} ({self.contact_name})\n"
                f"Телефон: {self.phone}, Email: {self.email}\n"
                f"Город: {self.city}, Адрес: {self.address}\n"
                f"ИНН: {self.inn}")

    def __repr__(self):
        return (f"Supplier(supplier_id={self._supplier_id}, name={self._name!r}, "
                f"contact_name={self._contact_name!r}, phone={self._phone!r}, "
                f"email={self._email!r}, city={self._city!r}, "
                f"address={self._address!r}, inn={self._inn!r})")

    def __eq__(self, other):
        """Сравнение"""
        if not isinstance(other, Supplier):
            return False
        return (self.supplier_id == other.supplier_id and
                self.name == other.name and
                self.contact_name == other.contact_name and
                self.phone == other.phone and
                self.email == other.email and
                self.city == other.city and
                self.address == other.address and
                self.inn == other.inn)

    @staticmethod
    def validate_supplier_id(value):
        return isinstance(value, int) and value > 0

    @staticmethod
    def validate_name(value):
        return isinstance(value, str) and bool(value.strip())

    @staticmethod
    def validate_contact_name(value):
        return isinstance(value, str) and bool(value.strip())

    @staticmethod
    def validate_phone(value):
        """Телефон может содержать цифры, +, -, пробелы и скобки."""
        if not isinstance(value, str) or not value.strip():
            return False
        pattern = r'^[\d\+\-\(\)\s]+$'
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_email(value):
        return isinstance(value, str) and "@" in value

    @staticmethod
    def validate_city(value):
        """Город не пустой, только буквы и пробелы."""
        if not isinstance(value, str) or not value.strip():
            return False
        pattern = r'^[A-Za-zА-Яа-яЁё\s\-]+$'
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_address(value):
        """Адрес не может быть пустым."""
        return isinstance(value, str) and bool(value.strip())

    @staticmethod
    def validate_inn(value):
        """ИНН — строка из 10 или 12 цифр."""
        return isinstance(value, str) and value.isdigit() and len(value) in (10, 12)

class SupplierShort:
    """Краткая версия класса Supplier (без адреса и контактного лица)."""

    def __init__(self, supplier_id, name, phone, email, inn):
        self.supplier_id = supplier_id
        self.name = name
        self.phone = phone
        self.email = email
        self.inn = inn

    # --- Инкапсуляция ---
    @property
    def supplier_id(self): return self._supplier_id
    @supplier_id.setter
    def supplier_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Идентификатор должен быть положительным числом.")
        self._supplier_id = value

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название поставщика не может быть пустым.")
        self._name = value.strip()

    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Телефон не может быть пустым.")
        self._phone = value.strip()

    @property
    def email(self): return self._email
    @email.setter
    def email(self, value):
        if not isinstance(value, str) or '@' not in value:
            raise ValueError("Некорректный email.")
        self._email = value.strip()

    @property
    def inn(self): return self._inn
    @inn.setter
    def inn(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) in (10, 12)):
            raise ValueError("ИНН должен содержать 10 или 12 цифр.")
        self._inn = value

    # --- Альтернативный конструктор ---
    @classmethod
    def from_supplier(cls, supplier):
        """Создание краткого объекта на основе полного объекта Supplier."""
        return cls(
            supplier.supplier_id,
            supplier.name,
            supplier.phone,
            supplier.email,
            supplier.inn
        )

    # --- Методы отображения ---
    def __str__(self):
        return f"{self.name} — тел: {self.phone}, email: {self.email}, ИНН: {self.inn}"

    def __repr__(self):
        return (f"SupplierShort(supplier_id={self._supplier_id}, "
                f"name='{self._name}', phone='{self._phone}', "
                f"email='{self._email}', inn='{self._inn}')")

    def __eq__(self, other):
        if not isinstance(other, SupplierShort):
            return False
        return (self.supplier_id == other.supplier_id and
                self.name == other.name and
                self.phone == other.phone and
                self.email == other.email and
                self.inn == other.inn)


if __name__ == "__main__":
    s1 = Supplier.from_string("1;ООО АвтоПартс;Иванов;+7 495 123-45-67;info@parts.ru;Москва;ул. Ленина, 1;1234567890")
    s2 = Supplier.from_json('{"supplier_id":1,"name":"ООО АвтоПартс","contact_name":"Иванов","phone":"+7 495 123-45-67","email":"info@parts.ru","city":"Москва","address":"ул. Ленина, 1","inn":"1234567890"}')

    print("Полная версия объекта:")
    print(repr(s1))
    print("\nКраткая версия объекта:")
    print(s1.short_info())
    print("\nСравнение объектов:")
    print(s1 == s2)

    print("\nСоздаём краткий объект на основе полного:")
    short_supplier = SupplierShort.from_supplier(s1)
    print(short_supplier)

    print("\nrepr краткого объекта:")
    print(repr(short_supplier))

