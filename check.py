from Supplier import Supplier
from Supplier_rep_json import Supplier_rep_json

# Путь к файлу JSON
FILE_PATH = "suppliers.json"

# Создаём репозиторий
repo = Supplier_rep_json(FILE_PATH)

print("Пункт a) Чтение всех значений из файла ===")
#Список объектов класса Supplier
#Каждый элемент списка — полноценный объект Supplier
all_suppliers = repo.read_all()
for s in all_suppliers:
    print(s)
print("\nВсего поставщиков:", len(all_suppliers))
print("-" * 50)

print("Пункт b) Добавление нового поставщика и запись в файл ===")
new_supplier = Supplier(
    supplier_id=3,
    name="ООО НоваяФирма",
    contact_name="Сидоров С.С.",
    phone="+7 999 111 22 33",
    email="new@parts.ru",
    city="Казань",
    address="ул. Пушкина, 10",
    inn="7707083893"
)
all_suppliers.append(new_supplier)
repo.write_all(all_suppliers)
print("Новый поставщик добавлен и записан в файл.\n")

print("=== Проверка после добавления ===")
all_suppliers = repo.read_all()
for s in all_suppliers:
    print(s)
print("-" * 50)

print("Пункт c) Получение объекта по ID ===")
supplier_1 = repo.get_by_id(1)
print("Поставщик с ID=1:")
print(supplier_1, "\n")

supplier_999 = repo.get_by_id(999)
print("Поставщик с ID=999 (не существует):")
print(supplier_999)
print("-" * 50)

"""
print("=== Проверка валидации при создании объекта ===")
try:
    bad_supplier = Supplier(
        supplier_id=10,
        name="Плохой",
        contact_name="Иванов И.И.",
        phone="12345",
        email="bademail",
        city="Москва",
        address="ул. Ленина, 15",
        inn="1234567890"
    )
except ValueError as e:
    print("Ошибка валидации поймана:", e)

print("-" * 50)
"""

