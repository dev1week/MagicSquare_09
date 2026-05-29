"""Magic Square 4×4 — PyQt6 desktop entry point."""

import sys


def main() -> int:
    """Launch the Magic Square GUI application."""
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        sys.stderr.write(
            "PyQt6 is required for the GUI. Install with:\n"
            "  pip install -e \".[gui]\"\n"
            "or:\n"
            "  pip install PyQt6\n"
        )
        return 1

    from src.boundary.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("Magic Square")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
