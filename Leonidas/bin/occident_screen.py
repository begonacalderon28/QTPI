from PyQt5 import QtWidgets, QtGui, QtCore
from error_codes import get_error_message
from Mutua_occident import occident_auto

class OccidentScreen(QtWidgets.QWidget):
    def __init__(self, return_callback=None):
        super().__init__()
        self.return_callback = return_callback
        self.setWindowTitle("Descargas de Mutua Occident")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("background-color: white; font-family: 'Sans Serif';")
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Título de la pantalla
        title_label = QtWidgets.QLabel("Mutua Occident")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("color: rgb(51, 54, 57); font-size: 18px; font-weight: bold;")

        # Inputs y etiquetas
        user_label = QtWidgets.QLabel("Usuario:")
        self.user_input = QtWidgets.QLineEdit()
        self.user_input.setFixedWidth(180)
        self.user_input.setStyleSheet("background-color: rgb(210, 210, 210);")

        pass_label = QtWidgets.QLabel("Contraseña:")
        self.pass_input = QtWidgets.QLineEdit()
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_input.setFixedWidth(180)
        self.pass_input.setStyleSheet("background-color: rgb(210, 210, 210);")

        siniestro_label = QtWidgets.QLabel("Siniestro:")
        self.siniestro_input = QtWidgets.QLineEdit()
        self.siniestro_input.setFixedWidth(180)
        self.siniestro_input.setStyleSheet("background-color: rgb(210, 210, 210);")

        download_path_label = QtWidgets.QLabel("Ruta de descarga:")
        self.download_path_input = QtWidgets.QLineEdit()
        self.download_path_input.setReadOnly(True)
        self.download_path_input.setStyleSheet("background-color: rgb(210, 210, 210);")
        self.download_path_button = QtWidgets.QPushButton("Seleccionar ruta")
        self.download_path_button.setFixedWidth(120)
        self.download_path_button.setFixedHeight(40)
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

        submit_button = QtWidgets.QPushButton("Descargar")
        submit_button.setFixedWidth(120)
        submit_button.setFixedHeight(40)
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

        layout.addWidget(title_label, alignment=QtCore.Qt.AlignCenter)
        input_layout = QtWidgets.QFormLayout()
        input_layout.addRow(user_label, self.user_input)
        input_layout.addRow(pass_label, self.pass_input)
        input_layout.addRow(siniestro_label, self.siniestro_input)
        input_layout.addRow(download_path_label, self.download_path_input)
        input_layout.addRow("", self.download_path_button)
        layout.addLayout(input_layout)
        layout.addWidget(submit_button, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(return_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.setLayout(layout)

    def download_files(self):
        if not self.user_input.text() or not self.pass_input.text() or not self.siniestro_input.text() or not self.download_path_input.text():
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, rellene todos los campos antes de continuar.")
            return

        usuario = self.user_input.text()
        contrasena = self.pass_input.text()
        siniestro = self.siniestro_input.text()
        ruta_descarga = self.download_path_input.text()

        try:
            resultado = occident_auto.login_and_download_documents(usuario, contrasena, siniestro, ruta_descarga)
            mensaje_error = get_error_message(resultado)
            if resultado == 200:
                QtWidgets.QMessageBox.information(self, "Éxito", mensaje_error)
            else:
                QtWidgets.QMessageBox.warning(self, "Error", mensaje_error)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Ha ocurrido un error inesperado: {str(e)}")

    def return_to_main(self):
        if self.return_callback:
            self.return_callback()
        self.close()

    def select_download_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de descarga")
        if path:
            self.download_path_input.setText(path)
