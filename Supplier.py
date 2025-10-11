from datetime import date


class Supplier:
    def __init__(self, supplier_name=None, supplier_address=None, supplier_phone=None):
        self._supplier_name = None
        self._supplier_address = None
        self._supplier_phone = None

        if supplier_name is not None:
            self.supplier_name = supplier_name
        if supplier_address is not None:
            self.supplier_address = supplier_address
        if supplier_phone is not None:
            self.supplier_phone = supplier_phone

    @property
    def supplier_name(self):
        return self._supplier_name

    @supplier_name.setter
    def supplier_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Название поставщика не может быть пустым")
        self._supplier_name = value.strip()

    @property
    def supplier_address(self):
        return self._supplier_address

    @supplier_address.setter
    def supplier_address(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Адрес поставщика не может быть пустым")
        self._supplier_address = value.strip()

    @property
    def supplier_phone(self):
        return self._supplier_phone

    @supplier_phone.setter
    def supplier_phone(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Телефон поставщика не может быть пустым")
        self._supplier_phone = value.strip()

    def __str__(self):
        return (f"Поставщик: {self.supplier_name}\n"
                f"Адрес: {self.supplier_address}\n"
                f"Телефон: {self.supplier_phone}")

    def __repr__(self):
        return (f"Supplier(supplier_name='{self.supplier_name}', "
                f"supplier_address='{self.supplier_address}', "
                f"supplier_phone='{self.supplier_phone}')")


print("\n1. СОЗДАНИЕ ПОСТАВЩИКОВ:")
print("-" * 30)

supplier1 = Supplier(
    supplier_name="   ООО Автодеталь   ",
    supplier_address="Москва, ул. Промышленная, 15",
    supplier_phone="+7-495-111-2233"
)

print("Поставщик 1 создан:")
print(supplier1)
print()

# Второй поставщика
supplier2 = Supplier(
    supplier_name="ЗАО Автозапчасти",
    supplier_address="   Санкт-Петербург, пр. Металлистов, 28   ",
    supplier_phone="+7-812-222-3344"
)

print("Поставщик 2 создан:")
print(supplier2)
print()

# 2. ДЕМОНСТРАЦИЯ repr
print("\n2. ПРЕДСТАВЛЕНИЕ ДЛЯ РАЗРАБОТЧИКОВ (repr):")
print("-" * 40)
print(f"supplier1 repr: {repr(supplier1)}")
print(f"supplier2 repr: {repr(supplier2)}")


# 3. ДОСТУП К СВОЙСТВАМ
print("\n3. ДОСТУП К ОТДЕЛЬНЫМ СВОЙСТВАМ:")
print("-" * 35)
print(f"Название 1-го поставщика: '{supplier1.supplier_name}'")
print(f"Адрес 2-го поставщика: '{supplier2.supplier_address}'")
print(f"Телефон 1-го поставщика: '{supplier1.supplier_phone}'")

# 4. ИЗМЕНЕНИЕ ДАННЫХ
print("\n4. ИЗМЕНЕНИЕ ДАННЫХ ПОСТАВЩИКА:")
print("-" * 35)
print("До изменения:")
print(f"Телефон supplier1: '{supplier1.supplier_phone}'")

supplier1.supplier_phone = "   +7-495-999-8877   "
print("После изменения:")
print(f"Телефон supplier1: '{supplier1.supplier_phone}'")

# 5. ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ
print("\n5. ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ ДАННЫХ:")
print("-" * 40)

print("Попытка создать поставщика с пустым именем:")
try:
    bad_supplier = Supplier(supplier_name="")
    print("Ошибка не сработала!")
except ValueError as e:
    print(f" {e}")

print("\nПопытка создать поставщика с числом вместо имени:")
try:
    bad_supplier = Supplier(supplier_name=123)
    print("Ошибка не сработала!")
except ValueError as e:
    print(f" {e}")

print("\nПопытка установить пустой адрес:")
try:
    supplier1.supplier_address = ""
    print("Ошибка не сработала!")
except ValueError as e:
    print(f" {e}")


#СОЗДАНИЕ ЧАСТИЧНО ЗАПОЛНЕННОГО ПОСТАВЩИКА
print("\n6. СОЗДАНИЕ ЧАСТИЧНО ЗАПОЛНЕННОГО ПОСТАВЩИКА:")
print("-" * 50)

supplier3 = Supplier(supplier_name="ИП Петров")
print("Поставщик создан только с именем:")
print(supplier3)

supplier3.supplier_address = "Казань, ул. Центральная, 10"
supplier3.supplier_phone = "+7-843-333-4455"
print("\nПосле заполнения всех данных:")
print(supplier3)

print("\n7. АВТОМАТИЧЕСКОЕ УДАЛЕНИЕ ПРОБЕЛОВ:")
print("-" * 40)

supplier4 = Supplier(
    supplier_name="   ТОО АвтоСервис   ",
    supplier_address="   Екатеринбург, ул. Заводская, 25   ",
    supplier_phone="   +7-343-444-5566   "
)

print("Создан с пробелами:")
print(f"Имя: '{supplier4.supplier_name}'")
print(f"Адрес: '{supplier4.supplier_address}'")
print(f"Телефон: '{supplier4.supplier_phone}'")

print("\n" + "=" * 50)
print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
print("=" * 50)