import yaml
from Supplier import Supplier
from Supplier_rep_base import Supplier_rep_base


class Supplier_rep_yaml(Supplier_rep_base):
    def __init__(self, file_path: str):
        if not (file_path.endswith(".yaml") or file_path.endswith(".yml")):
            raise ValueError("Файл должен быть формата .yaml или .yml")
        super().__init__(file_path)

    def read_all(self) -> list:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                if data is None:
                    data = []
        except FileNotFoundError:
            data = []

        return [Supplier(item) for item in data]

    def write_all(self, suppliers: list) -> None:
        data = [supplier.to_dict() for supplier in suppliers]
        with open(self.file_path, "w", encoding="utf-8") as file:
            yaml.safe_dump(
                data,
                file,
                allow_unicode=True,
                sort_keys=False
            )
