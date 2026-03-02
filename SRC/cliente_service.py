from csv_repository import CsvRepository
from errors import AppError
from input_validator import InputValidator
from cliente import Cliente


class ClienteService:
    """Casos de uso (CRUD) para clientes/pacientes."""

    def __init__(self, repository: CsvRepository, validator: InputValidator) -> None:
        self._repository = repository
        self._validator = validator

    def list_brief(self) -> None:
        """Lista clientes mostrando id y nombre completo."""
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
        """Consulta un cliente por id y muestra todos sus datos (incluye descuento calculado)."""
        key_value = self._validator.require_existing_id(input("Ingresa el id del cliente: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un cliente con id={key_value}.")

        cliente = Cliente.from_row(row)
        self._print_full(cliente)

    def create_interactive(self) -> None:
        """Captura un nuevo cliente desde consola y lo guarda."""
        print("\n--- Alta de cliente ---")
        nombre = self._validator.read_text("Nombre: ")
        apellido_paterno = self._validator.read_text("Apellido paterno: ")
        apellido_materno = self._validator.read_text("Apellido materno: ")

        telefonos = self._validator.read_phone_list("Telefonos (uno o varios separados por coma): ")
        correos = self._validator.read_email_list("Correos (uno o varios separados por coma): ")
        fecha_nacimiento = self._validator.read_date_iso("Fecha nacimiento (YYYY-MM-DD): ")

        calle = self._validator.read_text("Calle: ")
        numero_interior = self._validator.read_int("Numero interior (enter si no aplica): ", allow_empty=True)
        numero_exterior = self._validator.read_int("Numero exterior (enter si no aplica): ", allow_empty=True)
        colonia = self._validator.read_text("Colonia: ")
        estado = self._validator.read_text("Estado: ")

        metodo_pago = self._read_payment_method()

        visitas_anuales = self._validator.read_int("Visitas anuales (entero, 0 si no aplica): ", allow_empty=False, default=0) or 0

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
        """Edita un cliente existente solicitando nuevos valores por consola."""
        key_value = self._validator.require_existing_id(input("Ingresa el id del cliente a editar: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un cliente con id={key_value}.")

        current = Cliente.from_row(row)
        print("\n--- Editar cliente (enter = conservar valor actual) ---")

        nombre = self._validator.read_text(f"Nombre [{current.nombre}]: ", allow_empty=True, default=current.nombre)
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

        # Para listas, aceptamos enter para conservar.
        raw_telefonos = input(f"Telefonos (coma) [{current.telefonos.replace('|', ', ')}]: ").strip()
        telefonos = current.telefonos if not raw_telefonos else self._validator.read_phone_list("Reingresa telefonos: ")

        raw_correos = input(f"Correos (coma) [{current.correos.replace('|', ', ')}]: ").strip()
        correos = current.correos if not raw_correos else self._validator.read_email_list("Reingresa correos: ")

        fecha_nacimiento = self._validator.read_date_iso(
            f"Fecha nacimiento [{current.fecha_nacimiento}]: ",
            allow_empty=True,
            default=current.fecha_nacimiento,
        )

        calle = self._validator.read_text(f"Calle [{current.calle}]: ", allow_empty=True, default=current.calle)
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
        colonia = self._validator.read_text(f"Colonia [{current.colonia}]: ", allow_empty=True, default=current.colonia)
        estado = self._validator.read_text(f"Estado [{current.estado}]: ", allow_empty=True, default=current.estado)

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
        """Elimina un cliente por id."""
        key_value = self._validator.require_existing_id(input("Ingresa el id del cliente a eliminar: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un cliente con id={key_value}.")

        confirm = self._validator.read_bool("Seguro que deseas eliminarlo? (s/n): ", default=False)
        if not confirm:
            print("Operacion cancelada.")
            return

        self._repository.delete(key_value)
        print("Cliente eliminado.")

    def _read_payment_method(self, default: str | None = None) -> str:
        """Lee el metodo de pago permitido (EFECTIVO o TARJETA)."""
        allowed = {"1": "EFECTIVO", "2": "TARJETA", "EFECTIVO": "EFECTIVO", "TARJETA": "TARJETA"}
        while True:
            default_label = "" if default is None else f" [{default}]"
            raw_value = input(f"Metodo de pago: 1) Efectivo  2) Tarjeta{default_label}: ").strip().upper()

            if not raw_value and default is not None:
                return default

            value = allowed.get(raw_value)
            if value:
                return value

            print("Entrada invalida: elige 1 (EFECTIVO) o 2 (TARJETA).")

    def _print_full(self, cliente: Cliente) -> None:
        """Imprime todos los campos de un cliente."""
        full_name = f"{cliente.nombre} {cliente.apellido_paterno} {cliente.apellido_materno}".strip()
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
