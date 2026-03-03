from csv_repository import CsvRepository
from errors import AppError
from input_validator import InputValidator
from cliente import Cliente


class ClienteService:
    """
    Servicio de aplicación que implementa los casos de uso (CRUD)
    para la entidad Cliente.

    Responsabilidades:
    -------------------
    - Coordinar la interacción entre consola (entrada/salida),
      validaciones y repositorio CSV.
    - Transformar filas (dict) en objetos Cliente y viceversa.
    - Aplicar reglas de negocio básicas (ej. descuento por visitas).
    - Manejar errores de dominio mediante AppError.

    Este servicio NO accede directamente a archivos;
    delega la persistencia al CsvRepository.
    """

    def __init__(self, repository: CsvRepository, validator: InputValidator) -> None:
        """
        Inicializa el servicio de clientes.

        Parámetros:
        -----------
        repository : CsvRepository
            Repositorio encargado de la persistencia en CSV.
        validator : InputValidator
            Componente encargado de validar entradas del usuario.
        """
        self._repository = repository
        self._validator = validator

    def list_brief(self) -> None:
        """
        Lista todos los clientes mostrando únicamente:
        - id
        - nombre completo

        Si no existen registros, informa al usuario.
        """
        rows = self._repository.list_all()
        if not rows:
            print("No hay clientes registrados.")
            return

        print("\nClientes registrados:")
        for row in rows:
            full_name = " ".join(
                [
                    row.get("nombre") or "",
                    row.get("apellido_paterno") or "",
                    row.get("apellido_materno") or "",
                ]
            ).strip()
            print(f"  [{row.get('id')}] {full_name}")

    def consult_by_id(self) -> None:
        """
        Consulta un cliente por su id.

        - Solicita el id al usuario.
        - Valida que exista.
        - Muestra todos sus datos.
        - Incluye el descuento calculado a partir de visitas_anuales.
        """
        key_value = self._validator.require_existing_id(
            input("Ingresa el id del cliente: ")
        )

        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un cliente con id={key_value}.")

        cliente = Cliente.from_row(row)
        self._print_full(cliente)

    def create_interactive(self) -> None:
        """
        Crea un nuevo cliente solicitando datos por consola.

        Flujo:
        1. Se solicitan y validan todos los campos.
        2. Se genera automáticamente el siguiente id disponible.
        3. Se construye el objeto Cliente.
        4. Se guarda en el repositorio.
        """
        print("\n--- Alta de cliente ---")

        nombre = self._validator.read_text("Nombre: ")
        apellido_paterno = self._validator.read_text("Apellido paterno: ")
        apellido_materno = self._validator.read_text("Apellido materno: ")

        telefonos = self._validator.read_phone_list(
            "Telefonos (uno o varios separados por coma): "
        )
        correos = self._validator.read_email_list(
            "Correos (uno o varios separados por coma): "
        )
        fecha_nacimiento = self._validator.read_date_iso(
            "Fecha nacimiento (YYYY-MM-DD): "
        )

        calle = self._validator.read_text("Calle: ")
        numero_interior = self._validator.read_int(
            "Numero interior (enter si no aplica): ",
            allow_empty=True
        )
        numero_exterior = self._validator.read_int(
            "Numero exterior (enter si no aplica): ",
            allow_empty=True
        )
        colonia = self._validator.read_text("Colonia: ")
        estado = self._validator.read_text("Estado: ")

        metodo_pago = self._read_payment_method()

        visitas_anuales = (
            self._validator.read_int(
                "Visitas anuales (entero, 0 si no aplica): ",
                allow_empty=False,
                default=0
            ) or 0
        )

        cliente = Cliente(
            id_value=self._repository.next_id(),
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            telefonos=telefonos,
            correos=correos,
            fecha_nacimiento=fecha_nacimiento,
            calle=calle,
            numero_interior=numero_interior,
            numero_exterior=numero_exterior,
            colonia=colonia,
            estado=estado,
            metodo_pago=metodo_pago,
            visitas_anuales=visitas_anuales,
        )

        self._repository.add(cliente.to_row())
        print(f"Cliente creado con id={cliente.id}.")

    def edit_interactive(self) -> None:
        """
        Edita un cliente existente.

        Permite presionar Enter para conservar el valor actual.
        Se reconstruye el objeto Cliente con los nuevos valores
        y se actualiza en el repositorio.
        """
        key_value = self._validator.require_existing_id(
            input("Ingresa el id del cliente a editar: ")
        )

        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un cliente con id={key_value}.")

        current = Cliente.from_row(row)
        print("\n--- Editar cliente (enter = conservar valor actual) ---")

        nombre = self._validator.read_text(
            f"Nombre [{current.nombre}]: ",
            allow_empty=True,
            default=current.nombre
        )

        apellido_paterno = self._validator.read_text(
            f"Apellido paterno [{current.apellido_paterno}]: ",
            allow_empty=True,
            default=current.apellido_paterno,
        )

        apellido_materno = self._validator.read_text(
            f"Apellido materno [{current.apellido_materno}]: ",
            allow_empty=True,
            default=current.apellido_materno,
        )

        raw_telefonos = input(
            f"Telefonos (coma) [{current.telefonos.replace('|', ', ')}]: "
        ).strip()
        telefonos = (
            current.telefonos
            if not raw_telefonos
            else self._validator.read_phone_list("Reingresa telefonos: ")
        )

        raw_correos = input(
            f"Correos (coma) [{current.correos.replace('|', ', ')}]: "
        ).strip()
        correos = (
            current.correos
            if not raw_correos
            else self._validator.read_email_list("Reingresa correos: ")
        )

        fecha_nacimiento = self._validator.read_date_iso(
            f"Fecha nacimiento [{current.fecha_nacimiento}]: ",
            allow_empty=True,
            default=current.fecha_nacimiento,
        )

        calle = self._validator.read_text(
            f"Calle [{current.calle}]: ",
            allow_empty=True,
            default=current.calle
        )

        numero_interior = self._validator.read_int(
            f"Numero interior [{'' if current.numero_interior is None else current.numero_interior}]: ",
            allow_empty=True,
            default=current.numero_interior,
        )

        numero_exterior = self._validator.read_int(
            f"Numero exterior [{'' if current.numero_exterior is None else current.numero_exterior}]: ",
            allow_empty=True,
            default=current.numero_exterior,
        )

        colonia = self._validator.read_text(
            f"Colonia [{current.colonia}]: ",
            allow_empty=True,
            default=current.colonia
        )

        estado = self._validator.read_text(
            f"Estado [{current.estado}]: ",
            allow_empty=True,
            default=current.estado
        )

        metodo_pago = self._read_payment_method(default=current.metodo_pago)

        visitas_anuales = self._validator.read_int(
            f"Visitas anuales [{current.visitas_anuales}]: ",
            allow_empty=True,
            default=current.visitas_anuales,
        )

        if visitas_anuales is None:
            visitas_anuales = current.visitas_anuales

        updated = Cliente(
            id_value=int(key_value),
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            telefonos=telefonos,
            correos=correos,
            fecha_nacimiento=fecha_nacimiento,
            calle=calle,
            numero_interior=numero_interior,
            numero_exterior=numero_exterior,
            colonia=colonia,
            estado=estado,
            metodo_pago=metodo_pago,
            visitas_anuales=visitas_anuales,
        )

        self._repository.update(key_value, updated.to_row())
        print("Cliente actualizado.")

    def delete_interactive(self) -> None:
        """
        Elimina un cliente por id.

        Se solicita confirmación antes de realizar la operación.
        """
        key_value = self._validator.require_existing_id(
            input("Ingresa el id del cliente a eliminar: ")
        )

        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un cliente con id={key_value}.")

        confirm = self._validator.read_bool(
            "Seguro que deseas eliminarlo? (s/n): ",
            default=False
        )

        if not confirm:
            print("Operacion cancelada.")
            return

        self._repository.delete(key_value)
        print("Cliente eliminado.")

    def _read_payment_method(self, default: str | None = None) -> str:
        """
        Lee y valida el método de pago permitido.

        Valores aceptados:
        - 1 o EFECTIVO
        - 2 o TARJETA

        Si se proporciona un valor por defecto y el usuario presiona Enter,
        se conserva dicho valor.
        """
        allowed = {
            "1": "EFECTIVO",
            "2": "TARJETA",
            "EFECTIVO": "EFECTIVO",
            "TARJETA": "TARJETA"
        }

        while True:
            default_label = "" if default is None else f" [{default}]"
            raw_value = input(
                f"Metodo de pago: 1) Efectivo  2) Tarjeta{default_label}: "
            ).strip().upper()

            if not raw_value and default is not None:
                return default

            value = allowed.get(raw_value)
            if value:
                return value

            print("Entrada invalida: elige 1 (EFECTIVO) o 2 (TARJETA).")

    def _print_full(self, cliente: Cliente) -> None:
        """
        Imprime todos los datos de un cliente en formato legible.

        Incluye:
        - Información personal
        - Domicilio
        - Método de pago
        - Número de visitas
        - Descuento calculado dinámicamente
        """
        full_name = (
            f"{cliente.nombre} "
            f"{cliente.apellido_paterno} "
            f"{cliente.apellido_materno}"
        ).strip()

        print("\n--- Detalle de cliente ---")
        print(f"Id: {cliente.id}")
        print(f"Nombre: {full_name}")
        print(f"Telefonos: {cliente.telefonos.replace('|', ', ')}")
        print(f"Correos: {cliente.correos.replace('|', ', ')}")
        print(f"Fecha nacimiento: {cliente.fecha_nacimiento}")

        print("Domicilio:")
        print(f"  Calle: {cliente.calle}")
        print(f"  Num interior: {'' if cliente.numero_interior is None else cliente.numero_interior}")
        print(f"  Num exterior: {'' if cliente.numero_exterior is None else cliente.numero_exterior}")
        print(f"  Colonia: {cliente.colonia}")
        print(f"  Estado: {cliente.estado}")

        print(f"Metodo de pago: {cliente.metodo_pago}")
        print(f"Visitas anuales: {cliente.visitas_anuales}")
        print(f"Descuento aplicable: {cliente.tasa_descuento()}%")
