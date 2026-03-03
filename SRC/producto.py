class Producto:
    """
    Modelo unificado que representa un producto dentro del sistema.

    Un producto puede ser:
        - MEDICAMENTO
        - INSUMO

    Esta clase está diseñada para cumplir con los requerimientos del prototipo,
    donde se mantiene un catálogo centralizado de:
        - Sucursales
        - Medicamentos/Insumos
        - Clientes

    Aunque el caso de uso menciona inventario por sucursal, proveedores,
    tickets y venta en línea, este modelo se enfoca únicamente en los
    atributos necesarios para:

        - Persistencia en almacenamiento plano (CSV).
        - Futuro poblamiento de base de datos.
        - Venta en línea (ej. control de receta).
        - Gestión de lotes, fechas y precios.

    Atributos relevantes:
        - requiere_receta: necesario para venta en línea.
        - fecha_recepcion y fecha_caducidad: control de lotes.
        - condiciones_almacenamiento: logística.
        - precio_unitario y precio_publico: control comercial.
    """

    def __init__(
        self,
        id_value: int,
        categoria: str,
        requiere_receta: bool,
        nombre_comercial: str,
        nombre_generico: str,
        nombre_cientifico: str,
        tipo: str,
        forma_farmaceutica: str,
        forma_fisica: str,
        concentracion_potencia: str,
        presentacion: str,
        via_administracion: str,
        clasificacion: str,
        tipo_control: str,
        laboratorio_fabricante: str,
        grado_farmacopeico: str,
        riesgo: str,
        es_esteril: bool,
        temperatura_almacenamiento: str,
        sensibilidad: str,
        condiciones_almacenamiento: str,
        fecha_recepcion: str,
        fecha_caducidad: str,
        precio_unitario: str,
        precio_publico: str,
        descripcion: str,
        observaciones: str,
    ) -> None:
        """
        Constructor del modelo Producto.

        Args:
            id_value (int): Identificador único del producto.
            categoria (str): Tipo de producto (MEDICAMENTO o INSUMO).
            requiere_receta (bool): Indica si requiere receta médica.
            nombre_comercial (str): Nombre comercial del producto.
            nombre_generico (str): Nombre genérico.
            nombre_cientifico (str): Nombre científico o principio activo.
            tipo (str): Tipo interno del producto.
            forma_farmaceutica (str): Tableta, cápsula, jarabe, etc.
            forma_fisica (str): Estado físico (sólido, líquido, etc.).
            concentracion_potencia (str): Concentración o potencia.
            presentacion (str): Empaque o formato de venta.
            via_administracion (str): Oral, intravenosa, tópica, etc.
            clasificacion (str): Clasificación farmacológica.
            tipo_control (str): Tipo de control sanitario.
            laboratorio_fabricante (str): Laboratorio fabricante.
            grado_farmacopeico (str): Grado farmacéutico.
            riesgo (str): Nivel o tipo de riesgo.
            es_esteril (bool): Indica si es producto estéril.
            temperatura_almacenamiento (str): Rango de temperatura.
            sensibilidad (str): Sensibilidad a luz, humedad, etc.
            condiciones_almacenamiento (str): Recomendaciones especiales.
            fecha_recepcion (str): Fecha de recepción (YYYY-MM-DD).
            fecha_caducidad (str): Fecha de caducidad (YYYY-MM-DD).
            precio_unitario (str): Precio de adquisición.
            precio_publico (str): Precio de venta al público.
            descripcion (str): Descripción general del producto.
            observaciones (str): Notas adicionales.
        """
        self.id = id_value
        self.categoria = categoria
        self.requiere_receta = requiere_receta
        self.nombre_comercial = nombre_comercial
        self.nombre_generico = nombre_generico
        self.nombre_cientifico = nombre_cientifico
        self.tipo = tipo
        self.forma_farmaceutica = forma_farmaceutica
        self.forma_fisica = forma_fisica
        self.concentracion_potencia = concentracion_potencia
        self.presentacion = presentacion
        self.via_administracion = via_administracion
        self.clasificacion = clasificacion
        self.tipo_control = tipo_control
        self.laboratorio_fabricante = laboratorio_fabricante
        self.grado_farmacopeico = grado_farmacopeico
        self.riesgo = riesgo
        self.es_esteril = es_esteril
        self.temperatura_almacenamiento = temperatura_almacenamiento
        self.sensibilidad = sensibilidad
        self.condiciones_almacenamiento = condiciones_almacenamiento
        self.fecha_recepcion = fecha_recepcion
        self.fecha_caducidad = fecha_caducidad
        self.precio_unitario = precio_unitario
        self.precio_publico = precio_publico
        self.descripcion = descripcion
        self.observaciones = observaciones

    def to_row(self) -> dict[str, str]:
        """
        Convierte el objeto Producto a un diccionario serializable para CSV.

        Returns:
            dict[str, str]: Representación del producto lista para escritura
                            en archivo CSV.

        Notas:
            - Los valores booleanos se convierten a "1" (True) o "0" (False).
            - El ID se convierte explícitamente a cadena.
            - Todas las claves coinciden con los encabezados del CSV.
        """
        return {
            "id": str(self.id),
            "categoria": self.categoria,
            "requiere_receta": "1" if self.requiere_receta else "0",
            "nombre_comercial": self.nombre_comercial,
            "nombre_generico": self.nombre_generico,
            "nombre_cientifico": self.nombre_cientifico,
            "tipo": self.tipo,
            "forma_farmaceutica": self.forma_farmaceutica,
            "forma_fisica": self.forma_fisica,
            "concentracion_potencia": self.concentracion_potencia,
            "presentacion": self.presentacion,
            "via_administracion": self.via_administracion,
            "clasificacion": self.clasificacion,
            "tipo_control": self.tipo_control,
            "laboratorio_fabricante": self.laboratorio_fabricante,
            "grado_farmacopeico": self.grado_farmacopeico,
            "riesgo": self.riesgo,
            "es_esteril": "1" if self.es_esteril else "0",
            "temperatura_almacenamiento": self.temperatura_almacenamiento,
            "sensibilidad": self.sensibilidad,
            "condiciones_almacenamiento": self.condiciones_almacenamiento,
            "fecha_recepcion": self.fecha_recepcion,
            "fecha_caducidad": self.fecha_caducidad,
            "precio_unitario": self.precio_unitario,
            "precio_publico": self.precio_publico,
            "descripcion": self.descripcion,
            "observaciones": self.observaciones,
        }

    @staticmethod
    def from_row(row: dict[str, str]) -> "Producto":
        """
        Crea una instancia de Producto a partir de una fila leída de un CSV.

        Args:
            row (dict[str, str]): Diccionario con los datos de una fila CSV.

        Returns:
            Producto: Objeto reconstruido a partir de los datos almacenados.

        Comportamiento:
            - Convierte el ID a entero.
            - Interpreta "1" como True y cualquier otro valor como False
              para campos booleanos.
            - Aplica strip() para evitar espacios no deseados.
            - Usa valores por defecto seguros si alguna clave no existe.
        """
        return Producto(
            id_value=int((row.get("id") or "0").strip() or "0"),
            categoria=(row.get("categoria") or "").strip(),
            requiere_receta=((row.get("requiere_receta") or "0").strip() == "1"),
            nombre_comercial=(row.get("nombre_comercial") or "").strip(),
            nombre_generico=(row.get("nombre_generico") or "").strip(),
            nombre_cientifico=(row.get("nombre_cientifico") or "").strip(),
            tipo=(row.get("tipo") or "").strip(),
            forma_farmaceutica=(row.get("forma_farmaceutica") or "").strip(),
            forma_fisica=(row.get("forma_fisica") or "").strip(),
            concentracion_potencia=(row.get("concentracion_potencia") or "").strip(),
            presentacion=(row.get("presentacion") or "").strip(),
            via_administracion=(row.get("via_administracion") or "").strip(),
            clasificacion=(row.get("clasificacion") or "").strip(),
            tipo_control=(row.get("tipo_control") or "").strip(),
            laboratorio_fabricante=(row.get("laboratorio_fabricante") or "").strip(),
            grado_farmacopeico=(row.get("grado_farmacopeico") or "").strip(),
            riesgo=(row.get("riesgo") or "").strip(),
            es_esteril=((row.get("es_esteril") or "0").strip() == "1"),
            temperatura_almacenamiento=(row.get("temperatura_almacenamiento") or "").strip(),
            sensibilidad=(row.get("sensibilidad") or "").strip(),
            condiciones_almacenamiento=(row.get("condiciones_almacenamiento") or "").strip(),
            fecha_recepcion=(row.get("fecha_recepcion") or "").strip(),
            fecha_caducidad=(row.get("fecha_caducidad") or "").strip(),
            precio_unitario=(row.get("precio_unitario") or "").strip(),
            precio_publico=(row.get("precio_publico") or "").strip(),
            descripcion=(row.get("descripcion") or "").strip(),
            observaciones=(row.get("observaciones") or "").strip(),
        )
