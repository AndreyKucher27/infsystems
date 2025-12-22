import json
from Supplier import Supplier
from Supplier_rep_base import Supplier_rep_base


class Supplier_rep_json(Supplier_rep_base):
    def __init__(self, file_path: str):
        if not file_path.endswith(".json"):
            raise ValueError("Файл должен быть формата .json")
        super().__init__(file_path)

    def read_all(self) -> list:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        return [Supplier(item) for item in data]

    def write_all(self, suppliers: list) -> None:
        data = [supplier.to_dict() for supplier in suppliers]
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
