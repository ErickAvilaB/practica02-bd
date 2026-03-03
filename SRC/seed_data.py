from csv_repository import CsvRepository
from cliente import Cliente
from producto import Producto
from sucursal import Sucursal


class SeedData:
    """
    Generador de datos iniciales (seed) para pruebas del sistema.

    Esta clase se encarga de poblar los repositorios CSV con
    información mínima pero realista para facilitar:

    - Pruebas funcionales
    - Pruebas de descuentos por visitas anuales
    - Validación de relaciones entre entidades
    - Pruebas de productos de distintas categorías

    Entidades generadas:
    - Sucursales (incluye una con clínica activa)
    - Productos (mezcla de medicamentos e insumos)
    - Clientes (con diferente número de visitas anuales)

    IMPORTANTE:
    El método `generate()` sobrescribe completamente el contenido
    actual de los archivos CSV.
    """

    def __init__(
        self,
        sucursal_repository: CsvRepository,
        producto_repository: CsvRepository,
        cliente_repository: CsvRepository,
    ) -> None:
        """
        Inicializa el generador de datos con los repositorios necesarios.

        :param sucursal_repository: Repositorio para persistencia de sucursales.
        :param producto_repository: Repositorio para persistencia de productos.
        :param cliente_repository: Repositorio para persistencia de clientes.
        """
        self._sucursal_repository = sucursal_repository
        self._producto_repository = producto_repository
        self._cliente_repository = cliente_repository

    def generate(self) -> None:
        """
        Genera y guarda datos de prueba en los repositorios.

        Proceso:
        1. Crea instancias de Sucursal.
        2. Crea instancias de Producto.
        3. Crea instancias de Cliente.
        4. Convierte cada objeto a formato fila (to_row()).
        5. Sobrescribe completamente los CSV usando replace_with().

        Nota:
        Este método elimina cualquier dato previo almacenado en los CSV.
        """

        # ---------------------------
        # Sucursales de prueba
        # ---------------------------
        # Incluye:
        # - Una sucursal con clínica activa
        # - Una sucursal sin clínica
        sucursales = [
            Sucursal(
                id_value=1,
                nombre="Xiao Mao Centro",
                calle="Av Principal",
                numero_interior=None,
                numero_exterior=123,
                colonia="Centro",
                estado="CDMX",
                telefono="5512345678",
                horario_atencion="L-D 09:00-21:00",
                tiene_clinica=True,
                nombre_clinica="Clinica Centro",
                clinica_numero_cuartos=3,
                clinica_numero_empleados=8,
                clinica_horario_atencion="L-S 10:00-18:00",
            ),
            Sucursal(
                id_value=2,
                nombre="Xiao Mao Norte",
                calle="Calle Pinos",
                numero_interior=2,
                numero_exterior=45,
                colonia="San Andres",
                estado="CDMX",
                telefono="5598765432",
                horario_atencion="L-V 08:00-20:00",
                tiene_clinica=False,
                nombre_clinica="",
                clinica_numero_cuartos=None,
                clinica_numero_empleados=None,
                clinica_horario_atencion="",
            ),
        ]

        # ---------------------------
        # Productos de prueba
        # ---------------------------
        # Incluye:
        # - Medicamento de venta libre
        # - Medicamento bajo receta
        # - Insumo farmacéutico
        productos = [
            Producto(
                id_value=1,
                categoria="MEDICAMENTO",
                requiere_receta=False,
                nombre_comercial="Paracetamol Generico",
                nombre_generico="Paracetamol",
                nombre_cientifico="",
                tipo="",
                forma_farmaceutica="Tableta",
                forma_fisica="",
                concentracion_potencia="500 mg",
                presentacion="Caja 20 tabletas",
                via_administracion="Oral",
                clasificacion="Analgesico",
                tipo_control="Venta libre",
                laboratorio_fabricante="Laboratorios Ejemplo",
                grado_farmacopeico="",
                riesgo="",
                es_esteril=False,
                temperatura_almacenamiento="",
                sensibilidad="",
                condiciones_almacenamiento="Seco y fresco",
                fecha_recepcion="2026-01-10",
                fecha_caducidad="2027-01-10",
                precio_unitario="12.50",
                precio_publico="25.00",
                descripcion="Tableta blanca.",
                observaciones="",
            ),
            Producto(
                id_value=2,
                categoria="MEDICAMENTO",
                requiere_receta=True,
                nombre_comercial="Amoxicilina",
                nombre_generico="Amoxicilina",
                nombre_cientifico="",
                tipo="",
                forma_farmaceutica="Capsula",
                forma_fisica="",
                concentracion_potencia="500 mg",
                presentacion="Caja 12 capsulas",
                via_administracion="Oral",
                clasificacion="Antibiotico",
                tipo_control="Bajo receta medica",
                laboratorio_fabricante="Farmaceutica Demo",
                grado_farmacopeico="",
                riesgo="",
                es_esteril=False,
                temperatura_almacenamiento="",
                sensibilidad="",
                condiciones_almacenamiento="Seco",
                fecha_recepcion="2026-02-01",
                fecha_caducidad="2027-02-01",
                precio_unitario="35.00",
                precio_publico="70.00",
                descripcion="Capsulas duras.",
                observaciones="",
            ),
            Producto(
                id_value=3,
                categoria="INSUMO",
                requiere_receta=False,
                nombre_comercial="Glicerina",
                nombre_generico="",
                nombre_cientifico="Glicerol",
                tipo="Vehiculo",
                forma_farmaceutica="",
                forma_fisica="Liquido",
                concentracion_potencia="99.5%",
                presentacion="",
                via_administracion="",
                clasificacion="",
                tipo_control="",
                laboratorio_fabricante="",
                grado_farmacopeico="USP",
                riesgo="No peligroso",
                es_esteril=False,
                temperatura_almacenamiento="15-25C",
                sensibilidad="Humedad",
                condiciones_almacenamiento="Envase bien cerrado",
                fecha_recepcion="2026-01-15",
                fecha_caducidad="2028-01-15",
                precio_unitario="50.00",
                precio_publico="95.00",
                descripcion="",
                observaciones="Usar envase bien cerrado.",
            ),
        ]

        # ---------------------------
        # Clientes de prueba
        # ---------------------------
        # Incluye:
        # - Cliente con 7 visitas (para probar descuentos altos)
        # - Cliente con 4 visitas (nivel intermedio)
        clientes = [
            Cliente(
                id_value=1,
                nombre="Maria",
                apellido_paterno="Gomez",
                apellido_materno="Luna",
                telefonos="5510001111",
                correos="maria@example.com",
                fecha_nacimiento="1998-05-10",
                calle="Calle Reforma",
                numero_interior=None,
                numero_exterior=10,
                colonia="Centro",
                estado="CDMX",
                metodo_pago="TARJETA",
                visitas_anuales=7,
            ),
            Cliente(
                id_value=2,
                nombre="Juan",
                apellido_paterno="Perez",
                apellido_materno="Soto",
                telefonos="5522223333|5544445555",
                correos="juan@example.com|juan.perez@correo.com",
                fecha_nacimiento="2001-11-02",
                calle="Av Universidad",
                numero_interior=5,
                numero_exterior=120,
                colonia="Del Valle",
                estado="CDMX",
                metodo_pago="EFECTIVO",
                visitas_anuales=4,
            ),
        ]

        # Persistencia: conversión de objetos a filas CSV
        # y sobrescritura completa de archivos.
        self._sucursal_repository.replace_with([s.to_row() for s in sucursales])
        self._producto_repository.replace_with([p.to_row() for p in productos])
        self._cliente_repository.replace_with([c.to_row() for c in clientes])
