import re

class Supplier:

    def __init__(self, supplier_id, name, contact_name, phone, email, city, address, inn):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_name = contact_name
        self.phone = phone
        self.email = email
        self.city = city
        self.address = address
        self.inn = inn

    #Метод для сеттеров с валидацией
    def __set_field(self, field_name, value, validator, error_message):
        if not validator(value):
            raise ValueError(error_message)
        setattr(self, field_name, value)

    @property
    def supplier_id(self): return self.__supplier_id
    @supplier_id.setter
    def supplier_id(self, value):
        self.__set_field('__supplier_id', value, self.validate_supplier_id,
                         "Идентификатор поставщика должен быть положительным числом.")

    @property
    def name(self): return self.__name
    @name.setter
    def name(self, value):
        self.__set_field('__name', value, self.validate_name, "Название поставщика не может быть пустым.")

    @property
    def contact_name(self): return self.__contact_name
    @contact_name.setter
    def contact_name(self, value):
        self.__set_field('__contact_name', value, self.validate_contact_name,
                         "Контактное лицо не может быть пустым.")

    @property
    def phone(self): return self.__phone
    @phone.setter
    def phone(self, value):
        self.__set_field('__phone', value, self.validate_phone, "Некорректный формат телефона.")

    @property
    def email(self): return self.__email
    @email.setter
    def email(self, value):
        self.__set_field('__email', value, self.validate_email, "Некорректный адрес электронной почты.")

    @property
    def city(self): return self.__city
    @city.setter
    def city(self, value):
        self.__set_field('__city', value, self.validate_city,
                         "Город не может быть пустым и должен содержать только буквы и пробелы.")

    @property
    def address(self): return self.__address
    @address.setter
    def address(self, value):
        self.__set_field('__address', value, self.validate_address, "Адрес не может быть пустым.")

    @property
    def inn(self): return self.__inn
    @inn.setter
    def inn(self, value):
        self.__set_field('__inn', value, self.validate_inn, "ИНН должен содержать 10 или 12 цифр.")

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
