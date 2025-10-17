import re

class Supplier:

    def __init__(self, supplier_id, name, contact_name, phone, email, city, address, inn):
        # Валидация всех полей
        if not self.validate_supplier_id(supplier_id):
            raise ValueError("Идентификатор поставщика должен быть положительным числом.")
        if not self.validate_name(name):
            raise ValueError("Название поставщика не может быть пустым.")
        if not self.validate_contact_name(contact_name):
            raise ValueError("Контактное лицо не может быть пустым.")
        if not self.validate_phone(phone):
            raise ValueError("Некорректный формат телефона.")
        if not self.validate_email(email):
            raise ValueError("Некорректный адрес электронной почты.")
        if not self.validate_city(city):
            raise ValueError("Город не может быть пустым и должен содержать только буквы и пробелы.")
        if not self.validate_address(address):
            raise ValueError("Адрес не может быть пустым.")
        if not self.validate_inn(inn):
            raise ValueError("ИНН должен содержать 10 или 12 цифр.")

        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_name = contact_name
        self.__phone = phone
        self.__email = email
        self.__city = city
        self.__address = address
        self.__inn = inn

    @property
    def supplier_id(self): return self.__supplier_id
    @supplier_id.setter
    def supplier_id(self, value):
        if not self.validate_supplier_id(value):
            raise ValueError("Идентификатор поставщика должен быть положительным числом.")
        self.__supplier_id = value

    @property
    def name(self): return self.__name
    @name.setter
    def name(self, value):
        if not self.validate_name(value):
            raise ValueError("Название поставщика не может быть пустым.")
        self.__name = value

    @property
    def contact_name(self): return self.__contact_name
    @contact_name.setter
    def contact_name(self, value):
        if not self.validate_contact_name(value):
            raise ValueError("Контактное лицо не может быть пустым.")
        self.__contact_name = value

    @property
    def phone(self): return self.__phone
    @phone.setter
    def phone(self, value):
        if not self.validate_phone(value):
            raise ValueError("Некорректный формат телефона.")
        self.__phone = value

    @property
    def email(self): return self.__email
    @email.setter
    def email(self, value):
        if not self.validate_email(value):
            raise ValueError("Некорректный адрес электронной почты.")
        self.__email = value

    @property
    def city(self): return self.__city
    @city.setter
    def city(self, value):
        if not self.validate_city(value):
            raise ValueError("Город не может быть пустым и должен содержать только буквы и пробелы.")
        self.__city = value

    @property
    def address(self): return self.__address
    @address.setter
    def address(self, value):
        if not self.validate_address(value):
            raise ValueError("Адрес не может быть пустым.")
        self.__address = value

    @property
    def inn(self): return self.__inn
    @inn.setter
    def inn(self, value):
        if not self.validate_inn(value):
            raise ValueError("ИНН должен содержать 10 или 12 цифр.")
        self.__inn = value

    def display_info(self):
        print(f"Поставщик: {self.__name}")
        print(f"Контактное лицо: {self.__contact_name}")
        print(f"Телефон: {self.__phone}, Email: {self.__email}")
        print(f"Город: {self.__city}, Адрес: {self.__address}")
        print(f"ИНН: {self.__inn}")

    def __str__(self):
        return (f"{self.__name} ({self.__contact_name})\n"
                f"Телефон: {self.__phone}, Email: {self.__email}\n"
                f"Город: {self.__city}, Адрес: {self.__address}\n"
                f"ИНН: {self.__inn}")

    def __repr__(self):
        return (f"Supplier(supplier_id={self.__supplier_id}, name={self.__name!r}, "
                f"contact_name={self.__contact_name!r}, phone={self.__phone!r}, "
                f"email={self.__email!r}, city={self.__city!r}, "
                f"address={self.__address!r}, inn={self.__inn!r})")

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
        """Телефон может содержать цифры, +, -, пробелы и скобки"""
        if not isinstance(value, str) or not value.strip():
            return False
        pattern = r'^[\d\+\-\(\)\s]+$'
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_email(value):
        return isinstance(value, str) and "@" in value

    @staticmethod
    def validate_city(value):
        """Город не пустой, только буквы и пробелы"""
        if not isinstance(value, str) or not value.strip():
            return False
        pattern = r'^[A-Za-zА-Яа-яЁё\s\-]+$'
        return bool(re.match(pattern, value))

    @staticmethod
    def validate_address(value):
        """Адрес не может быть пустым"""
        return isinstance(value, str) and bool(value.strip())

    @staticmethod
    def validate_inn(value):
        return isinstance(value, str) and value.isdigit() and len(value) in (10, 12)
