import re
import psycopg2
from psycopg2.extras import RealDictCursor
from Supplier import Supplier, SupplierShort


class Supplier_rep_DB:
    """
    Репозиторий Supplier для PostgreSQL (без ORM, только SQL).

    Уникальность (по требованию пользователя):
    Нельзя добавлять/заменять, если совпадает ХОТЯ БЫ ОДНО поле из:
    name, phone, email, inn.

    Поля city/address/contact_name в проверке уникальности НЕ участвуют.
    """

    def __init__(self, dbname, user, password, host="localhost", port=5432):
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

    def _connect(self):
        return psycopg2.connect(**self.conn_params)

    # --- Нормализация (как в файловых репозиториях) ---
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

    def _check_uniqueness_or_raise(self, conn, candidate: Supplier, exclude_id: int | None = None) -> None:
        """
        Проверка уникальности в коде (без UNIQUE в SQL):
        если найден любой supplier, у которого совпадает name или phone или email или inn — ошибка.
        """
        cand_name = self._norm_text(candidate.name)
        cand_email = self._norm_text(getattr(candidate, "email", None))
        cand_phone = self._norm_phone(getattr(candidate, "phone", None))
        cand_inn = self._norm_inn(getattr(candidate, "inn", None))

        # Формируем WHERE динамически (чтобы не сравнивать NULL/пустые)
        conds = []
        params = []

        # name (без регистра)
        if cand_name is not None:
            conds.append("lower(trim(name)) = lower(trim(%s))")
            params.append(candidate.name)

        # inn
        if cand_inn is not None:
            conds.append("inn = %s")
            params.append(candidate.inn)

        # email (без регистра)
        if cand_email is not None:
            conds.append("lower(trim(email)) = lower(trim(%s))")
            params.append(candidate.email)

        # phone: сравнение по цифрам (чтобы +7 900... == 7900...)
        if cand_phone is not None:
            conds.append("regexp_replace(coalesce(phone,''), '\\D', '', 'g') = %s")
            params.append(cand_phone)

        if not conds:
            # Нечего проверять (в твоей модели это маловероятно)
            return

        where_or = " OR ".join(f"({c})" for c in conds)
        query = f"""
            SELECT supplier_id, name, phone, email, inn
            FROM suppliers
            WHERE ({where_or})
        """

        if exclude_id is not None:
            query += " AND supplier_id <> %s"
            params.append(exclude_id)

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()

        # Финальная проверка в Python (точно по нашим правилам)
        for r in rows:
            conflicts = []

            if cand_name is not None and self._norm_text(r.get("name")) == cand_name:
                conflicts.append("name")

            if cand_inn is not None and self._norm_inn(r.get("inn")) == cand_inn:
                conflicts.append("inn")

            r_email = self._norm_text(r.get("email"))
            if cand_email is not None and r_email is not None and r_email == cand_email:
                conflicts.append("email")

            r_phone = self._norm_phone(r.get("phone"))
            if cand_phone is not None and r_phone is not None and r_phone == cand_phone:
                conflicts.append("phone")

            if conflicts:
                raise ValueError(
                    f"Нарушение уникальности: поля {conflicts} уже существуют "
                    f"(конфликт с supplier_id={r['supplier_id']})."
                )

    @staticmethod
    def _row_to_supplier(row: dict) -> Supplier:
        return Supplier(
            supplier_id=row["supplier_id"],
            name=row["name"],
            contact_name=row["contact_name"],
            phone=row["phone"],
            email=row["email"],
            city=row["city"],
            address=row["address"],
            inn=row["inn"]
        )

    # a) Получить объект по ID
    def get_by_id(self, supplier_id: int):
        query = """
            SELECT supplier_id, name, contact_name, phone, email, city, address, inn
            FROM suppliers
            WHERE supplier_id = %s;
        """
        with self._connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (supplier_id,))
                row = cur.fetchone()

        if not row:
            return None
        return self._row_to_supplier(row)

    # b) Получить k объектов SupplierShort с n-й страницы
    def get_k_n_short_list(self, k: int, n: int):
        offset = (n - 1) * k
        query = """
            SELECT supplier_id, name, phone, email, inn
            FROM suppliers
            ORDER BY supplier_id
            LIMIT %s OFFSET %s;
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (k, offset))
                rows = cur.fetchall()

        return [
            SupplierShort(
                supplier_id=row[0],
                name=row[1],
                phone=row[2],
                email=row[3],
                inn=row[4]
            )
            for row in rows
        ]

    # c) Добавить объект (ID генерируется БД)
    def add_supplier(self, supplier: Supplier) -> Supplier:
        insert_query = """
            INSERT INTO suppliers (name, contact_name, phone, email, city, address, inn)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING supplier_id;
        """
        with self._connect() as conn:
            # Проверка уникальности перед INSERT
            self._check_uniqueness_or_raise(conn, supplier, exclude_id=None)

            with conn.cursor() as cur:
                cur.execute(insert_query, (
                    supplier.name,
                    supplier.contact_name,
                    supplier.phone,
                    supplier.email,
                    supplier.city,
                    supplier.address,
                    supplier.inn
                ))
                new_id = cur.fetchone()[0]

        supplier.supplier_id = new_id
        return supplier

    # d) Заменить элемент по ID
    def replace_by_id(self, supplier_id: int, new_supplier: Supplier) -> bool:
        update_query = """
            UPDATE suppliers
            SET name=%s,
                contact_name=%s,
                phone=%s,
                email=%s,
                city=%s,
                address=%s,
                inn=%s
            WHERE supplier_id=%s;
        """
        with self._connect() as conn:
            # Проверка уникальности перед UPDATE, исключая саму запись
            self._check_uniqueness_or_raise(conn, new_supplier, exclude_id=supplier_id)

            with conn.cursor() as cur:
                cur.execute(update_query, (
                    new_supplier.name,
                    new_supplier.contact_name,
                    new_supplier.phone,
                    new_supplier.email,
                    new_supplier.city,
                    new_supplier.address,
                    new_supplier.inn,
                    supplier_id
                ))
                updated = cur.rowcount

        return updated > 0

    # e) Удалить элемент по ID
    def delete_by_id(self, supplier_id: int) -> bool:
        query = "DELETE FROM suppliers WHERE supplier_id=%s;"
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (supplier_id,))
                deleted = cur.rowcount
        return deleted > 0

    # f) Получить количество элементов
    def get_count(self) -> int:
        query = "SELECT COUNT(*) FROM suppliers;"
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchone()[0]
