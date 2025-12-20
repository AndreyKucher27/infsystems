import json

class SupplierShort:

    possible_keys = ('supplier_id', 'name', 'phone', 'email', 'inn')

    @classmethod
    def _parse_init_input(cls, args, kwargs, possible_keys=None, type_name=None):
        """
        Универсальный парсер входных параметров
        """
        if possible_keys is None:
            possible_keys = cls.possible_keys
        if type_name is None:
            type_name = cls.__name__

        data = {}
        for k in possible_keys:
            if k in kwargs:
                data[k] = kwargs[k]

        if args:
            if len(args) == 1:
                single = args[0]
                if isinstance(single, str):
                    s = single.strip()
                    parsed = None
                    if (s.startswith('{') and s.endswith('}')) or ('"' in s and ':' in s):
                        try:
                            parsed = json.loads(s)
                        except (json.JSONDecodeError, TypeError):
                            parsed = None
                    if isinstance(parsed, dict):
                        for k in possible_keys:
                            if k in parsed and k not in data:
                                data[k] = parsed[k]
                    else:
                        parts = s.split(';')
                        if len(parts) == len(possible_keys):
                            parsed_map = dict(zip(possible_keys, parts))
                            for k in possible_keys:
                                if k not in data:
                                    data[k] = parsed_map[k]
                        else:
                            raise ValueError(f"Ожидалась строка в формате JSON или {len(possible_keys)} элементов для {type_name}")
                elif isinstance(single, dict):
                    for k in possible_keys:
                        if k in single and k not in data:
                            data[k] = single[k]
                else:
                    raise ValueError("Неподдерживаемый тип единственного позиционного аргумента")
            elif len(args) == len(possible_keys):
                seq = dict(zip(possible_keys, args))
                for k in possible_keys:
                    if k not in data:
                        data[k] = seq[k]
            else:
                raise ValueError("Неподдерживаемая комбинация позиционных аргументов для " + type_name)

        return data

    def __init__(self, *args, **kwargs):
        data = self._parse_init_input(args, kwargs, possible_keys=self.possible_keys, type_name=self.__class__.__name__)

        missing = [k for k in SupplierShort.possible_keys if k not in data]
        if missing:
            raise ValueError(f"Не хватает данных для инициализации {SupplierShort.__name__}: отсутствуют {missing}")

        if isinstance(data['supplier_id'], str) and data['supplier_id'].strip().isdigit():
            data['supplier_id'] = int(data['supplier_id'].strip())

        self.supplier_id = data['supplier_id']
        self.name = data['name']
        self.phone = data['phone']
        self.email = data['email']
        self.inn = data['inn']

    def _set_field(self, field_name, value, validator, error_message):
        if not validator(value):
            raise ValueError(f"{error_message} (значение: {repr(value)})")
        setattr(self, field_name, value)

    @property
    def supplier_id(self): return self._supplier_id
    @supplier_id.setter
    def supplier_id(self, value):
        self._set_field('_supplier_id', value, self.validate_supplier_id,
                        "ID должен быть положительным целым числом.")

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value):
        self._set_field('_name', value, self.validate_name, "Название поставщика некорректно.")

    @property
    def phone(self): return self._phone
    @phone.setter
    def phone(self, value):
        self._set_field('_phone', value, self.validate_phone, "Неверный формат телефона.")

    @property
    def email(self): return self._email
    @email.setter
    def email(self, value):
        self._set_field('_email', value, self.validate_email, "Некорректный email.")

    @property
    def inn(self): return self._inn
    @inn.setter
    def inn(self, value):
        self._set_field('_inn', value, self.validate_inn,
                        "Некорректный ИНН (проверьте длину и контрольную цифру).")

    @staticmethod
    def validate_supplier_id(value): return isinstance(value, int) and value > 0

    @staticmethod
    def validate_name(value):
        if not isinstance(value, str): return False
        value = value.strip()
        if len(value) < 2: return False
        return any(ch.isalpha() for ch in value)

    @staticmethod
    def validate_phone(value):
        if not isinstance(value, str): return False
        value = value.strip()
        if len([ch for ch in value if ch.isdigit()]) < 10: return False
        allowed = set("0123456789 +-()")
        if any(ch not in allowed for ch in value): return False
        return value[0].isdigit() or value.startswith("+")

    @staticmethod
    def validate_email(value):
        if not isinstance(value, str): return False
        value = value.strip()
        if value.count("@") != 1: return False
        local, domain = value.split("@")
        if not local or not domain: return False
        if "." not in domain: return False
        if domain.startswith(".") or domain.endswith("."): return False
        if " " in value: return False
        return True

    @staticmethod
    def validate_inn(value):
        if not isinstance(value, str): return False
        value = value.strip()
        if not value.isdigit(): return False
        if len(value) not in (10, 12): return False

        def calc(ctrl_nums, digits):
            return sum(int(digits[i]) * ctrl_nums[i] for i in range(len(ctrl_nums))) % 11 % 10

        if len(value) == 10:
            return calc([2, 4, 10, 3, 5, 9, 4, 6, 8], value) == int(value[-1])
        if len(value) == 12:
            n11 = calc([7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0], value)
            n12 = calc([3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8], value)
            return n11 == int(value[10]) and n12 == int(value[11])
        return False

    def __str__(self):
        return f"{self.name} — тел: {self.phone}, email: {self.email}, ИНН: {self.inn}"

    def __repr__(self):
        return (f"SupplierShort(supplier_id={self._supplier_id}, name='{self._name}', "
                f"phone='{self._phone}', email='{self._email}', inn='{self._inn}')")


