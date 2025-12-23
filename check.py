import time
import random

from Supplier import Supplier
from Supplier_rep_json import Supplier_rep_json
from Supplier_rep_yaml import Supplier_rep_yaml
from Supplier_rep_DB import Supplier_rep_DB


MODE = "add_only"
SHOW_READ_ALL = True
K, N = 3, 1


def generate_valid_inn_10(seed: int | None = None) -> str:
    """
    Генерация валидного 10-значного ИНН под твою проверку (контрольная цифра).
    """
    if seed is not None:
        rnd = random.Random(seed)
    else:
        rnd = random.Random()

    digits9 = [rnd.randint(0, 9) for _ in range(9)]
    ctrl_nums = [2, 4, 10, 3, 5, 9, 4, 6, 8]
    s = sum(digits9[i] * ctrl_nums[i] for i in range(9)) % 11 % 10
    return "".join(map(str, digits9)) + str(s)


def make_test_supplier(prefix="Тест"):
    """
    Создаём нового поставщика для теста с уникальными name/email/phone/inn,
    иначе add будет запрещён твоим правилом уникальности.
    """
    unique = int(time.time() * 1000) % 1000000  # достаточно для демо
    inn = generate_valid_inn_10(seed=unique)

    # телефон: делаем уникальные цифры, формат допустим твоим валидатором
    phone = f"+7 900 {unique // 1000:03d} {unique % 1000:03d}"

    email = f"test{unique}@test.ru"
    name = f"ООО {prefix}_{unique}"

    return Supplier(
        supplier_id=1,  # переопределится репозиторием/БД
        name=name,
        contact_name=f"{prefix} Т.Т.",
        phone=phone,
        email=email,
        city="Тула",
        address="ул. Тестовая, 1",
        inn=inn
    )


def test_file_repository(repo, title):
    print(f"\n===== Проверка {title} (MODE={MODE}) =====")

    print("get_count:", repo.get_count())

    if SHOW_READ_ALL:
        print("\nread_all:")
        for s in repo.read_all():
            print(s)

    print("\nget_by_id(1):")
    print(repo.get_by_id(1))

    print(f"\nget_k_n_short_list({K}, {N}):")
    for s in repo.get_k_n_short_list(K, N):
        print(s)

    print("\nsort_by_city:")
    for s in repo.sort_by_city():
        print(s)

    if MODE in ("demo", "full", "add_only"):
        print("\nADD:")
        new_supplier = make_test_supplier(prefix=f"Тест_{title}")
        before = repo.get_count()
        try:
            repo.add_supplier(new_supplier)
            after = repo.get_count()
            print("Добавлен id =", new_supplier.supplier_id)
            print("count:", before, "->", after)
            print(repo.get_by_id(new_supplier.supplier_id))
        except ValueError as e:
            print("ADD запрещён:", e)

    if MODE in ("demo", "full", "replace_only"):
        print("\nREPLACE:")
        supplier_id = 1
        existing = repo.get_by_id(supplier_id)
        if existing is None:
            print("Нечего заменять: supplier_id=1 не найден")
        else:
            try:
                existing.city = "Рязань"
                ok = repo.replace_by_id(supplier_id, existing)
                print("Заменено:", ok)
                print(repo.get_by_id(supplier_id))
            except ValueError as e:
                print("REPLACE запрещён:", e)

    if MODE in ("demo", "full", "delete_only"):
        print("\nDELETE:")
        supplier_id = 1
        before = repo.get_count()
        ok = repo.delete_by_id(supplier_id)
        after = repo.get_count()
        print("Удалено:", ok, "id=", supplier_id)
        print("count:", before, "->", after)

    print("\nИТОГ get_count:", repo.get_count())
    print("-" * 60)


def test_db_repository(repo, title):
    print(f"\n===== Проверка {title} (MODE={MODE}) =====")

    print("get_count:", repo.get_count())

    print("\nget_by_id(1):")
    print(repo.get_by_id(1))

    print(f"\nget_k_n_short_list({K}, {N}):")
    for s in repo.get_k_n_short_list(K, N):
        print(s)

    if MODE in ("demo", "full", "add_only"):
        print("\nADD:")
        new_supplier = make_test_supplier(prefix="ТестDB")
        before = repo.get_count()
        try:
            repo.add_supplier(new_supplier)
            after = repo.get_count()
            print("Добавлен id =", new_supplier.supplier_id)
            print("count:", before, "->", after)
            print(repo.get_by_id(new_supplier.supplier_id))
        except ValueError as e:
            print("ADD запрещён:", e)

    if MODE in ("demo", "full", "replace_only"):
        print("\nREPLACE:")
        supplier_id = 1
        existing = repo.get_by_id(supplier_id)
        if existing is None:
            print("Нечего заменять: supplier_id=1 не найден")
        else:
            try:
                existing.city = "Рязань"
                ok = repo.replace_by_id(supplier_id, existing)
                print("Заменено:", ok)
                print(repo.get_by_id(supplier_id))
            except ValueError as e:
                print("REPLACE запрещён:", e)

    if MODE in ("demo", "full", "delete_only"):
        print("\nDELETE:")
        supplier_id = 1
        before = repo.get_count()
        ok = repo.delete_by_id(supplier_id)
        after = repo.get_count()
        print("Удалено:", ok, "id=", supplier_id)
        print("count:", before, "->", after)

    print("\nИТОГ get_count:", repo.get_count())
    print("-" * 60)


# =========================
# ЗАПУСК
# =========================
json_repo = Supplier_rep_json("suppliers.json")
test_file_repository(json_repo, "JSON")

yaml_repo = Supplier_rep_yaml("suppliers.yaml")
test_file_repository(yaml_repo, "YAML")

db_repo = Supplier_rep_DB(
    dbname="suppliers_db",
    user="supplier_user",
    password="password123",
    host="localhost",
    port=5432
)
test_db_repository(db_repo, "PostgreSQL")
