class Cliente:
    """
    Modelo de dominio que representa a un cliente/paciente del sistema.

    Esta clase encapsula:
    - Información personal (nombre completo).
    - Datos de contacto (teléfonos y correos).
    - Fecha de nacimiento.
    - Domicilio.
    - Método de pago preferido.
    - Número de visitas anuales (base para cálculo de descuento).

    Importante:
    ----------
    Esta clase pertenece a la capa de dominio.
    No realiza operaciones de entrada/salida ni interactúa directamente
    con archivos. La persistencia se maneja a través del repositorio.
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
        """
        Inicializa una instancia de Cliente.

        Parámetros:
        -----------
        id_value : int
            Identificador único del cliente.
        nombre : str
            Nombre del cliente.
        apellido_paterno : str
            Apellido paterno.
        apellido_materno : str
            Apellido materno.
        telefonos : str
            Lista de teléfonos almacenados como cadena separada por "|".
        correos : str
            Lista de correos almacenados como cadena separada por "|".
        fecha_nacimiento : str
            Fecha en formato ISO (YYYY-MM-DD).
        calle : str
            Calle del domicilio.
        numero_interior : int | None
            Número interior (puede ser None si no aplica).
        numero_exterior : int | None
            Número exterior (puede ser None si no aplica).
        colonia : str
            Colonia del domicilio.
        estado : str
            Estado del domicilio.
        metodo_pago : str
            Método de pago preferido (EFECTIVO o TARJETA).
        visitas_anuales : int
            Número de visitas realizadas en un año.
        """

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
        """
        Calcula el porcentaje de descuento aplicable
        según el número de visitas anuales.

        Reglas de negocio:
        ------------------
        - Más de 6 visitas → 25%
        - Entre 4 y 6 visitas → 10%
        - Entre 2 y 3 visitas → 5%
        - Menos de 2 visitas → 0%

        Regresa:
        --------
        int
            Porcentaje de descuento aplicable.
        """
        if self.visitas_anuales > 6:
            return 25
        if self.visitas_anuales >= 4:
            return 10
        if self.visitas_anuales >= 2:
            return 5
        return 0

    def to_row(self) -> dict[str, str]:
        """
        Convierte la instancia Cliente en un diccionario
        compatible con una fila CSV.

        Todas las claves y valores se transforman en str,
        ya que el formato CSV almacena datos como texto.

        Retorna:
        --------
        dict[str, str]
            Representación serializable del cliente.
        """
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
        """
        Crea una instancia de Cliente a partir de una fila CSV.

        Convierte automáticamente:
        - id → int
        - numero_interior y numero_exterior → int | None
        - visitas_anuales → int (default 0 si es inválido)

        Parámetros:
        -----------
        row : dict[str, str]
            Diccionario proveniente del repositorio CSV.

        Retorna:
        --------
        Cliente
            Instancia completamente construida.
        """

        def parse_int(value: str) -> int | None:
            """
            Convierte una cadena a entero si es numérica.
            Retorna None si está vacía o no es válida.
            """
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
