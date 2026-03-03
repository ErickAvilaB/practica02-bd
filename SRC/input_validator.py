from datetime import datetime

from errors import AppError


class InputValidator:
    """
    Clase utilitaria para la captura y validación de entradas por consola.

    Centraliza todas las validaciones relacionadas con datos ingresados
    por el usuario en aplicaciones CLI (Command Line Interface).

    Funcionalidades principales:
    - Validación de campos obligatorios y opcionales.
    - Lectura y validación de números enteros positivos.
    - Validación de listas de teléfonos.
    - Validación básica de correos electrónicos.
    - Validación de fechas en formato ISO (YYYY-MM-DD).
    - Lectura de valores booleanos (s/n).
    - Validación de identificadores numéricos.
    - Validación de valores monetarios decimales simples.
    """

    def read_text(self, prompt: str, allow_empty: bool = False, default: str | None = None) -> str:
        """
        Lee texto desde consola y valida si puede estar vacío.

        Args:
            prompt (str): Mensaje mostrado al usuario.
            allow_empty (bool): Indica si se permite una cadena vacía.
            default (str | None): Valor por defecto si el usuario no ingresa nada.

        Returns:
            str: Texto ingresado por el usuario o el valor por defecto.

        Comportamiento:
            - Si el usuario no ingresa nada y existe un valor por defecto,
              se retorna el valor por defecto.
            - Si no se permite vacío y el usuario no ingresa texto,
              se solicita nuevamente la entrada.
        """
        while True:
            user_input = input(prompt).strip()

            if not user_input and default is not None:
                return default

            if not user_input and not allow_empty:
                print("Entrada invalida: este campo es obligatorio.")
                continue

            return user_input

    def read_int(self, prompt: str, allow_empty: bool = False, default: int | None = None) -> int | None:
        """
        Lee un número entero positivo desde consola.

        Args:
            prompt (str): Mensaje mostrado al usuario.
            allow_empty (bool): Permite retornar None si la entrada está vacía.
            default (int | None): Valor por defecto si no se ingresa nada.

        Returns:
            int | None:
                - Entero convertido si la entrada es válida.
                - None si allow_empty=True y el usuario deja vacío.
                - default si está definido y la entrada es vacía.

        Restricciones:
            - Solo acepta dígitos (sin signos ni decimales).
        """
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
        """
        Lee una lista de teléfonos separados por coma.

        Formato permitido:
            - Un teléfono: 5512345678
            - Varios teléfonos: 5512345678, 5587654321
            - Se permiten espacios o guiones (serán eliminados).

        Args:
            prompt (str): Mensaje mostrado al usuario.

        Returns:
            str: Teléfonos normalizados y separados por '|'.

        Ejemplo:
            Entrada: "5512-345678, 55 8765 4321"
            Salida:  "5512345678|5587654321"
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
        """
        Lee una lista de correos electrónicos separados por coma.

        Validación aplicada:
            - Debe contener '@'.
            - No puede iniciar ni terminar con '@'.

        Args:
            prompt (str): Mensaje mostrado al usuario.

        Returns:
            str: Correos válidos separados por '|'.

        Nota:
            La validación es básica y no cumple completamente
            con el estándar RFC de correos electrónicos.
        """
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
        """
        Lee y valida una fecha en formato ISO (YYYY-MM-DD).

        Args:
            prompt (str): Mensaje mostrado al usuario.
            allow_empty (bool): Permite retornar cadena vacía.
            default (str | None): Valor por defecto si no se ingresa nada.

        Returns:
            str: Fecha válida en formato YYYY-MM-DD.

        Validación:
            - Usa datetime.strptime para verificar formato y fecha real.
        """
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
        """
        Lee un valor booleano desde consola usando 's'/'n'.

        Args:
            prompt (str): Mensaje mostrado al usuario.
            default (bool | None): Valor por defecto si no se ingresa nada.

        Returns:
            bool:
                True si el usuario responde 's' o 'si'.
                False si responde 'n' o 'no'.
        """
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
        """
        Valida que un identificador exista y sea numérico.

        Args:
            raw_value (str): Valor ingresado.

        Returns:
            str: ID validado (solo dígitos).

        Raises:
            AppError: Si el valor está vacío o no es numérico.
        """
        value = raw_value.strip()
        if not value:
            raise AppError("Debes proporcionar un id.")
        if not value.isdigit():
            raise AppError("El id debe ser un numero entero (solo digitos).")
        return value

    def require_money(self, raw_value: str, field_name: str) -> str:
        """
        Valida un valor monetario en formato decimal simple.

        Formatos válidos:
            - 12
            - 12.50

        Args:
            raw_value (str): Valor ingresado.
            field_name (str): Nombre del campo (para mensajes de error).

        Returns:
            str: Valor validado.

        Raises:
            AppError: Si el valor está vacío o tiene formato inválido.
        """
        value = raw_value.strip()
        if not value:
            raise AppError(f"Debes proporcionar {field_name}.")
        if not self._is_simple_decimal(value):
            raise AppError(f"{field_name} invalido: usa un numero (ej. 12 o 12.50).")
        return value

    def _is_simple_decimal(self, value: str) -> bool:
        """
        Verifica si una cadena representa un decimal positivo simple.

        Reglas:
            - Solo dígitos (entero).
            - O formato con un solo punto decimal (ej. 12.50).
            - No permite signos negativos ni múltiples puntos.

        Args:
            value (str): Cadena a validar.

        Returns:
            bool: True si cumple el formato, False en caso contrario.
        """
        if value.isdigit():
            return True
        if value.count(".") != 1:
            return False
        left, right = value.split(".", 1)
        return left.isdigit() and right.isdigit()
