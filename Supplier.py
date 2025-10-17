class Supplier:

    def __init__(self, supplier_id, name, contact_name, phone, email, city, address, inn):
        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_name = contact_name
        self.__phone = phone
        self.__email = email
        self.__city = city
        self.__address = address
        self.__inn = inn

    @property
    def supplier_id(self):
        return self.__supplier_id

    @supplier_id.setter
    def supplier_id(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Идентификатор поставщика должен быть положительным числом.")
        self.__supplier_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Название поставщика не может быть пустым.")
        self.__name = value

    @property
    def contact_name(self):
        return self.__contact_name

    @contact_name.setter
    def contact_name(self, value):
        self.__contact_name = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Некорректный адрес электронной почты.")
        self.__email = value

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        self.__city = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value):
        if not value.isdigit() or len(value) not in (10, 12):
            raise ValueError("ИНН должен содержать 10 или 12 цифр.")
        self.__inn = value

#Вывод
    def display_info(self):
        """Выводит краткую информацию о поставщике"""
        print(f"Поставщик: {self.__name}")
        print(f"Контактное лицо: {self.__contact_name}")
        print(f"Телефон: {self.__phone}, Email: {self.__email}")
        print(f"Город: {self.__city}, Адрес: {self.__address}")
        print(f"ИНН: {self.__inn}")
