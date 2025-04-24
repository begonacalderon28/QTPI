import sys
import os
from pathlib import Path
from PyQt5 import QtWidgets, QtGui

# ─────────────────────────  AppUserModelID (icono en barra de tareas) ──
if sys.platform.startswith("win"):
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        u"qtpi.leonidas.automatizador"
    )

# ─────────────────────────  Playwright & recursos  ─────────────────────
if getattr(sys, "frozen", False):                   # ejecutable congelado
    # 1) Playwright buscará los navegadores en su propio paquete
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
    # 2) Carpeta base donde PyInstaller descomprime todos los datos
    BASE_PATH = Path(sys._MEIPASS)
else:                                               # entorno de desarrollo
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "0")
    BASE_PATH = Path(__file__).resolve().parent

# -----------------------------------------------------------------------
from bin.main_ui import MainUI                      # después de configurar env

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Icono global de la aplicación
    icon_path = BASE_PATH / "Logos" / "qtpi-leonidas-logo.ico"
    app.setWindowIcon(QtGui.QIcon(str(icon_path)))

    main_window = MainUI()                          # las demás ventanas heredan
    main_window.show()

    sys.exit(app.exec_())
