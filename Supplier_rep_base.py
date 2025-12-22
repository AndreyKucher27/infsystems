from abc import ABC, abstractmethod
from Supplier import Supplier, SupplierShort


class Supplier_rep_base(ABC):
    """
    Базовый абстрактный репозиторий поставщиков
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    # --- Абстрактные методы (реализация в наследниках) ---

    @abstractmethod
    def read_all(self) -> list:
        pass

    @abstractmethod
    def write_all(self, suppliers: list) -> None:
        pass

    # --- Общая логика ---

    def get_by_id(self, supplier_id: int):
        for supplier in self.read_all():
            if supplier.supplier_id == supplier_id:
                return supplier
        return None

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

    def sort_by_city(self):
        return sorted(self.read_all(), key=lambda s: s.city)

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

    def replace_by_id(self, supplier_id: int, new_supplier: Supplier) -> bool:
        suppliers = self.read_all()

        for i, supplier in enumerate(suppliers):
            if supplier.supplier_id == supplier_id:
                new_supplier.supplier_id = supplier_id
                suppliers[i] = new_supplier
                self.write_all(suppliers)
                return True

        return False

    def delete_by_id(self, supplier_id: int) -> bool:
        suppliers = self.read_all()
        filtered = [s for s in suppliers if s.supplier_id != supplier_id]

        if len(filtered) == len(suppliers):
            return False

        self.write_all(filtered)
        return True

    def get_count(self) -> int:
        return len(self.read_all())
