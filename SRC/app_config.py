from pathlib import Path


class AppConfig:
    """
    Clase de configuración general del prototipo.

    Esta clase centraliza las rutas de los archivos CSV utilizados por el sistema
    y define la estructura (headers) esperada para cada uno de ellos.

    Propósito:
    ----------
    - Evitar rutas absolutas que generen errores al ejecutar el programa
      desde diferentes ubicaciones.
    - Centralizar la definición de columnas de cada archivo CSV.
    - Facilitar futuras migraciones hacia una base de datos relacional.

    Archivos gestionados:
    ----------------------
    - sucursales.csv
    - productos.csv
    - clientes.csv
    """

    def __init__(self) -> None:
        """
        Inicializa las rutas y encabezados de los archivos CSV.

        Las rutas se construyen dinámicamente tomando como referencia
        la ubicación del archivo actual (__file__), lo que garantiza
        portabilidad del proyecto.
        """

        # Obtiene el directorio donde se encuentra este archivo Python.
        # resolve() convierte la ruta a absoluta.
        # parent obtiene la carpeta contenedora.
        src_dir = Path(__file__).resolve().parent

        # =============================
        # RUTAS DE ARCHIVOS CSV
        # =============================

        # Archivo que almacena la información de las sucursales
        self.sucursales_csv = src_dir / "sucursales.csv"

        # Archivo que almacena la información de productos
        self.productos_csv = src_dir / "productos.csv"

        # Archivo que almacena la información de clientes
        self.clientes_csv = src_dir / "clientes.csv"

        # =============================
        # SUCURSALES
        # =============================

        self.sucursales_header = [
            "id",  # Identificador único de la sucursal
            "nombre",  # Nombre comercial de la sucursal
            "calle",
            "numero_interior",
            "numero_exterior",
            "colonia",
            "estado",
            "telefono",
            "horario_atencion",
            "tiene_clinica",  # Indica si la sucursal cuenta con clínica (1/0)
            "nombre_clinica",
            "clinica_numero_cuartos",
            "clinica_numero_empleados",
            "clinica_horario_atencion",
        ]

        # =============================
        # PRODUCTOS
        # =============================

        """
        Nota de diseño:
        ---------------
        El caso de uso original separa medicamentos e insumos.
        Para simplificar el prototipo, ambos se modelan bajo una sola entidad
        llamada "producto", diferenciados por el campo 'categoria'.

        Valores posibles:
        - MEDICAMENTO
        - INSUMO

        Este diseño mantiene el entregable simple, pero permite una futura
        normalización hacia una base de datos más formal.
        """

        self.productos_header = [
            "id",  # Identificador único del producto
            "categoria",  # MEDICAMENTO | INSUMO
            "requiere_receta",  # 1 = sí requiere receta, 0 = no requiere
            "nombre_comercial",
            "nombre_generico",
            "nombre_cientifico",
            "tipo",  # Para insumos: principio activo, excipiente, vehículo, etc.
            "forma_farmaceutica",  # Tableta, cápsula, jarabe, etc.
            "forma_fisica",  # Polvo, solución, gel, etc.
            "concentracion_potencia",
            "presentacion",
            "via_administracion",
            "clasificacion",
            "tipo_control",
            "laboratorio_fabricante",
            "grado_farmacopeico",
            "riesgo",
            "es_esteril",  # 1/0
            "temperatura_almacenamiento",
            "sensibilidad",
            "condiciones_almacenamiento",
            "fecha_recepcion",
            "fecha_caducidad",
            "precio_unitario",
            "precio_publico",
            "descripcion",
            "observaciones",
        ]

        # =============================
        # CLIENTES
        # =============================

        self.clientes_header = [
            "id",  # Identificador único del cliente
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "telefonos",  # Puede contener múltiples valores separados por coma
            "correos",  # Puede contener múltiples correos
            "fecha_nacimiento",
            "calle",
            "numero_interior",
            "numero_exterior",
            "colonia",
            "estado",
            "metodo_pago",  # EFECTIVO | TARJETA
            "visitas_anuales",  # Número estimado de visitas por año
        ]