class Supplier(SupplierShort):

    possible_keys = ('supplier_id', 'name', 'contact_name', 'phone', 'email', 'city', 'address', 'inn')

    def __init__(self, *args, **kwargs):
        data = self._parse_init_input(args, kwargs, possible_keys=self.possible_keys, type_name=self.__class__.__name__)

        missing = [k for k in self.possible_keys if k not in data]
        if missing:
            raise ValueError(f"Не хватает данных для инициализации {self.__class__.__name__}: отсутствуют {missing}")

        super().__init__(**{k: data[k] for k in SupplierShort.possible_keys})

        self.contact_name = data['contact_name']
        self.city = data['city']
        self.address = data['address']

    @property
    def contact_name(self): return self._contact_name
    @contact_name.setter
    def contact_name(self, value):
        self._set_field('_contact_name', value, self.validate_contact_name,
                        "Некорректное имя контактного лица.")

    @property
    def city(self): return self._city
    @city.setter
    def city(self, value):
        self._set_field('_city', value, self.validate_city, "Некорректное название города.")

    @property
    def address(self): return self._address
    @address.setter
    def address(self, value):
        self._set_field('_address', value, self.validate_address, "Некорректный адрес.")

    @staticmethod
    def validate_contact_name(value):
        if not isinstance(value, str): return False
        value = value.strip()
        if len(value) < 2: return False
        return any(ch.isalpha() for ch in value)

    @staticmethod
    def validate_city(value):
        if not isinstance(value, str): return False
        value = value.strip()
        if len(value) < 2: return False
        return all(ch.isalpha() or ch in " -" for ch in value)

    @staticmethod
    def validate_address(value):
        if not isinstance(value, str): return False
        value = value.strip()
        return len(value) >= 5 and any(ch.isdigit() for ch in value)

    def __str__(self):
        return (f"{self.name} ({self.contact_name}) — тел: {self.phone}, email: {self.email}\n"
                f"Город: {self.city}, Адрес: {self.address}, ИНН: {self.inn}")

    def __repr__(self):
        return (f"Supplier(supplier_id={self._supplier_id}, name='{self._name}', "
                f"contact_name='{self._contact_name}', phone='{self._phone}', "
                f"email='{self._email}', city='{self._city}', address='{self._address}', "
                f"inn='{self._inn}')")

    def to_dict(self):
        """
        Преобразует объект Supplier в словарь для записи в JSON
        """
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_name": self.contact_name,
            "phone": self.phone,
            "email": self.email,
            "city": self.city,
            "address": self.address,
            "inn": self.inn
        }
