class Cliente:
    """Modelo de un cliente/paciente.

    Guarda:
    - Nombre completo y datos de contacto
    - Fecha de nacimiento y domicilio
    - Metodo de pago
    - Visitas anuales (para descuento automatico)
    """

    def __init__(
        self,
        id_value: int,
        nombre: str,
        apellido_paterno: str,
        apellido_materno: str,
        telefonos: str,
        correos: str,
        fecha_nacimiento: str,
        calle: str,
        numero_interior: int | None,
        numero_exterior: int | None,
        colonia: str,
        estado: str,
        metodo_pago: str,
        visitas_anuales: int,
    ) -> None:
        self.id = id_value
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.telefonos = telefonos
        self.correos = correos
        self.fecha_nacimiento = fecha_nacimiento
        self.calle = calle
        self.numero_interior = numero_interior
        self.numero_exterior = numero_exterior
        self.colonia = colonia
        self.estado = estado
        self.metodo_pago = metodo_pago
        self.visitas_anuales = visitas_anuales

    def tasa_descuento(self) -> int:
        """Calcula el descuento porcentual basado en visitas anuales."""
        if self.visitas_anuales > 6:
            return 25
        if self.visitas_anuales >= 4:
            return 10
        if self.visitas_anuales >= 2:
            return 5
        return 0

    def to_row(self) -> dict[str, str]:
        """Convierte el objeto a una fila CSV."""
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "telefonos": self.telefonos,
            "correos": self.correos,
            "fecha_nacimiento": self.fecha_nacimiento,
            "calle": self.calle,
            "numero_interior": "" if self.numero_interior is None else str(self.numero_interior),
            "numero_exterior": "" if self.numero_exterior is None else str(self.numero_exterior),
            "colonia": self.colonia,
            "estado": self.estado,
            "metodo_pago": self.metodo_pago,
            "visitas_anuales": str(self.visitas_anuales),
        }

    @staticmethod
    def from_row(row: dict[str, str]) -> "Cliente":
        """Crea un Cliente a partir de una fila CSV."""
        def parse_int(value: str) -> int | None:
            value = (value or "").strip()
            return int(value) if value.isdigit() else None

        visitas_raw = (row.get("visitas_anuales") or "0").strip()
        visitas_anuales = int(visitas_raw) if visitas_raw.isdigit() else 0

        return Cliente(
            id_value=int((row.get("id") or "0").strip() or "0"),
            nombre=(row.get("nombre") or "").strip(),
            apellido_paterno=(row.get("apellido_paterno") or "").strip(),
            apellido_materno=(row.get("apellido_materno") or "").strip(),
            telefonos=(row.get("telefonos") or "").strip(),
            correos=(row.get("correos") or "").strip(),
            fecha_nacimiento=(row.get("fecha_nacimiento") or "").strip(),
            calle=(row.get("calle") or "").strip(),
            numero_interior=parse_int(row.get("numero_interior") or ""),
            numero_exterior=parse_int(row.get("numero_exterior") or ""),
            colonia=(row.get("colonia") or "").strip(),
            estado=(row.get("estado") or "").strip(),
            metodo_pago=(row.get("metodo_pago") or "").strip(),
            visitas_anuales=visitas_anuales,
        )
