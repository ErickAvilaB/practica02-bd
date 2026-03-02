class Sucursal:
    """Modelo de una sucursal.

    Guarda:
    - Datos generales: nombre, direccion, telefono, horario
    - Datos opcionales de clinica integrada
    """

    def __init__(
        self,
        id_value: int,
        nombre: str,
        calle: str,
        numero_interior: int | None,
        numero_exterior: int | None,
        colonia: str,
        estado: str,
        telefono: str,
        horario_atencion: str,
        tiene_clinica: bool,
        nombre_clinica: str,
        clinica_numero_cuartos: int | None,
        clinica_numero_empleados: int | None,
        clinica_horario_atencion: str,
    ) -> None:
        self.id = id_value
        self.nombre = nombre
        self.calle = calle
        self.numero_interior = numero_interior
        self.numero_exterior = numero_exterior
        self.colonia = colonia
        self.estado = estado
        self.telefono = telefono
        self.horario_atencion = horario_atencion
        self.tiene_clinica = tiene_clinica
        self.nombre_clinica = nombre_clinica
        self.clinica_numero_cuartos = clinica_numero_cuartos
        self.clinica_numero_empleados = clinica_numero_empleados
        self.clinica_horario_atencion = clinica_horario_atencion

    def to_row(self) -> dict[str, str]:
        """Convierte el objeto a una fila para CSV."""
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "calle": self.calle,
            "numero_interior": "" if self.numero_interior is None else str(self.numero_interior),
            "numero_exterior": "" if self.numero_exterior is None else str(self.numero_exterior),
            "colonia": self.colonia,
            "estado": self.estado,
            "telefono": self.telefono,
            "horario_atencion": self.horario_atencion,
            "tiene_clinica": "1" if self.tiene_clinica else "0",
            "nombre_clinica": self.nombre_clinica,
            "clinica_numero_cuartos": "" if self.clinica_numero_cuartos is None else str(self.clinica_numero_cuartos),
            "clinica_numero_empleados": "" if self.clinica_numero_empleados is None else str(self.clinica_numero_empleados),
            "clinica_horario_atencion": self.clinica_horario_atencion,
        }

    @staticmethod
    def from_row(row: dict[str, str]) -> "Sucursal":
        """Crea una Sucursal a partir de una fila CSV."""
        def parse_int(value: str) -> int | None:
            value = (value or "").strip()
            return int(value) if value.isdigit() else None

        return Sucursal(
            id_value=int((row.get("id") or "0").strip() or "0"),
            nombre=(row.get("nombre") or "").strip(),
            calle=(row.get("calle") or "").strip(),
            numero_interior=parse_int(row.get("numero_interior") or ""),
            numero_exterior=parse_int(row.get("numero_exterior") or ""),
            colonia=(row.get("colonia") or "").strip(),
            estado=(row.get("estado") or "").strip(),
            telefono=(row.get("telefono") or "").strip(),
            horario_atencion=(row.get("horario_atencion") or "").strip(),
            tiene_clinica=((row.get("tiene_clinica") or "0").strip() == "1"),
            nombre_clinica=(row.get("nombre_clinica") or "").strip(),
            clinica_numero_cuartos=parse_int(row.get("clinica_numero_cuartos") or ""),
            clinica_numero_empleados=parse_int(row.get("clinica_numero_empleados") or ""),
            clinica_horario_atencion=(row.get("clinica_horario_atencion") or "").strip(),
        )
