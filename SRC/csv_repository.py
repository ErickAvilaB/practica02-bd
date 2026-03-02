import csv
from pathlib import Path

from errors import AppError


class CsvRepository:
    """Repositorio generico para persistir entidades en un archivo CSV.

    El repositorio trabaja con filas como diccionarios (columna -> valor).
    Esto facilita: agregar, listar, consultar por llave, actualizar y eliminar.

    Reglas:
    - Se garantiza que el archivo exista y contenga el encabezado esperado.
    - La llave primaria se asume como campo 'id' (configurable).
    - El repositorio NO interpreta tipos; eso lo hacen los modelos/servicios.
    """

    def __init__(self, file_path: Path, header: list[str], key_field: str = "id") -> None:
        self._file_path = file_path
        self._header = header
        self._key_field = key_field
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Crea el archivo con encabezado si no existe y valida encabezado si existe."""
        try:
            if not self._file_path.exists():
                self._file_path.write_text(",".join(self._header) + "\n", encoding="utf-8")
                return

            with self._file_path.open("r", encoding="utf-8", newline="") as file_handle:
                reader = csv.reader(file_handle)
                existing_header = next(reader, None)

            if existing_header is None:
                self._file_path.write_text(",".join(self._header) + "\n", encoding="utf-8")
                return

            if existing_header != self._header:
                raise AppError(
                    "El archivo CSV existe pero su encabezado no coincide con el esperado.\n"
                    f"Archivo: {self._file_path}\n"
                    f"Esperado: {self._header}\n"
                    f"Encontrado: {existing_header}"
                )
        except OSError as error:
            raise AppError(f"No se pudo preparar el archivo CSV: {self._file_path}. Detalle: {error}") from error

    def list_all(self) -> list[dict[str, str]]:
        """Regresa todas las filas del CSV como lista de diccionarios."""
        try:
            with self._file_path.open("r", encoding="utf-8", newline="") as file_handle:
                reader = csv.DictReader(file_handle)
                return [dict(row) for row in reader]
        except OSError as error:
            raise AppError(f"No se pudo leer el archivo CSV: {self._file_path}. Detalle: {error}") from error

    def get_by_key(self, key_value: str) -> dict[str, str] | None:
        """Busca una fila por valor de llave primaria y regresa la fila o None."""
        for row in self.list_all():
            if row.get(self._key_field) == key_value:
                return row
        return None

    def _write_all(self, rows: list[dict[str, str]]) -> None:
        """Sobrescribe el CSV con el encabezado esperado y las filas proporcionadas."""
        try:
            with self._file_path.open("w", encoding="utf-8", newline="") as file_handle:
                writer = csv.DictWriter(file_handle, fieldnames=self._header)
                writer.writeheader()
                for row in rows:
                    writer.writerow(self._normalize_row(row))
        except OSError as error:
            raise AppError(f"No se pudo escribir el archivo CSV: {self._file_path}. Detalle: {error}") from error

    def _normalize_row(self, row: dict[str, str]) -> dict[str, str]:
        """Asegura que la fila tenga exactamente las columnas del encabezado."""
        normalized: dict[str, str] = {}
        for column_name in self._header:
            normalized[column_name] = str(row.get(column_name, "") or "")
        return normalized

    def next_id(self) -> int:
        """Calcula el siguiente id numerico disponible (max(id)+1)."""
        max_id = 0
        for row in self.list_all():
            raw_value = (row.get(self._key_field) or "").strip()
            if raw_value.isdigit():
                max_id = max(max_id, int(raw_value))
        return max_id + 1

    def add(self, row: dict[str, str]) -> dict[str, str]:
        """Agrega una fila nueva al CSV. Si no trae id, se asigna automaticamente."""
        rows = self.list_all()
        if not row.get(self._key_field):
            row[self._key_field] = str(self.next_id())

        if self.get_by_key(str(row[self._key_field])) is not None:
            raise AppError(f"Ya existe un registro con id={row[self._key_field]}.")

        rows.append(self._normalize_row(row))
        self._write_all(rows)
        return row

    def update(self, key_value: str, updated_row: dict[str, str]) -> dict[str, str]:
        """Actualiza un registro por id. Lanza AppError si no existe."""
        rows = self.list_all()
        found = False

        for index, row in enumerate(rows):
            if row.get(self._key_field) == key_value:
                updated_row[self._key_field] = key_value  # la llave no se cambia
                rows[index] = self._normalize_row(updated_row)
                found = True
                break

        if not found:
            raise AppError(f"No se encontro un registro con id={key_value}.")

        self._write_all(rows)
        return updated_row

    def delete(self, key_value: str) -> None:
        """Elimina un registro por id. Lanza AppError si no existe."""
        rows = self.list_all()
        new_rows = [row for row in rows if row.get(self._key_field) != key_value]

        if len(new_rows) == len(rows):
            raise AppError(f"No se encontro un registro con id={key_value} para eliminar.")

        self._write_all(new_rows)

    def replace_with(self, rows: list[dict[str, str]]) -> None:
        """Reemplaza el contenido del archivo por la lista indicada (util para poblar datos)."""
        self._write_all(rows)
