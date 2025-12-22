import yaml
from Supplier import Supplier, SupplierShort


class Supplier_rep_yaml:
    """
    Репозиторий для работы с сущностью Supplier в YAML-файле
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    # a. Чтение всех значений из файла
    def read_all(self) -> list:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                if data is None:
                    data = []
        except FileNotFoundError:
            data = []

        return [Supplier(item) for item in data]

    # b. Запись всех значений в файл
    def write_all(self, suppliers: list) -> None:
        data = [supplier.to_dict() for supplier in suppliers]
        with open(self.file_path, "w", encoding="utf-8") as file:
            yaml.safe_dump(
                data,
                file,
                allow_unicode=True,
                sort_keys=False
            )

    # c. Получить объект по ID
    def get_by_id(self, supplier_id: int):
        for supplier in self.read_all():
            if supplier.supplier_id == supplier_id:
                return supplier
        return None

    # d. Пагинация — получить k объектов SupplierShort с n-й страницы
    def get_k_n_short_list(self, k: int, n: int):
        suppliers = self.read_all()

        short_list = [
            SupplierShort(
                supplier_id=s.supplier_id,
                name=s.name,
                phone=s.phone,
                email=s.email,
                inn=s.inn
            )
            for s in suppliers
        ]

        start = (n - 1) * k
        end = start + k
        return short_list[start:end]

    # e. Сортировка по городу
    def sort_by_city(self):
        suppliers = self.read_all()
        return sorted(suppliers, key=lambda s: s.city)

    # f. Добавить объект с автогенерацией ID
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
                new_supplier.supplier_id = supplier_id
                suppliers[i] = new_supplier
                self.write_all(suppliers)
                return True

        return False

    # h. Удалить элемент списка по ID
    def delete_by_id(self, supplier_id: int) -> bool:
        suppliers = self.read_all()
        filtered = [s for s in suppliers if s.supplier_id != supplier_id]

        if len(filtered) == len(suppliers):
            return False

        self.write_all(filtered)
        return True

    # i. Получить количество элементов
    def get_count(self) -> int:
        return len(self.read_all())
