import json
from Supplier import Supplier, SupplierShort


class Supplier_rep_json:
    """
    Репозиторий для работы с сущностью Supplier в JSON-файле
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    # a. Чтение всех значений из файла
    def read_all(self) -> list:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        return [Supplier(item) for item in data]

    # b. Запись всех значений в файл
    def write_all(self, suppliers: list) -> None:
        data = [supplier.to_dict() for supplier in suppliers]
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    # c. Получить объект по ID
    def get_by_id(self, supplier_id: int):
        for supplier in self.read_all():
            if supplier.supplier_id == supplier_id:
                return supplier
        return None

    # d. Пагинация — получить k объектов SupplierShort с n-й страницы
    def get_k_n_short_list(self, k: int, n: int):
        all_suppliers = self.read_all()
        #Явное создание объектов SupplierShort (лишние поля отбрасываются, нужное копируется и остается)
        #SupplierShort может быть создан из Supplier, потому что у Supplier есть все нужные данные
        short_list = [
            SupplierShort(
                supplier_id=s.supplier_id,
                name=s.name,
                phone=s.phone,
                email=s.email,
                inn=s.inn
            )
            for s in all_suppliers
        ]

        start_index = (n - 1) * k
        end_index = start_index + k

        return short_list[start_index:end_index]

    # e. Сортировка поставщиков по городу
    def sort_by_city(self):
        suppliers = self.read_all()
        return sorted(suppliers, key=lambda s: s.city)

    # f. Добавление нового поставщика с автогенерацией ID
    def add_supplier(self, supplier: Supplier):
        suppliers = self.read_all()

        existing_ids = [
            s.supplier_id for s in suppliers
            if isinstance(s.supplier_id, int)
        ]

        new_id = max(existing_ids) + 1 if existing_ids else 1

        supplier.supplier_id = new_id
        suppliers.append(supplier)

        self.write_all(suppliers)
        return supplier

    # g. Заменить элемент списка по ID
    def replace_by_id(self, supplier_id: int, new_supplier: Supplier) -> bool:
        suppliers = self.read_all()

        for i, supplier in enumerate(suppliers):
            if supplier.supplier_id == supplier_id:
                # сохраняем старый ID
                new_supplier.supplier_id = supplier_id
                suppliers[i] = new_supplier
                self.write_all(suppliers)
                return True

        return False

    # h. Удалить элемент списка по ID
    def delete_by_id(self, supplier_id: int) -> bool:
        suppliers = self.read_all()
        new_suppliers = [s for s in suppliers if s.supplier_id != supplier_id]

        if len(new_suppliers) == len(suppliers):
            return False  # ничего не удалено

        self.write_all(new_suppliers)
        return True

    # i. Получить количество элементов
    def get_count(self) -> int:
        return len(self.read_all())



