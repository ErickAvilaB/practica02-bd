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
    """
    Clase principal de la aplicación.

    Esta clase coordina todos los componentes del sistema:
    - Configuración general
    - Repositorios CSV
    - Servicios de negocio
    - Validaciones
    - Menú de interacción
    - Generación de datos de prueba

    Cumple con los requisitos del punto ii del proyecto:

    Requisitos funcionales:
    ------------------------
    - Almacenar información de sucursales, productos y clientes en archivos CSV.
    - Permitir operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
    - Incluir un menú interactivo.
    - Consultas por llave (id).
    - Validación de campos numéricos.
    - Manejo de excepciones con mensajes claros.

    Requisitos adicionales alineados al análisis:
    ----------------------------------------------
    - El descuento puede calcularse a partir de visitas_anuales del cliente.
    - El producto incluye el campo requiere_receta, útil para futura venta en línea.
    """

    def __init__(self) -> None:
        """
        Inicializa todos los componentes necesarios para la ejecución del sistema.

        Flujo de inicialización:
        1. Se carga la configuración general (rutas y headers).
        2. Se crean los repositorios CSV.
        3. Se crean los servicios de negocio.
        4. Se prepara el generador de datos de prueba.
        """

        # Configuración global (rutas y encabezados)
        config = AppConfig()

        # Componentes auxiliares
        validator = InputValidator()
        menu = Menu()

        # =============================
        # REPOSITORIOS CSV
        # =============================

        # Cada repositorio gestiona lectura y escritura sobre su archivo CSV
        sucursal_repository = CsvRepository(
            config.sucursales_csv,
            config.sucursales_header
        )

        producto_repository = CsvRepository(
            config.productos_csv,
            config.productos_header
        )

        cliente_repository = CsvRepository(
            config.clientes_csv,
            config.clientes_header
        )

        # =============================
        # COMPONENTES PRINCIPALES
        # =============================

        self._validator = validator
        self._menu = menu

        # Servicios de negocio (capa intermedia entre UI y repositorio)
        self._sucursal_service = SucursalService(sucursal_repository, validator)
        self._producto_service = ProductoService(producto_repository, validator)
        self._cliente_service = ClienteService(cliente_repository, validator)

        # Generador de datos iniciales
        self._seed_data = SeedData(
            sucursal_repository=sucursal_repository,
            producto_repository=producto_repository,
            cliente_repository=cliente_repository,
        )

    def run(self) -> None:
        """
        Ejecuta el ciclo principal del programa.

        Este método:
        - Muestra el menú principal.
        - Redirige a los submenús correspondientes.
        - Controla el manejo global de excepciones.
        """

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

            # Manejo de errores controlados de la aplicación
            except AppError as error:
                print("\n[ERROR] " + str(error))

            # Permite salir con Ctrl+C sin mostrar traceback
            except KeyboardInterrupt:
                print("\nInterrumpido por el usuario. Saliendo.")
                return

            # Captura errores inesperados para evitar que el programa colapse
            except Exception as error:
                print("\n[ERROR INESPERADO] " + str(error))

    def _entity_loop(self, title: str, service) -> None:
        """
        Ejecuta el submenú CRUD para una entidad específica.

        Parámetros:
        -----------
        title : str
            Nombre que se mostrará en el menú.
        service :
            Servicio que implementa la lógica de negocio
            (SucursalService, ProductoService o ClienteService).

        Funcionalidades disponibles:
        - Listar registros
        - Consultar por ID
        - Agregar nuevo registro
        - Editar registro existente
        - Eliminar registro
        """

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
        """
        Genera y guarda datos de prueba en los archivos CSV.

        Advertencia:
        ------------
        Esta acción sobrescribe completamente el contenido actual
        de los archivos CSV, eliminando datos existentes.

        Se solicita confirmación explícita al usuario antes de proceder.
        """

        print("\nEsta accion SOBRESCRIBIRA los CSV actuales (perderas datos).")

        confirm = self._validator.read_bool(
            "Deseas continuar? (s/n): ",
            default=False
        )

        if not confirm:
            print("Operacion cancelada.")
            return

        self._seed_data.generate()
        print("Datos de prueba generados correctamente.")
