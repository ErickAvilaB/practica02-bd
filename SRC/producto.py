class Producto:
    """Modelo unificado para medicamento o insumo (producto).

    Por requerimiento del prototipo (punto ii), se almacena un catalogo de:
    - Sucursales
    - Medicamentos/Insumos
    - Clientes

    El caso de uso separa medicamentos e insumos, y ademas menciona inventario por sucursal,
    proveedores, tickets y venta en linea. Para no salirnos del alcance del prototipo, aqui
    guardamos los campos del producto que seran utiles para poblar la BD mas adelante:
    - Para venta en linea: requiere_receta
    - Para lotes y precios: fecha_recepcion, fecha_caducidad, condiciones_almacenamiento,
      precio_unitario y precio_publico

    Categoria:
    - MEDICAMENTO
    - INSUMO
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
        """Convierte el objeto a una fila CSV."""
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
        """Crea un Producto a partir de una fila CSV."""
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
