from application import Application


class Main:
    """Punto de entrada del programa."""

    def start(self) -> None:
        """Inicia la aplicacion."""
        Application().run()


if __name__ == "__main__":
    Main().start()
