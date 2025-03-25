from PyQt5 import QtWidgets, QtGui, QtCore
from bin.mutua_screen import MutuaScreen
from bin.allianz_screen import AllianzScreen
from bin.bbva_screen import BBVAScreen
from bin.propietarios_screen import PropietariosScreen
from bin.occident_screen import OccidentScreen

class MainUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leonidas - Automatizador de Descargas")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet("background-color: white; font-family: 'Sans Serif';")
        self.initUI()

    def initUI(self):
        main_layout = QtWidgets.QVBoxLayout()

        # Botones con los logos de las aseguradoras
        mutua_button = self.create_logo_button("resources/mutua-logo.png")
        mutua_button.clicked.connect(self.show_mutua_screen)
        allianz_button = self.create_logo_button("resources/allianz-logo.png")
        allianz_button.clicked.connect(self.show_allianz_screen)
        propietarios_button = self.create_logo_button("resources/mutua-propietarios.png")
        propietarios_button.clicked.connect(self.show_propietarios_screen)
        bbva_button = self.create_logo_button("resources/bbva-logo.png")
        bbva_button.clicked.connect(self.show_bbva_screen)
        occident_button = self.create_logo_button("resources/occident-logo.png")
        occident_button.clicked.connect(self.show_occident_screen)

        # Distribuir los logos en un layout horizontal
        logo_layout = QtWidgets.QHBoxLayout()
        logo_layout.addWidget(mutua_button)
        logo_layout.addWidget(allianz_button)
        logo_layout.addWidget(propietarios_button)
        logo_layout.addWidget(bbva_button)
        logo_layout.addWidget(occident_button)

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
        self.screen = MutuaScreen(return_callback=self.show)
        self.screen.show()
        self.hide()  # Oculta el MainUI en lugar de cerrarlo


    def show_allianz_screen(self):
        self.screen = AllianzScreen(return_callback=self.show)
        self.screen.show()
        self.hide() 

    def show_bbva_screen(self):
        self.screen = BBVAScreen(return_callback=self.show)
        self.screen.show()
        self.hide() 

    def show_propietarios_screen(self):
        self.screen = PropietariosScreen(return_callback=self.show)
        self.screen.show()
        self.hide() 

    def show_occident_screen(self):
        self.screen = OccidentScreen(return_callback=self.show)
        self.screen.show()
        self.hide() 

    def show_main_ui(self):
        # Si deseas crear una nueva instancia o volver a mostrar la misma:
        main_ui = MainUI()
        main_ui.show()

