import sys
from PyQt5 import QtWidgets
from bin.main_ui import MainUI  # Importa la clase principal de la GUI



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainUI()
    main_window.show()
    sys.exit(app.exec_())
