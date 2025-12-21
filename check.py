from Supplier import Supplier
from Supplier_rep_json import Supplier_rep_json

# Путь к файлу JSON
FILE_PATH = "suppliers.json"

# Создаём репозиторий
repo = Supplier_rep_json(FILE_PATH)

print("Пункт a) Чтение всех значений из файла ===")
# Список объектов класса Supplier
all_suppliers = repo.read_all()
for s in all_suppliers:
    print(s)

print("\nВсего поставщиков:", len(all_suppliers))
print("-" * 50)


print("Пункт b) Запись всех значений в файл ===")
# В пункте b мы НИЧЕГО не добавляем, а просто проверяем,
# что текущий список корректно сохраняется
repo.write_all(all_suppliers)
print("Список поставщиков сохранён без изменений.")
print("-" * 50)


print("Пункт c) Получение объекта по ID ===")
supplier_1 = repo.get_by_id(1)
print("Поставщик с ID = 1:")
print(supplier_1, "\n")

supplier_999 = repo.get_by_id(999)
print("Поставщик с ID = 999 (не существует):")
print(supplier_999)
print("-" * 50)


print("Пункт d) Получение подсписка SupplierShort (get_k_n_short_list) ===")
k = 5  # количество элементов на странице
n = 2  # номер страницы

page = repo.get_k_n_short_list(k, n)
print(f"Страница {n}, элементов на странице: {k}")
for s in page:
    print(s)

print("-" * 50)


print("Пункт e) Сортировка поставщиков по городу ===")
sorted_suppliers = repo.sort_by_city()
for s in sorted_suppliers:
    print(s)

print("-" * 50)


print("Пункт f) Добавление нового поставщика с автогенерацией ID ===")
# ID НЕ задаём — он будет сформирован автоматически
new_supplier = Supplier(
    supplier_id=1, #supplier_id будет перезаписан репозиторием
    name="ООО НовыйПоставщик",
    contact_name="Орлов О.О.",
    phone="+7 900 555 66 77",
    email="new@supplier.ru",
    city="Екатеринбург",
    address="ул. Мира, 20",
    inn="7707083893"
)

added_supplier = repo.add_supplier(new_supplier)

print("Добавлен поставщик:")
print(added_supplier)

print("-" * 50)

print("Пункт i) Количество элементов ===")
count = repo.get_count()
print("Количество поставщиков:", count)
print("-" * 50)


print("Пункт g) Замена поставщика по ID ===")
replacement = Supplier(
    supplier_id=999,  # будет перезаписан
    name="ООО ОбновлённыйПоставщик",
    contact_name="Новый Контакт",
    phone="+7 900 000 00 00",
    email="updated@supplier.ru",
    city="Пермь",
    address="ул. Новая, 1",
    inn="7707083893"
)

result = repo.replace_by_id(1, replacement)
print("Замена выполнена:", result)
print(repo.get_by_id(1))
print("-" * 50)


print("Пункт h) Удаление поставщика по ID ===")
delete_result = repo.delete_by_id(2)
print("Удаление выполнено:", delete_result)
print("Осталось поставщиков:", repo.get_count())
print("-" * 50)

