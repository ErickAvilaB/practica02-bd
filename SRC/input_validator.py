from datetime import datetime

from errors import AppError


class InputValidator:
    """Utilidades de captura y validacion de entradas por consola.

    Centraliza validaciones para:
    - Campos obligatorios y opcionales
    - Numeros enteros (campos numericos solo aceptan numeros)
    - Telefonos (solo digitos, aceptando espacios o guiones)
    - Fechas (formato ISO YYYY-MM-DD)
    - Booleanos (s/n)
    """

    def read_text(self, prompt: str, allow_empty: bool = False, default: str | None = None) -> str:
        """Lee texto desde consola y valida vacio segun se indique."""
        while True:
            user_input = input(prompt).strip()

            if not user_input and default is not None:
                return default

            if not user_input and not allow_empty:
                print("Entrada invalida: este campo es obligatorio.")
                continue

            return user_input

    def read_int(self, prompt: str, allow_empty: bool = False, default: int | None = None) -> int | None:
        """Lee un entero. Regresa None si allow_empty=True y el usuario deja vacio."""
        while True:
            raw_value = input(prompt).strip()

            if not raw_value:
                if default is not None:
                    return default
                if allow_empty:
                    return None
                print("Entrada invalida: se requiere un numero entero.")
                continue

            if not raw_value.isdigit():
                print("Entrada invalida: solo se aceptan numeros enteros (sin signos ni decimales).")
                continue

            return int(raw_value)

    def read_phone_list(self, prompt: str) -> str:
        """Lee una lista de telefonos.

        El usuario puede escribir:
        - Un telefono: 5512345678
        - Varios separados por coma: 5512345678, 5587654321

        Se guarda en CSV como una sola cadena separada por '|', por simplicidad.
        """
        while True:
            raw_value = input(prompt).strip()
            if not raw_value:
                print("Entrada invalida: se requiere al menos un telefono.")
                continue

            parts = [part.strip() for part in raw_value.split(",") if part.strip()]
            if not parts:
                print("Entrada invalida: se requiere al menos un telefono.")
                continue

            normalized_parts: list[str] = []
            for part in parts:
                cleaned = part.replace(" ", "").replace("-", "")
                if not cleaned.isdigit():
                    print("Entrada invalida: los telefonos deben contener solo digitos (puedes usar espacios o guiones).")
                    normalized_parts = []
                    break
                normalized_parts.append(cleaned)

            if not normalized_parts:
                continue

            return "|".join(normalized_parts)

    def read_email_list(self, prompt: str) -> str:
        """Lee correos y aplica una validacion ligera (presencia de '@')."""
        while True:
            raw_value = input(prompt).strip()
            if not raw_value:
                print("Entrada invalida: se requiere al menos un correo.")
                continue

            parts = [part.strip() for part in raw_value.split(",") if part.strip()]
            invalid = [email for email in parts if "@" not in email or email.startswith("@") or email.endswith("@")]
            if invalid:
                print("Entrada invalida: correos mal formados: " + ", ".join(invalid))
                continue

            return "|".join(parts)

    def read_date_iso(self, prompt: str, allow_empty: bool = False, default: str | None = None) -> str:
        """Lee una fecha en formato YYYY-MM-DD."""
        while True:
            raw_value = input(prompt).strip()

            if not raw_value:
                if default is not None:
                    return default
                if allow_empty:
                    return ""
                print("Entrada invalida: se requiere una fecha.")
                continue

            try:
                datetime.strptime(raw_value, "%Y-%m-%d")
                return raw_value
            except ValueError:
                print("Entrada invalida: usa el formato YYYY-MM-DD (ejemplo: 2001-03-15).")

    def read_bool(self, prompt: str, default: bool | None = None) -> bool:
        """Lee un booleano como 's'/'n'."""
        while True:
            raw_value = input(prompt).strip().lower()

            if not raw_value and default is not None:
                return default

            if raw_value in ("s", "si"):
                return True
            if raw_value in ("n", "no"):
                return False

            print("Entrada invalida: responde con 's' o 'n'.")

    def require_existing_id(self, raw_value: str) -> str:
        """Valida que un id exista y sea numerico (como llave)."""
        value = raw_value.strip()
        if not value:
            raise AppError("Debes proporcionar un id.")
        if not value.isdigit():
            raise AppError("El id debe ser un numero entero (solo digitos).")
        return value

    def require_money(self, raw_value: str, field_name: str) -> str:
        """Valida un valor monetario en formato decimal simple (ej. 12.50 o 12)."""
        value = raw_value.strip()
        if not value:
            raise AppError(f"Debes proporcionar {field_name}.")
        if not self._is_simple_decimal(value):
            raise AppError(f"{field_name} invalido: usa un numero (ej. 12 o 12.50).")
        return value

    def _is_simple_decimal(self, value: str) -> bool:
        if value.isdigit():
            return True
        if value.count(".") != 1:
            return False
        left, right = value.split(".", 1)
        return left.isdigit() and right.isdigit()
