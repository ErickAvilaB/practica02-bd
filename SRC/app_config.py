from pathlib import Path


class AppConfig:
    """Configuracion del prototipo.

    Define donde se encuentran los archivos CSV.
    Por requerimiento del entregable, los CSV viven dentro de la carpeta SRC/.

    Se usa una ruta relativa a este archivo para evitar problemas cuando se ejecute
    desde otra carpeta.
    """

    def __init__(self) -> None:
        src_dir = Path(__file__).resolve().parent

        self.sucursales_csv = src_dir / "sucursales.csv"
        self.productos_csv = src_dir / "productos.csv"
        self.clientes_csv = src_dir / "clientes.csv"

        self.sucursales_header = [
            "id",
            "nombre",
            "calle",
            "numero_interior",
            "numero_exterior",
            "colonia",
            "estado",
            "telefono",
            "horario_atencion",
            "tiene_clinica",
            "nombre_clinica",
            "clinica_numero_cuartos",
            "clinica_numero_empleados",
            "clinica_horario_atencion",
        ]

        # Nota: el caso de uso separa medicamentos e insumos; el prototipo usa una sola entidad "producto"
        # con categoria MEDICAMENTO o INSUMO. Esto mantiene el entregable simple y alineado al punto ii,
        # pero conserva los campos mas relevantes para poblar la BD despues. 
        self.productos_header = [
            "id",
            "categoria",  # MEDICAMENTO | INSUMO
            "requiere_receta",  # 1/0 (sirve para venta en linea en el futuro)
            "nombre_comercial",
            "nombre_generico",
            "nombre_cientifico",
            "tipo",  # para insumos: principio activo, excipiente, vehiculo, etc.
            "forma_farmaceutica",  # para medicamentos: tableta, jarabe, etc.
            "forma_fisica",  # para insumos: polvo, solucion, gel, etc.
            "concentracion_potencia",
            "presentacion",
            "via_administracion",
            "clasificacion",
            "tipo_control",
            "laboratorio_fabricante",
            "grado_farmacopeico",
            "riesgo",
            "es_esteril",
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

        self.clientes_header = [
            "id",
            "nombre",
            "apellido_paterno",
            "apellido_materno",
            "telefonos",
            "correos",
            "fecha_nacimiento",
            "calle",
            "numero_interior",
            "numero_exterior",
            "colonia",
            "estado",
            "metodo_pago",  # EFECTIVO | TARJETA
            "visitas_anuales",
        ]
