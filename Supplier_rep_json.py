import json
from Supplier import Supplier


class Supplier_rep_json:
    """
    Репозиторий для работы с сущностью Supplier в JSON-файле
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    # a. Чтение всех значений из файла
    def read_all(self) -> list:
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

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
