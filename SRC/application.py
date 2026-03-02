from app_config import AppConfig
from csv_repository import CsvRepository
from errors import AppError
from input_validator import InputValidator
from menu import Menu
from seed_data import SeedData

from sucursal_service import SucursalService
from producto_service import ProductoService
from cliente_service import ClienteService


class Application:
    """Aplicacion principal del prototipo.

    Requisitos del punto ii:
    - Almacenar informacion de sucursales, medicamentos/insumos y clientes en CSV
    - Permitir agregar, consultar, editar y eliminar (CRUD)
    - Tener al menos un menu de interaccion
    - Consultas por llave: recibir id y regresar todos los datos relacionados
    - Validar campos numericos
    - Manejo de excepciones con mensajes claros

    Adicional (alineado a requerimientos del analisis):
    - Descuento se calcula a partir de visitas_anuales
    - Producto incluye campo requiere_receta, util para venta en linea mas adelante
    """

    def __init__(self) -> None:
        config = AppConfig()
        validator = InputValidator()
        menu = Menu()

        sucursal_repository = CsvRepository(config.sucursales_csv, config.sucursales_header)
        producto_repository = CsvRepository(config.productos_csv, config.productos_header)
        cliente_repository = CsvRepository(config.clientes_csv, config.clientes_header)

        self._validator = validator
        self._menu = menu

        self._sucursal_service = SucursalService(sucursal_repository, validator)
        self._producto_service = ProductoService(producto_repository, validator)
        self._cliente_service = ClienteService(cliente_repository, validator)

        self._seed_data = SeedData(
            sucursal_repository=sucursal_repository,
            producto_repository=producto_repository,
            cliente_repository=cliente_repository,
        )

    def run(self) -> None:
        """Ejecuta el ciclo principal del programa."""
        print("Prototipo CSV - Una farmacia de otro mundo (Xiao Mao)")

        while True:
            try:
                option = self._menu.choose_option(
                    "Menu principal",
                    [
                        "Sucursales",
                        "Productos (medicamentos/insumos)",
                        "Clientes",
                        "Poblar CSV con datos de prueba",
                        "Salir",
                    ],
                )

                if option == 1:
                    self._entity_loop("Sucursales", self._sucursal_service)
                elif option == 2:
                    self._entity_loop("Productos", self._producto_service)
                elif option == 3:
                    self._entity_loop("Clientes", self._cliente_service)
                elif option == 4:
                    self._populate_test_data()
                elif option == 5:
                    print("Saliendo. Hasta luego.")
                    return

            except AppError as error:
                print("\n[ERROR] " + str(error))
            except KeyboardInterrupt:
                print("\nInterrumpido por el usuario. Saliendo.")
                return
            except Exception as error:
                print("\n[ERROR INESPERADO] " + str(error))

    def _entity_loop(self, title: str, service) -> None:
        """Submenu de CRUD para una entidad."""
        while True:
            option = self._menu.choose_option(
                title,
                [
                    "Listar",
                    "Consultar por id",
                    "Agregar",
                    "Editar",
                    "Eliminar",
                    "Volver",
                ],
            )

            if option == 1:
                service.list_brief()
            elif option == 2:
                service.consult_by_id()
            elif option == 3:
                service.create_interactive()
            elif option == 4:
                service.edit_interactive()
            elif option == 5:
                service.delete_interactive()
            elif option == 6:
                return

    def _populate_test_data(self) -> None:
        """Puebla los CSV con datos de prueba (sobrescribe el contenido)."""
        print("\nEsta accion SOBRESCRIBIRA los CSV actuales (perderas datos).")
        confirm = self._validator.read_bool("Deseas continuar? (s/n): ", default=False)
        if not confirm:
            print("Operacion cancelada.")
            return

        self._seed_data.generate()
        print("Datos de prueba generados correctamente.")
