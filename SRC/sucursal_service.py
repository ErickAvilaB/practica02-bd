from csv_repository import CsvRepository
from errors import AppError
from input_validator import InputValidator
from sucursal import Sucursal


class SucursalService:
    """Casos de uso (CRUD) para sucursales."""

    def __init__(self, repository: CsvRepository, validator: InputValidator) -> None:
        self._repository = repository
        self._validator = validator

    def list_brief(self) -> None:
        """Lista sucursales mostrando id y nombre."""
        rows = self._repository.list_all()
        if not rows:
            print("No hay sucursales registradas.")
            return

        print("\nSucursales registradas:")
        for row in rows:
            print(f"  [{row.get('id')}] {row.get('nombre')}")

    def consult_by_id(self) -> None:
        """Consulta una sucursal por id y muestra todos sus datos."""
        key_value = self._validator.require_existing_id(input("Ingresa el id de la sucursal: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe una sucursal con id={key_value}.")

        sucursal = Sucursal.from_row(row)
        self._print_full(sucursal)

    def create_interactive(self) -> None:
        """Captura una nueva sucursal desde consola y la guarda."""
        print("\n--- Alta de sucursal ---")
        nombre = self._validator.read_text("Nombre de la sucursal: ")
        calle = self._validator.read_text("Calle: ")
        numero_interior = self._validator.read_int("Numero interior (enter si no aplica): ", allow_empty=True)
        numero_exterior = self._validator.read_int("Numero exterior (enter si no aplica): ", allow_empty=True)
        colonia = self._validator.read_text("Colonia: ")
        estado = self._validator.read_text("Estado: ")

        telefono = self._validator.read_text("Telefono (solo digitos): ")
        telefono_clean = telefono.replace(" ", "").replace("-", "")
        if not telefono_clean.isdigit():
            raise AppError("El telefono debe contener solo digitos (puedes usar espacios o guiones).")

        horario_atencion = self._validator.read_text("Horario de atencion (ej. L-V 09:00-18:00): ")

        tiene_clinica = self._validator.read_bool("Tiene clinica integrada? (s/n): ", default=False)
        nombre_clinica = ""
        clinica_numero_cuartos = None
        clinica_numero_empleados = None
        clinica_horario_atencion = ""

        if tiene_clinica:
            nombre_clinica = self._validator.read_text("Nombre de la clinica: ")
            clinica_numero_cuartos = self._validator.read_int("Numero de cuartos (entero): ")
            clinica_numero_empleados = self._validator.read_int("Numero de empleados (entero): ")
            clinica_horario_atencion = self._validator.read_text("Horario de la clinica: ")

        sucursal = Sucursal(
            id_value=self._repository.next_id(),
            nombre=nombre,
            calle=calle,
            numero_interior=numero_interior,
            numero_exterior=numero_exterior,
            colonia=colonia,
            estado=estado,
            telefono=telefono_clean,
            horario_atencion=horario_atencion,
            tiene_clinica=tiene_clinica,
            nombre_clinica=nombre_clinica,
            clinica_numero_cuartos=clinica_numero_cuartos,
            clinica_numero_empleados=clinica_numero_empleados,
            clinica_horario_atencion=clinica_horario_atencion,
        )

        self._repository.add(sucursal.to_row())
        print(f"Sucursal creada con id={sucursal.id}.")

    def edit_interactive(self) -> None:
        """Edita una sucursal existente solicitando nuevos valores por consola."""
        key_value = self._validator.require_existing_id(input("Ingresa el id de la sucursal a editar: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe una sucursal con id={key_value}.")

        current = Sucursal.from_row(row)
        print("\n--- Editar sucursal (enter = conservar valor actual) ---")

        nombre = self._validator.read_text(f"Nombre [{current.nombre}]: ", allow_empty=True, default=current.nombre)
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

        telefono = self._validator.read_text(f"Telefono [{current.telefono}]: ", allow_empty=True, default=current.telefono)
        telefono_clean = telefono.replace(" ", "").replace("-", "")
        if telefono_clean and not telefono_clean.isdigit():
            raise AppError("El telefono debe contener solo digitos (puedes usar espacios o guiones).")

        horario_atencion = self._validator.read_text(
            f"Horario atencion [{current.horario_atencion}]: ",
            allow_empty=True,
            default=current.horario_atencion,
        )

        tiene_clinica = self._validator.read_bool(
            f"Tiene clinica? (s/n) [{'s' if current.tiene_clinica else 'n'}]: ",
            default=current.tiene_clinica,
        )

        nombre_clinica = current.nombre_clinica
        clinica_numero_cuartos = current.clinica_numero_cuartos
        clinica_numero_empleados = current.clinica_numero_empleados
        clinica_horario_atencion = current.clinica_horario_atencion

        if tiene_clinica:
            nombre_clinica = self._validator.read_text(
                f"Nombre clinica [{current.nombre_clinica or '-'}]: ",
                allow_empty=True,
                default=current.nombre_clinica,
            )
            clinica_numero_cuartos = self._validator.read_int(
                f"Numero cuartos [{'' if current.clinica_numero_cuartos is None else current.clinica_numero_cuartos}]: ",
                allow_empty=True,
                default=current.clinica_numero_cuartos,
            )
            clinica_numero_empleados = self._validator.read_int(
                f"Numero empleados [{'' if current.clinica_numero_empleados is None else current.clinica_numero_empleados}]: ",
                allow_empty=True,
                default=current.clinica_numero_empleados,
            )
            clinica_horario_atencion = self._validator.read_text(
                f"Horario clinica [{current.clinica_horario_atencion or '-'}]: ",
                allow_empty=True,
                default=current.clinica_horario_atencion,
            )
        else:
            # Si el usuario quita la clinica, limpiamos campos relacionados.
            nombre_clinica = ""
            clinica_numero_cuartos = None
            clinica_numero_empleados = None
            clinica_horario_atencion = ""

        updated = Sucursal(
            id_value=int(key_value),
            nombre=nombre,
            calle=calle,
            numero_interior=numero_interior,
            numero_exterior=numero_exterior,
            colonia=colonia,
            estado=estado,
            telefono=telefono_clean,
            horario_atencion=horario_atencion,
            tiene_clinica=tiene_clinica,
            nombre_clinica=nombre_clinica,
            clinica_numero_cuartos=clinica_numero_cuartos,
            clinica_numero_empleados=clinica_numero_empleados,
            clinica_horario_atencion=clinica_horario_atencion,
        )

        self._repository.update(key_value, updated.to_row())
        print("Sucursal actualizada.")

    def delete_interactive(self) -> None:
        """Elimina una sucursal por id."""
        key_value = self._validator.require_existing_id(input("Ingresa el id de la sucursal a eliminar: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe una sucursal con id={key_value}.")

        confirm = self._validator.read_bool("Seguro que deseas eliminarla? (s/n): ", default=False)
        if not confirm:
            print("Operacion cancelada.")
            return

        self._repository.delete(key_value)
        print("Sucursal eliminada.")

    def _print_full(self, sucursal: Sucursal) -> None:
        """Imprime todos los campos de una sucursal."""
        print("\n--- Detalle de sucursal ---")
        print(f"Id: {sucursal.id}")
        print(f"Nombre: {sucursal.nombre}")
        print("Direccion:")
        print(f"  Calle: {sucursal.calle}")
        print(f"  Num interior: {'' if sucursal.numero_interior is None else sucursal.numero_interior}")
        print(f"  Num exterior: {'' if sucursal.numero_exterior is None else sucursal.numero_exterior}")
        print(f"  Colonia: {sucursal.colonia}")
        print(f"  Estado: {sucursal.estado}")
        print(f"Telefono: {sucursal.telefono}")
        print(f"Horario: {sucursal.horario_atencion}")
        print(f"Tiene clinica: {'Si' if sucursal.tiene_clinica else 'No'}")

        if sucursal.tiene_clinica:
            print("\nClinica integrada:")
            print(f"  Nombre: {sucursal.nombre_clinica}")
            print(f"  Cuartos: {'' if sucursal.clinica_numero_cuartos is None else sucursal.clinica_numero_cuartos}")
            print(f"  Empleados: {'' if sucursal.clinica_numero_empleados is None else sucursal.clinica_numero_empleados}")
            print(f"  Horario: {sucursal.clinica_horario_atencion}")
