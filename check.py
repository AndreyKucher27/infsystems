from Supplier import Supplier
from Supplier_rep_json import Supplier_rep_json
from Supplier_rep_yaml import Supplier_rep_yaml

#Универсальная функция для теста работы репозиториев
#Принимает любой репозиторий (JSOM и YAML)
def test_repository(repo, title):
    print(f"\n===== Проверка {title} =====")

    # Чтение всех значений из файла (Пункт a)
    print("a) read_all")
    for s in repo.read_all():
        print(s)
    print("Всего:", repo.get_count())
    print("-" * 40)

    # Получение объекта по ID (Пункт c)
    print("c) get_by_id(1)")
    print(repo.get_by_id(1))
    print("-" * 40)

    # Пагинация (Пункт d)
    print("d) get_k_n_short_list(3, 1)")
    for s in repo.get_k_n_short_list(3, 1):
        print(s)
    print("-" * 40)

    # Сортировка элементов по выбранному полю (Пункт е)
    print("e) sort_by_city")
    for s in repo.sort_by_city():
        print(s)
    print("-" * 40)

    # Добавление элемента (Пункт f)
    print("f) add_supplier")
    new_supplier = Supplier(
        supplier_id=1,
        name="ООО Тест",
        contact_name="Тест Т.Т.",
        phone="+7 900 000 00 00",
        email="test@test.ru",
        city="Тула",
        address="ул. Тестовая, 1",
        inn="7707083893"
    )
    repo.add_supplier(new_supplier)
    print(repo.get_by_id(new_supplier.supplier_id))
    print("-" * 40)

    # Замена элемента списка по ID (Пункт g)
    print("g) replace_by_id")
    new_supplier.city = "Рязань"
    print(repo.replace_by_id(new_supplier.supplier_id, new_supplier))
    print(repo.get_by_id(new_supplier.supplier_id))
    print("-" * 40)

    # Удалить элемент списка по ID (Пункт h)
    print("h) delete_by_id")
    print(repo.delete_by_id(new_supplier.supplier_id))

    # Получить количество элементов (Пункт i)
    print("Осталось:", repo.get_count())
    print("-" * 40)


json_repo = Supplier_rep_json("suppliers.json")
yaml_repo = Supplier_rep_yaml("suppliers.yaml")

test_repository(json_repo, "JSON")
test_repository(yaml_repo, "YAML")
