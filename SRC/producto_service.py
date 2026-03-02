from csv_repository import CsvRepository
from errors import AppError
from input_validator import InputValidator
from producto import Producto


class ProductoService:
    """Casos de uso (CRUD) para productos (medicamentos e insumos)."""

    def __init__(self, repository: CsvRepository, validator: InputValidator) -> None:
        self._repository = repository
        self._validator = validator

    def list_brief(self) -> None:
        """Lista productos mostrando id, categoria y nombre comercial."""
        rows = self._repository.list_all()
        if not rows:
            print("No hay productos registrados.")
            return

        print("\nProductos registrados:")
        for row in rows:
            print(f"  [{row.get('id')}] ({row.get('categoria')}) {row.get('nombre_comercial')}")

    def consult_by_id(self) -> None:
        """Consulta un producto por id y muestra todos sus datos."""
        key_value = self._validator.require_existing_id(input("Ingresa el id del producto: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un producto con id={key_value}.")

        item = Producto.from_row(row)
        self._print_full(item)

    def create_interactive(self) -> None:
        """Captura un nuevo producto desde consola y lo guarda."""
        print("\n--- Alta de producto ---")
        categoria = self._read_category()
        requiere_receta = self._validator.read_bool("Requiere receta? (s/n): ", default=False)

        nombre_comercial = self._validator.read_text("Nombre comercial: ")

        # Inicializamos con cadenas vacias para no dejar None.
        nombre_generico = ""
        nombre_cientifico = ""
        tipo = ""
        forma_farmaceutica = ""
        forma_fisica = ""
        concentracion_potencia = ""
        presentacion = ""
        via_administracion = ""
        clasificacion = ""
        tipo_control = ""
        laboratorio_fabricante = ""
        grado_farmacopeico = ""
        riesgo = ""
        es_esteril = False
        temperatura_almacenamiento = ""
        sensibilidad = ""
        condiciones_almacenamiento = ""
        fecha_recepcion = ""
        fecha_caducidad = ""
        precio_unitario = ""
        precio_publico = ""
        descripcion = ""
        observaciones = ""

        # Campos generales de lote y precio (opcionales en el prototipo).
        fecha_recepcion = self._validator.read_date_iso("Fecha recepcion (YYYY-MM-DD, enter si no aplica): ", allow_empty=True)
        fecha_caducidad = self._validator.read_date_iso("Fecha caducidad (YYYY-MM-DD, enter si no aplica): ", allow_empty=True)
        condiciones_almacenamiento = self._validator.read_text("Condiciones de almacenamiento (enter si no aplica): ", allow_empty=True)

        raw_precio_unitario = input("Precio unitario (ej. 12.50, enter si no aplica): ").strip()
        if raw_precio_unitario:
            precio_unitario = self._validator.require_money(raw_precio_unitario, "precio unitario")

        raw_precio_publico = input("Precio publico (ej. 20.00, enter si no aplica): ").strip()
        if raw_precio_publico:
            precio_publico = self._validator.require_money(raw_precio_publico, "precio publico")

        if categoria == "MEDICAMENTO":
            nombre_generico = self._validator.read_text("Nombre generico: ")
            forma_farmaceutica = self._validator.read_text("Forma farmaceutica (tableta, jarabe, etc.): ")
            concentracion_potencia = self._validator.read_text("Concentracion/Potencia (ej. 500 mg): ")
            presentacion = self._validator.read_text("Presentacion (ej. caja 20 tabletas): ")
            via_administracion = self._validator.read_text("Via de administracion (oral, IV, etc.): ")
            clasificacion = self._validator.read_text("Clasificacion (antibiotico, analgesico, etc.): ")
            tipo_control = self._validator.read_text("Tipo de control (venta libre, bajo receta, etc.): ")
            laboratorio_fabricante = self._validator.read_text("Laboratorio fabricante: ")
            descripcion = self._validator.read_text("Descripcion (enter si no aplica): ", allow_empty=True)
        else:
            nombre_cientifico = self._validator.read_text("Nombre cientifico: ")
            tipo = self._validator.read_text("Tipo (principio activo, excipiente, etc.): ")
            forma_fisica = self._validator.read_text("Forma fisica (polvo, solucion, gel, etc.): ")
            concentracion_potencia = self._validator.read_text("Potencia/Concentracion (ej. 1g/10mL): ")
            grado_farmacopeico = self._validator.read_text("Grado farmacopeico (USP/EP/FEUM, etc.): ")
            riesgo = self._validator.read_text("Riesgo (no peligroso, inflamable, etc.): ")
            es_esteril = self._validator.read_bool("Es esteril? (s/n): ", default=False)
            temperatura_almacenamiento = self._validator.read_text("Temperatura de almacenamiento: ")
            sensibilidad = self._validator.read_text("Sensibilidad (enter si no aplica): ", allow_empty=True)
            observaciones = self._validator.read_text("Observaciones (enter si no aplica): ", allow_empty=True)

        item = Producto(
            id_value=self._repository.next_id(),
            categoria=categoria,
            requiere_receta=requiere_receta,
            nombre_comercial=nombre_comercial,
            nombre_generico=nombre_generico,
            nombre_cientifico=nombre_cientifico,
            tipo=tipo,
            forma_farmaceutica=forma_farmaceutica,
            forma_fisica=forma_fisica,
            concentracion_potencia=concentracion_potencia,
            presentacion=presentacion,
            via_administracion=via_administracion,
            clasificacion=clasificacion,
            tipo_control=tipo_control,
            laboratorio_fabricante=laboratorio_fabricante,
            grado_farmacopeico=grado_farmacopeico,
            riesgo=riesgo,
            es_esteril=es_esteril,
            temperatura_almacenamiento=temperatura_almacenamiento,
            sensibilidad=sensibilidad,
            condiciones_almacenamiento=condiciones_almacenamiento,
            fecha_recepcion=fecha_recepcion,
            fecha_caducidad=fecha_caducidad,
            precio_unitario=precio_unitario,
            precio_publico=precio_publico,
            descripcion=descripcion,
            observaciones=observaciones,
        )

        self._repository.add(item.to_row())
        print(f"Producto creado con id={item.id}.")

    def edit_interactive(self) -> None:
        """Edita un producto existente."""
        key_value = self._validator.require_existing_id(input("Ingresa el id del producto a editar: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un producto con id={key_value}.")

        current = Producto.from_row(row)
        print("\n--- Editar producto (enter = conservar valor actual) ---")

        print(f"Categoria: {current.categoria} (no editable)")
        requiere_receta = self._validator.read_bool(
            f"Requiere receta? (s/n) [{'s' if current.requiere_receta else 'n'}]: ",
            default=current.requiere_receta,
        )

        nombre_comercial = self._validator.read_text(
            f"Nombre comercial [{current.nombre_comercial}]: ",
            allow_empty=True,
            default=current.nombre_comercial,
        )

        # Campos opcionales de lote y precios
        fecha_recepcion = self._validator.read_date_iso(
            f"Fecha recepcion [{current.fecha_recepcion or '-'}]: ",
            allow_empty=True,
            default=current.fecha_recepcion,
        )
        fecha_caducidad = self._validator.read_date_iso(
            f"Fecha caducidad [{current.fecha_caducidad or '-'}]: ",
            allow_empty=True,
            default=current.fecha_caducidad,
        )
        condiciones_almacenamiento = self._validator.read_text(
            f"Condiciones almacenamiento [{current.condiciones_almacenamiento or '-'}]: ",
            allow_empty=True,
            default=current.condiciones_almacenamiento,
        )

        raw_precio_unitario = input(f"Precio unitario [{current.precio_unitario or '-'}]: ").strip()
        precio_unitario = current.precio_unitario
        if raw_precio_unitario:
            precio_unitario = self._validator.require_money(raw_precio_unitario, "precio unitario")

        raw_precio_publico = input(f"Precio publico [{current.precio_publico or '-'}]: ").strip()
        precio_publico = current.precio_publico
        if raw_precio_publico:
            precio_publico = self._validator.require_money(raw_precio_publico, "precio publico")

        if current.categoria == "MEDICAMENTO":
            nombre_generico = self._validator.read_text(
                f"Nombre generico [{current.nombre_generico}]: ",
                allow_empty=True,
                default=current.nombre_generico,
            )
            forma_farmaceutica = self._validator.read_text(
                f"Forma farmaceutica [{current.forma_farmaceutica}]: ",
                allow_empty=True,
                default=current.forma_farmaceutica,
            )
            concentracion_potencia = self._validator.read_text(
                f"Concentracion/Potencia [{current.concentracion_potencia}]: ",
                allow_empty=True,
                default=current.concentracion_potencia,
            )
            presentacion = self._validator.read_text(
                f"Presentacion [{current.presentacion}]: ",
                allow_empty=True,
                default=current.presentacion,
            )
            via_administracion = self._validator.read_text(
                f"Via administracion [{current.via_administracion}]: ",
                allow_empty=True,
                default=current.via_administracion,
            )
            clasificacion = self._validator.read_text(
                f"Clasificacion [{current.clasificacion}]: ",
                allow_empty=True,
                default=current.clasificacion,
            )
            tipo_control = self._validator.read_text(
                f"Tipo control [{current.tipo_control}]: ",
                allow_empty=True,
                default=current.tipo_control,
            )
            laboratorio_fabricante = self._validator.read_text(
                f"Laboratorio [{current.laboratorio_fabricante}]: ",
                allow_empty=True,
                default=current.laboratorio_fabricante,
            )
            descripcion = self._validator.read_text(
                f"Descripcion [{current.descripcion or '-'}]: ",
                allow_empty=True,
                default=current.descripcion,
            )

            updated = Producto(
                id_value=int(key_value),
                categoria=current.categoria,
                requiere_receta=requiere_receta,
                nombre_comercial=nombre_comercial,
                nombre_generico=nombre_generico,
                nombre_cientifico="",
                tipo="",
                forma_farmaceutica=forma_farmaceutica,
                forma_fisica="",
                concentracion_potencia=concentracion_potencia,
                presentacion=presentacion,
                via_administracion=via_administracion,
                clasificacion=clasificacion,
                tipo_control=tipo_control,
                laboratorio_fabricante=laboratorio_fabricante,
                grado_farmacopeico="",
                riesgo="",
                es_esteril=False,
                temperatura_almacenamiento="",
                sensibilidad="",
                condiciones_almacenamiento=condiciones_almacenamiento,
                fecha_recepcion=fecha_recepcion,
                fecha_caducidad=fecha_caducidad,
                precio_unitario=precio_unitario,
                precio_publico=precio_publico,
                descripcion=descripcion,
                observaciones="",
            )
        else:
            nombre_cientifico = self._validator.read_text(
                f"Nombre cientifico [{current.nombre_cientifico}]: ",
                allow_empty=True,
                default=current.nombre_cientifico,
            )
            tipo = self._validator.read_text(
                f"Tipo [{current.tipo}]: ",
                allow_empty=True,
                default=current.tipo,
            )
            forma_fisica = self._validator.read_text(
                f"Forma fisica [{current.forma_fisica}]: ",
                allow_empty=True,
                default=current.forma_fisica,
            )
            concentracion_potencia = self._validator.read_text(
                f"Potencia/Concentracion [{current.concentracion_potencia}]: ",
                allow_empty=True,
                default=current.concentracion_potencia,
            )
            grado_farmacopeico = self._validator.read_text(
                f"Grado farmacopeico [{current.grado_farmacopeico}]: ",
                allow_empty=True,
                default=current.grado_farmacopeico,
            )
            riesgo = self._validator.read_text(
                f"Riesgo [{current.riesgo}]: ",
                allow_empty=True,
                default=current.riesgo,
            )
            es_esteril = self._validator.read_bool(
                f"Es esteril? (s/n) [{'s' if current.es_esteril else 'n'}]: ",
                default=current.es_esteril,
            )
            temperatura_almacenamiento = self._validator.read_text(
                f"Temperatura almacenamiento [{current.temperatura_almacenamiento}]: ",
                allow_empty=True,
                default=current.temperatura_almacenamiento,
            )
            sensibilidad = self._validator.read_text(
                f"Sensibilidad [{current.sensibilidad or '-'}]: ",
                allow_empty=True,
                default=current.sensibilidad,
            )
            observaciones = self._validator.read_text(
                f"Observaciones [{current.observaciones or '-'}]: ",
                allow_empty=True,
                default=current.observaciones,
            )

            updated = Producto(
                id_value=int(key_value),
                categoria=current.categoria,
                requiere_receta=requiere_receta,
                nombre_comercial=nombre_comercial,
                nombre_generico="",
                nombre_cientifico=nombre_cientifico,
                tipo=tipo,
                forma_farmaceutica="",
                forma_fisica=forma_fisica,
                concentracion_potencia=concentracion_potencia,
                presentacion="",
                via_administracion="",
                clasificacion="",
                tipo_control="",
                laboratorio_fabricante="",
                grado_farmacopeico=grado_farmacopeico,
                riesgo=riesgo,
                es_esteril=es_esteril,
                temperatura_almacenamiento=temperatura_almacenamiento,
                sensibilidad=sensibilidad,
                condiciones_almacenamiento=condiciones_almacenamiento,
                fecha_recepcion=fecha_recepcion,
                fecha_caducidad=fecha_caducidad,
                precio_unitario=precio_unitario,
                precio_publico=precio_publico,
                descripcion="",
                observaciones=observaciones,
            )

        self._repository.update(key_value, updated.to_row())
        print("Producto actualizado.")

    def delete_interactive(self) -> None:
        """Elimina un producto por id."""
        key_value = self._validator.require_existing_id(input("Ingresa el id del producto a eliminar: "))
        row = self._repository.get_by_key(key_value)
        if row is None:
            raise AppError(f"No existe un producto con id={key_value}.")

        confirm = self._validator.read_bool("Seguro que deseas eliminarlo? (s/n): ", default=False)
        if not confirm:
            print("Operacion cancelada.")
            return

        self._repository.delete(key_value)
        print("Producto eliminado.")

    def _read_category(self) -> str:
        """Lee la categoria (MEDICAMENTO o INSUMO)."""
        while True:
            raw_value = input("Categoria: 1) Medicamento  2) Insumo: ").strip()
            if raw_value == "1":
                return "MEDICAMENTO"
            if raw_value == "2":
                return "INSUMO"
            print("Entrada invalida: elige 1 o 2.")

    def _print_full(self, item: Producto) -> None:
        """Imprime todos los campos de un producto."""
        print("\n--- Detalle de producto ---")
        print(f"Id: {item.id}")
        print(f"Categoria: {item.categoria}")
        print(f"Requiere receta: {'Si' if item.requiere_receta else 'No'}")
        print(f"Nombre comercial: {item.nombre_comercial}")

        # Campos de lote/precio (si hay)
        if item.fecha_recepcion:
            print(f"Fecha recepcion: {item.fecha_recepcion}")
        if item.fecha_caducidad:
            print(f"Fecha caducidad: {item.fecha_caducidad}")
        if item.condiciones_almacenamiento:
            print(f"Condiciones almacenamiento: {item.condiciones_almacenamiento}")
        if item.precio_unitario:
            print(f"Precio unitario: {item.precio_unitario}")
        if item.precio_publico:
            print(f"Precio publico: {item.precio_publico}")

        if item.categoria == "MEDICAMENTO":
            print(f"Nombre generico: {item.nombre_generico}")
            print(f"Forma farmaceutica: {item.forma_farmaceutica}")
            print(f"Concentracion/Potencia: {item.concentracion_potencia}")
            print(f"Presentacion: {item.presentacion}")
            print(f"Via administracion: {item.via_administracion}")
            print(f"Clasificacion: {item.clasificacion}")
            print(f"Tipo de control: {item.tipo_control}")
            print(f"Laboratorio fabricante: {item.laboratorio_fabricante}")
            if item.descripcion:
                print(f"Descripcion: {item.descripcion}")
        else:
            print(f"Nombre cientifico: {item.nombre_cientifico}")
            print(f"Tipo: {item.tipo}")
            print(f"Forma fisica: {item.forma_fisica}")
            print(f"Potencia/Concentracion: {item.concentracion_potencia}")
            print(f"Grado farmacopeico: {item.grado_farmacopeico}")
            print(f"Riesgo: {item.riesgo}")
            print(f"Es esteril: {'Si' if item.es_esteril else 'No'}")
            print(f"Temperatura almacenamiento: {item.temperatura_almacenamiento}")
            if item.sensibilidad:
                print(f"Sensibilidad: {item.sensibilidad}")
            if item.observaciones:
                print(f"Observaciones: {item.observaciones}")
