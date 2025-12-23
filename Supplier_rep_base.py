from abc import ABC, abstractmethod
import re
from Supplier import Supplier, SupplierShort


class Supplier_rep_base(ABC):
    """
    Базовый абстрактный репозиторий поставщиков (для файловых хранилищ).

    Уникальность:
    Нельзя добавлять/заменять поставщика, если совпадает ХОТЯ БЫ ОДНО поле из:
    name, phone, email, inn.

    Поля city/address/contact_name в проверке уникальности НЕ участвуют.
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

    # --- Нормализация для корректного сравнения ---
    @staticmethod
    def _norm_text(value):
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        value = value.strip()
        return value.casefold() if value else None

    @staticmethod
    def _norm_inn(value):
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        value = value.strip()
        return value if value else None

    @staticmethod
    def _norm_phone(value):
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        digits = re.sub(r"\D", "", value)
        return digits if digits else None

    def _check_uniqueness_or_raise(self, suppliers: list, candidate: Supplier, exclude_id: int | None = None) -> None:
        """
        Проверяет уникальность по правилу:
        если совпадает хотя бы одно поле name/phone/email/inn с любой другой записью — ошибка.

        exclude_id используется для replace: не сравниваем запись сама с собой.
        """
        cand_name = self._norm_text(getattr(candidate, "name", None))
        cand_email = self._norm_text(getattr(candidate, "email", None))
        cand_phone = self._norm_phone(getattr(candidate, "phone", None))
        cand_inn = self._norm_inn(getattr(candidate, "inn", None))

        for s in suppliers:
            if exclude_id is not None and s.supplier_id == exclude_id:
                continue

            conflicts = []

            # name
            if cand_name is not None and self._norm_text(getattr(s, "name", None)) == cand_name:
                conflicts.append("name")

            # inn
            if cand_inn is not None and self._norm_inn(getattr(s, "inn", None)) == cand_inn:
                conflicts.append("inn")

            # email (проверяем только если email задан у кандидата и у существующей записи)
            s_email = self._norm_text(getattr(s, "email", None))
            if cand_email is not None and s_email is not None and s_email == cand_email:
                conflicts.append("email")

            # phone (проверяем только если phone задан у кандидата и у существующей записи)
            s_phone = self._norm_phone(getattr(s, "phone", None))
            if cand_phone is not None and s_phone is not None and s_phone == cand_phone:
                conflicts.append("phone")

            if conflicts:
                raise ValueError(
                    f"Нарушение уникальности: поля {conflicts} уже существуют "
                    f"(конфликт с supplier_id={s.supplier_id})."
                )

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

        # Уникальность ДО генерации ID и добавления
        self._check_uniqueness_or_raise(suppliers, supplier, exclude_id=None)

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

        # Проверяем уникальность, исключая текущий supplier_id
        self._check_uniqueness_or_raise(suppliers, new_supplier, exclude_id=supplier_id)

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
