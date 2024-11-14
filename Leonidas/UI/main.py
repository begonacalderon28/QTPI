import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import mutua_auto    # Importa el script de automatización
from error_codes import get_error_message  # Importa la función de códigos de error


class MainUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leonidas - Automatizador de Descargas")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("background-color: white; font-family: 'Sans Serif';")
        self.initUI()

    def initUI(self):
        # Layout principal
        main_layout = QtWidgets.QVBoxLayout()

        # # Título del Proyecto
        # title_label = QtWidgets.QLabel("Leonidas")
        # title_label.setAlignment(QtCore.Qt.AlignCenter)
        # title_label.setStyleSheet("color: rgb(51, 54, 57); font-size: 24px; font-weight: bold;")

        # Botones con los logos de las aseguradoras
        mutua_button = self.create_logo_button("resources/mutua-logo.png")
        mutua_button.clicked.connect(self.show_mutua_screen)
        allianz_button = self.create_logo_button("resources/allianz-logo.png")
        axa_button = self.create_logo_button("resources/axa-logo.png")

        # Distribuir los logos en un layout
        logo_layout = QtWidgets.QHBoxLayout()
        logo_layout.addWidget(mutua_button)
        logo_layout.addWidget(allianz_button)
        logo_layout.addWidget(axa_button)

        # Añadir todos los elementos al layout principal
        #main_layout.addWidget(title_label)
        main_layout.addLayout(logo_layout)
        self.setLayout(main_layout)

    def create_logo_button(self, logo_path):
        button = QtWidgets.QPushButton()
        button.setFixedSize(180, 180)
        button.setIcon(QtGui.QIcon(logo_path))
        button.setIconSize(QtCore.QSize(160, 160))
        button.setStyleSheet("""
            QPushButton {
                border: 2px solid rgb(84, 92, 102);
                background-color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgb(84, 92, 102);
            }
            QPushButton:pressed {
                background-color: rgb(77, 170, 212);
            }
        """)
        return button

    def show_mutua_screen(self):
        self.mutua_screen = MutuaScreen()
        self.mutua_screen.show()
        self.close()

class MutuaScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Descargas de Mutua")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("background-color: white; font-family: 'Sans Serif';")
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Título
        title_label = QtWidgets.QLabel("Mutua")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("color: rgb(51, 54, 57); font-size: 18px; font-weight: bold;")

        # Inputs y etiquetas
        user_label = QtWidgets.QLabel("Usuario:")
        user_label.setStyleSheet("color: rgb(51, 54, 57); font-size: 14px;")
        self.user_input = QtWidgets.QLineEdit()
        self.user_input.setFixedWidth(180)
        self.user_input.setStyleSheet("background-color: rgb(210, 210, 210);")

        pass_label = QtWidgets.QLabel("Contraseña:")
        pass_label.setStyleSheet("color: rgb(51, 54, 57); font-size: 14px;")
        self.pass_input = QtWidgets.QLineEdit()
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_input.setFixedWidth(180)
        self.pass_input.setStyleSheet("background-color: rgb(210, 210, 210);")

        # Selector de tipo de búsqueda
        select_label = QtWidgets.QLabel("Seleccione tipo de búsqueda:")
        select_label.setStyleSheet("color: rgb(51, 54, 57); font-size: 14px;")
        self.search_type = QtWidgets.QComboBox()
        self.search_type.addItems(["Siniestro", "Póliza", "Matrícula"])
        self.search_type.setFixedWidth(200)
        self.search_type.setStyleSheet("""
            QComboBox {
                background-color: rgb(210, 210, 210);
                padding: 5px;
            }
        """)

        # Número de referencia
        ref_label = QtWidgets.QLabel("Número de referencia:")
        ref_label.setStyleSheet("color: rgb(51, 54, 57); font-size: 14px;")
        self.ref_input = QtWidgets.QLineEdit()
        self.ref_input.setFixedWidth(180)
        self.ref_input.setStyleSheet("background-color: rgb(210, 210, 210);")

        # Ruta de descarga
        download_path_label = QtWidgets.QLabel("Ruta de descarga:")
        download_path_label.setStyleSheet("color: rgb(51, 54, 57); font-size: 14px;")
        self.download_path_input = QtWidgets.QLineEdit()
        self.download_path_input.setReadOnly(True)
        self.download_path_input.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.download_path_button = QtWidgets.QPushButton("Seleccionar ruta")
        self.download_path_button.setFixedWidth(120)
        self.download_path_button.setFixedHeight(40)  # Más alto en eje Y
        self.download_path_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(84, 92, 102);
                color: white;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: rgb(77, 170, 212);
            }
        """)
        self.download_path_button.clicked.connect(self.select_download_path)

        # Botón de descarga
        submit_button = QtWidgets.QPushButton("Descargar")
        submit_button.setFixedWidth(120)
        submit_button.setFixedHeight(40)  # Más alto en eje Y
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(84, 92, 102);
                color: white;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: rgb(77, 170, 212);
            }
        """)
        submit_button.clicked.connect(self.download_files)

        # Botón de retorno con borde
        return_button = QtWidgets.QPushButton()
        return_button.setIcon(QtGui.QIcon("resources/return_icon.png"))  
        return_button.setFixedSize(30, 30)
        return_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid rgb(84, 92, 102);
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: rgb(77, 170, 212);
            }
        """)
        return_button.clicked.connect(self.return_to_main)

        # Organizar los elementos
        layout.addWidget(title_label, alignment=QtCore.Qt.AlignCenter)
        
        input_layout = QtWidgets.QFormLayout()
        input_layout.addRow(user_label, self.user_input)
        input_layout.addRow(pass_label, self.pass_input)
        input_layout.addRow(select_label, self.search_type)
        input_layout.addRow(ref_label, self.ref_input)
        input_layout.addRow(download_path_label, self.download_path_input)
        input_layout.addRow("", self.download_path_button)

        layout.addLayout(input_layout)
        layout.addWidget(submit_button, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(return_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.setLayout(layout)

    def download_files(self):
        # Verificar si todos los campos están completos
        if not self.user_input.text() or not self.pass_input.text() or not self.ref_input.text() or not self.download_path_input.text():
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, rellene todos los campos antes de continuar.")
            return

        # Obtener los valores de entrada
        usuario = self.user_input.text()
        contraseña = self.pass_input.text()
        tipo_busqueda = self.search_type.currentText()
        numero_busqueda = self.ref_input.text()
        ruta_descarga = self.download_path_input.text()

        # Llamar a la función de descarga de mutua_auto.py y capturar el código de retorno
        try:
            resultado = mutua_auto.login_and_download_documents(usuario, contraseña, tipo_busqueda, numero_busqueda, ruta_descarga)
            mensaje_error = get_error_message(resultado)

            # Mostrar el mensaje de error en una ventana emergente
            if resultado == 200:
                QtWidgets.QMessageBox.information(self, "Éxito", mensaje_error)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", mensaje_error)
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Ha ocurrido un error inesperado: {str(e)}")

    def return_to_main(self):
        self.main_screen = MainUI()
        self.main_screen.show()
        self.close()

    def select_download_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de descarga")
        if path:
            self.download_path_input.setText(path)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainUI()
    main_window.show()
    sys.exit(app.exec_())
