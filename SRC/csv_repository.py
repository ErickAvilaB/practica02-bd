import csv
from pathlib import Path

from errors import AppError


class CsvRepository:
    """
    Repositorio genérico para persistir entidades en un archivo CSV.

    Características:
    ----------------
    - Trabaja con filas representadas como diccionarios (columna -> valor).
    - Garantiza que el archivo exista y que su encabezado sea el esperado.
    - Permite operaciones CRUD básicas:
        * Listar
        * Consultar por llave primaria
        * Agregar
        * Actualizar
        * Eliminar
    - No interpreta tipos de datos (todo se maneja como str).
      La conversión de tipos es responsabilidad del modelo o servicio.

    Suposiciones:
    -------------
    - La llave primaria por defecto es el campo "id".
    - El encabezado del archivo debe coincidir exactamente con el definido
      al crear el repositorio.
    """

    def __init__(self, file_path: Path, header: list[str], key_field: str = "id") -> None:
        """
        Inicializa el repositorio.

        Parámetros:
        -----------
        file_path : Path
            Ruta del archivo CSV.
        header : list[str]
            Lista de nombres de columnas esperadas.
        key_field : str
            Campo que se usará como llave primaria (por defecto "id").
        """
        self._file_path = file_path
        self._header = header
        self._key_field = key_field
        self._ensure_file()

    def _ensure_file(self) -> None:
        """
        Garantiza que el archivo exista y tenga el encabezado correcto.

        Casos:
        - Si el archivo no existe → se crea con el encabezado.
        - Si existe pero está vacío → se escribe el encabezado.
        - Si existe pero el encabezado no coincide → lanza AppError.
        """
        try:
            if not self._file_path.exists():
                self._file_path.write_text(
                    ",".join(self._header) + "\n",
                    encoding="utf-8"
                )
                return

            with self._file_path.open("r", encoding="utf-8", newline="") as file_handle:
                reader = csv.reader(file_handle)
                existing_header = next(reader, None)

            if existing_header is None:
                self._file_path.write_text(
                    ",".join(self._header) + "\n",
                    encoding="utf-8"
                )
                return

            if existing_header != self._header:
                raise AppError(
                    "El archivo CSV existe pero su encabezado no coincide con el esperado.\n"
                    f"Archivo: {self._file_path}\n"
                    f"Esperado: {self._header}\n"
                    f"Encontrado: {existing_header}"
                )

        except OSError as error:
            raise AppError(
                f"No se pudo preparar el archivo CSV: {self._file_path}. "
                f"Detalle: {error}"
            ) from error

    def list_all(self) -> list[dict[str, str]]:
        """
        Devuelve todas las filas del archivo CSV.

        Retorna:
        --------
        list[dict[str, str]]
            Lista de filas representadas como diccionarios.
        """
        try:
            with self._file_path.open("r", encoding="utf-8", newline="") as file_handle:
                reader = csv.DictReader(file_handle)
                return [dict(row) for row in reader]
        except OSError as error:
            raise AppError(
                f"No se pudo leer el archivo CSV: {self._file_path}. "
                f"Detalle: {error}"
            ) from error

    def get_by_key(self, key_value: str) -> dict[str, str] | None:
        """
        Busca un registro por su llave primaria.

        Parámetros:
        -----------
        key_value : str
            Valor de la llave primaria.

        Retorna:
        --------
        dict[str, str] | None
            La fila encontrada o None si no existe.
        """
        for row in self.list_all():
            if row.get(self._key_field) == key_value:
                return row
        return None

    def _write_all(self, rows: list[dict[str, str]]) -> None:
        """
        Sobrescribe completamente el archivo CSV.

        - Escribe primero el encabezado.
        - Luego escribe todas las filas normalizadas.
        """
        try:
            with self._file_path.open("w", encoding="utf-8", newline="") as file_handle:
                writer = csv.DictWriter(file_handle, fieldnames=self._header)
                writer.writeheader()
                for row in rows:
                    writer.writerow(self._normalize_row(row))
        except OSError as error:
            raise AppError(
                f"No se pudo escribir el archivo CSV: {self._file_path}. "
                f"Detalle: {error}"
            ) from error

    def _normalize_row(self, row: dict[str, str]) -> dict[str, str]:
        """
        Normaliza una fila para que coincida exactamente con el encabezado.

        - Garantiza que todas las columnas existan.
        - Convierte todos los valores a str.
        - Elimina columnas no definidas en el header.
        """
        normalized: dict[str, str] = {}
        for column_name in self._header:
            normalized[column_name] = str(row.get(column_name, "") or "")
        return normalized

    def next_id(self) -> int:
        """
        Calcula el siguiente id numérico disponible.

        Regla:
        ------
        max(id_existente) + 1

        Retorna:
        --------
        int
            Siguiente id disponible.
        """
        max_id = 0
        for row in self.list_all():
            raw_value = (row.get(self._key_field) or "").strip()
            if raw_value.isdigit():
                max_id = max(max_id, int(raw_value))
        return max_id + 1

    def add(self, row: dict[str, str]) -> dict[str, str]:
        """
        Agrega un nuevo registro al CSV.

        - Si no se proporciona id, se genera automáticamente.
        - Valida que no exista otro registro con el mismo id.
        """
        rows = self.list_all()

        if not row.get(self._key_field):
            row[self._key_field] = str(self.next_id())

        if self.get_by_key(str(row[self._key_field])) is not None:
            raise AppError(
                f"Ya existe un registro con id={row[self._key_field]}."
            )

        rows.append(self._normalize_row(row))
        self._write_all(rows)
        return row

    def update(self, key_value: str, updated_row: dict[str, str]) -> dict[str, str]:
        """
        Actualiza un registro existente por id.

        - La llave primaria no puede modificarse.
        - Lanza AppError si el registro no existe.
        """
        rows = self.list_all()
        found = False

        for index, row in enumerate(rows):
            if row.get(self._key_field) == key_value:
                updated_row[self._key_field] = key_value
                rows[index] = self._normalize_row(updated_row)
                found = True
                break

        if not found:
            raise AppError(
                f"No se encontro un registro con id={key_value}."
            )

        self._write_all(rows)
        return updated_row

    def delete(self, key_value: str) -> None:
        """
        Elimina un registro por id.

        Lanza:
        ------
        AppError si el registro no existe.
        """
        rows = self.list_all()
        new_rows = [
            row for row in rows
            if row.get(self._key_field) != key_value
        ]

        if len(new_rows) == len(rows):
            raise AppError(
                f"No se encontro un registro con id={key_value} para eliminar."
            )

        self._write_all(new_rows)

    def replace_with(self, rows: list[dict[str, str]]) -> None:
        """
        Reemplaza completamente el contenido del archivo.

        Útil para:
        - Poblar datos de prueba.
        - Restaurar información.
        """
        self._write_all(rows)
