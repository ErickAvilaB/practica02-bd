class AppError(Exception):
    """Error controlado del sistema.

    Se usa para reportar fallas previsibles (entrada invalida, registro no encontrado,
    problemas de lectura/escritura, etc.) con mensajes claros para el usuario.
    """
