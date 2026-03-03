class Sucursal:
    """
    Modelo de dominio que representa una sucursal del sistema.

    Una sucursal puede:
    - Operar únicamente como punto de venta.
    - Tener integrada una clínica con información adicional.

    Contiene dos grupos de datos:

    1) Datos generales:
       - Identificador único
       - Nombre
       - Dirección (calle, números, colonia, estado)
       - Teléfono
       - Horario de atención

    2) Datos opcionales de clínica:
       - Indicador de si existe clínica
       - Nombre de la clínica
       - Número de cuartos
       - Número de empleados
       - Horario de atención de la clínica

    Este modelo es una entidad de dominio y es independiente
    del mecanismo de persistencia.
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
        """
        Inicializa una nueva instancia de Sucursal.

        :param id_value: Identificador único de la sucursal.
        :param nombre: Nombre comercial de la sucursal.
        :param calle: Calle del domicilio.
        :param numero_interior: Número interior (opcional).
        :param numero_exterior: Número exterior (opcional).
        :param colonia: Colonia o barrio.
        :param estado: Estado o entidad federativa.
        :param telefono: Número telefónico de contacto.
        :param horario_atencion: Horario general de atención.
        :param tiene_clinica: Indica si la sucursal cuenta con clínica integrada.
        :param nombre_clinica: Nombre de la clínica (si aplica).
        :param clinica_numero_cuartos: Número de cuartos disponibles en la clínica.
        :param clinica_numero_empleados: Número de empleados de la clínica.
        :param clinica_horario_atencion: Horario de atención específico de la clínica.
        """
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
        """
        Convierte la instancia de Sucursal a un diccionario
        listo para ser almacenado en un archivo CSV.

        Reglas de conversión:
        - Los valores numéricos se convierten a cadena.
        - Los valores None se representan como cadena vacía.
        - El booleano 'tiene_clinica' se almacena como:
            "1" -> True
            "0" -> False

        :return: Diccionario con claves tipo string y valores tipo string.
        """
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
        """
        Crea una instancia de Sucursal a partir de un diccionario
        proveniente de una fila de un archivo CSV.

        Reglas de conversión:
        - Cadenas vacías se convierten a None en campos numéricos.
        - El valor "1" en 'tiene_clinica' se interpreta como True.
        - Cualquier otro valor se interpreta como False.
        - Los textos se normalizan eliminando espacios laterales.

        :param row: Diccionario con los datos leídos del CSV.
        :return: Instancia de Sucursal.
        """

        def parse_int(value: str) -> int | None:
            """
            Convierte una cadena a entero si contiene únicamente dígitos.
            En caso contrario, devuelve None.

            :param value: Cadena a convertir.
            :return: Entero o None.
            """
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
