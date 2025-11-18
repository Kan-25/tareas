import sys
import re  # Importamos la librería para usar expresiones regulares
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QLabel, QPushButton, QMessageBox, QFrame
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve


class UsernameValidator(QWidget):   # Clase principal de la ventana
    def __init__(self):
        super().__init__()

        # --- Configuración de la ventana ---
        self.setWindowTitle("Validación de Username — Laboratorio")
        self.setGeometry(200, 100, 460, 260)

        # --- Estilos CSS para toda la interfaz ---
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #ffffff;
                font-family: Consolas;
            }

            QLineEdit {
                background-color: #1E1E1E;
                border: 2px solid #3A3A3A;
                padding: 8px;
                border-radius: 8px;
                font-size: 14px;
                color: #C8C8C8;
            }

            QLineEdit:focus {
                border: 2px solid #0078D7;
                color: white;
            }

            QPushButton {
                background-color: #0078D7;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }

            QPushButton:hover {
                background-color: #2894FF;
            }

            #card {
                background-color: #1A1A1A;
                border-radius: 14px;
                padding: 16px;
                border: 1px solid #333333;
            }
        """)

        # ------- Tarjeta principal que contiene los elementos -------
        card = QFrame()
        card.setObjectName("card")  # Para aplicar el estilo del CSS

        card_layout = QVBoxLayout()
        card.setLayout(card_layout)

        # Label del campo de texto
        self.username_label = QLabel("Nombre de usuario:")
        self.username_label.setFont(QFont("Consolas", 12))

        # Caja de entrada de texto
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ejemplo: estudiante_01")
        self.username_input.setFont(QFont("Consolas", 11))

        # Botón para validar
        self.button = QPushButton("Validar Username")
        self.button.clicked.connect(self.validar_username)  # Evento al hacer clic

        # Añadimos componentes al layout
        card_layout.addWidget(self.username_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.button)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(card)
        self.setLayout(layout)

        # Ejecutamos la animación de entrada
        self.animacion_entrada()

    # --------------------------
    # ANIMACIÓN FADE IN
    # --------------------------
    def animacion_entrada(self):
        self.setWindowOpacity(0)  # Inicio invisible
        self.fade = QPropertyAnimation(self, b"windowOpacity")  # Animamos la opacidad
        self.fade.setDuration(800)  # Duración 0.8s
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)  # Termina visible
        self.fade.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade.start()

    # --------------------------
    # ANIMACIÓN SHAKE (vibración)
    # --------------------------
    def shake_window(self):
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(300)  # Duración corta para simular vibración

        # Posición actual
        x = self.x()
        y = self.y()

        # Animación moviendo la ventana izquierda-derecha
        anim.setKeyValueAt(0, QRect(x, y, self.width(), self.height()))
        anim.setKeyValueAt(0.25, QRect(x - 10, y, self.width(), self.height()))
        anim.setKeyValueAt(0.50, QRect(x + 10, y, self.width(), self.height()))
        anim.setKeyValueAt(0.75, QRect(x - 10, y, self.width(), self.height()))
        anim.setKeyValueAt(1, QRect(x, y, self.width(), self.height()))

        anim.start()

    # --------------------------
    # VALIDACIÓN DEL USERNAME
    # --------------------------
    def validar_username(self):
        texto = self.username_input.text()  # Obtener texto ingresado

        # Expresión regular que define las reglas del username
        patron = r"^(?=.{4,16}$)[A-Za-z](?!.*\.\.)[A-Za-z0-9._]*[A-Za-z0-9]$"

        # Validación usando regex
        if re.fullmatch(patron, texto):
            # Si coincide con el patrón, es válido
            QMessageBox.information(self, "Correcto",
                                    "✔ El nombre de usuario es válido.")
        else:
            # Si NO es válido, la ventana tiembla y se muestra alerta
            self.shake_window()
            QMessageBox.warning(self, "Error de Validación",
                                "Username inválido.\n\n"
                                "Reglas:\n"
                                "- 4 a 16 caracteres.\n"
                                "- Inicia con letra.\n"
                                "- Puede usar letras, números, punto, guion bajo.\n"
                                "- No termina en punto ni guion.\n"
                                "- No contiene puntos consecutivos.")

# Punto de entrada del programa
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = UsernameValidator()
    ventana.show()
    sys.exit(app.exec_())  # Ejecuta el bucle de la aplicación
