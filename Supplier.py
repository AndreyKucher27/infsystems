import re
import json

class SupplierShort:

    def __init__(self, supplier_id, name, phone, email, inn):
        self.supplier_id = supplier_id
        self.name = name
        self.phone = phone
        self.email = email
        self.inn = inn

    def __set_field(self, field_name, value, validator, error_message):
        if not validator(value):
            raise ValueError(error_message)
        setattr(self, field_name, value)

    @property
    def supplier_id(self): return self._supplier_id
    @supplier_id.setter
    def supplier_id(self, value):
        self.__set_field('_supplier_id', value, self.validate_supplier_id,
                         "ID должен быть положительным числом.")

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value):
        self.__set_field('_name', value, self.validate_name,
                         "Название поставщика не может быть пустым.")

    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, value):
        self.__set_field('_phone', value, self.validate_phone,
                         "Некорректный формат телефона.")

    @property
    def email(self): return self._email
    @email.setter
    def email(self, value):
        self.__set_field('_email', value, self.validate_email,
                         "Некорректный email.")

    @property
    def inn(self): return self._inn
    @inn.setter
    def inn(self, value):
        self.__set_field('_inn', value, self.validate_inn,
                         "ИНН должен содержать 10 или 12 цифр.")

    # --- Методы сравнения и вывода ---
    def __eq__(self, other):
        if not isinstance(other, SupplierShort):
            return False
        return (self.supplier_id == other.supplier_id and
                self.name == other.name and
                self.phone == other.phone and
                self.email == other.email and
                self.inn == other.inn)

    def __str__(self):
        return f"{self.name} — тел: {self.phone}, email: {self.email}, ИНН: {self.inn}"

    def __repr__(self):
        return (f"SupplierShort(supplier_id={self._supplier_id}, name='{self._name}', "
                f"phone='{self._phone}', email='{self._email}', inn='{self._inn}')")

    # --- Статические проверки ---
    @staticmethod
    def validate_supplier_id(value):
        return isinstance(value, int) and value > 0

    @staticmethod
    def validate_name(value):
        return isinstance(value, str) and bool(value.strip())

    @staticmethod
    def validate_phone(value):
        return isinstance(value, str) and bool(re.match(r'^[\d\+\-\(\)\s]+$', value.strip()))

    @staticmethod
    def validate_email(value):
        return isinstance(value, str) and "@" in value

    @staticmethod
    def validate_inn(value):
        return isinstance(value, str) and value.isdigit() and len(value) in (10, 12)



class Supplier(SupplierShort):

    def __init__(self, supplier_id, name, contact_name, phone, email, city, address, inn):
        super().__init__(supplier_id, name, phone, email, inn)
        self.contact_name = contact_name
        self.city = city
        self.address = address

    # --- Инкапсуляция дополнительных полей ---
    @property
    def contact_name(self): return self._contact_name
    @contact_name.setter
    def contact_name(self, value):
        self._contact_name = value.strip() if isinstance(value, str) and value.strip() else \
            ValueError("Контактное лицо не может быть пустым.")

    @property
    def city(self): return self._city
    @city.setter
    def city(self, value):
        if not (isinstance(value, str) and re.match(r'^[A-Za-zА-Яа-яЁё\s\-]+$', value.strip())):
            raise ValueError("Город должен содержать только буквы и пробелы.")
        self._city = value.strip()

    @property
    def address(self): return self._address
    @address.setter
    def address(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Адрес не может быть пустым.")
        self._address = value.strip()

    # --- Альтернативные конструкторы ---
    @classmethod
    def from_string(cls, data_str):
        supplier_id, name, contact_name, phone, email, city, address, inn = data_str.split(';')
        return cls(int(supplier_id), name, contact_name, phone, email, city, address, inn)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
            int(data['supplier_id']), data['name'], data['contact_name'],
            data['phone'], data['email'], data['city'], data['address'], data['inn']
        )

    # --- Методы отображения ---
    def short_info(self):
        """Краткая информация — доступна благодаря наследованию."""
        return super().__str__()

    def display_info(self):
        """Подробная информация о поставщике."""
        print(f"Поставщик: {self.name} ({self.contact_name})")
        print(f"Телефон: {self.phone}, Email: {self.email}")
        print(f"Город: {self.city}, Адрес: {self.address}")
        print(f"ИНН: {self.inn}")

    def __str__(self):
        return (f"{self.name} ({self.contact_name}) — тел: {self.phone}, email: {self.email}\n"
                f"Город: {self.city}, Адрес: {self.address}, ИНН: {self.inn}")

    def __repr__(self):
        return (f"Supplier(supplier_id={self._supplier_id}, name='{self._name}', "
                f"contact_name='{self._contact_name}', phone='{self._phone}', "
                f"email='{self._email}', city='{self._city}', address='{self._address}', "
                f"inn='{self._inn}')")




if __name__ == "__main__":
    s1 = Supplier.from_string("1;ООО АвтоПартс;Иванов;+7 495 123-45-67;info@parts.ru;Москва;ул. Ленина, 1;1234567890")
    s2 = Supplier.from_json('{"supplier_id":1,"name":"ООО АвтоПартс","contact_name":"Иванов","phone":"+7 495 123-45-67","email":"info@parts.ru","city":"Москва","address":"ул. Ленина, 1","inn":"1234567890"}')

    print("Полная версия объекта:")
    print(repr(s1))
    print("\nКраткая версия объекта:")
    print(s1.short_info())
    print("\nСравнение объектов:")
    print(s1 == s2)
