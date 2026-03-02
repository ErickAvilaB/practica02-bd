from errors import AppError


class Menu:
    """Menu simple para interaccion por consola."""

    def choose_option(self, title: str, options: list[str]) -> int:
        """Muestra un menu y regresa el indice (1..n) seleccionado."""
        print("\n=== " + title + " ===")
        for index, option in enumerate(options, start=1):
            print(f"{index}) {option}")

        raw_value = input("Selecciona una opcion: ").strip()
        if not raw_value.isdigit():
            raise AppError("Opcion invalida: debes ingresar un numero.")

        choice = int(raw_value)
        if choice < 1 or choice > len(options):
            raise AppError("Opcion invalida: fuera de rango.")

        return choice
