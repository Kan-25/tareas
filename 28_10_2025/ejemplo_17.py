# ✨ Verificador de Palíndromos Visual en PyQt5
# Autor: David


from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
import sys
import itertools

class PalindromoVisual(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔤 Verificador de Palíndromos Visual ✨")
        self.setGeometry(100, 100, 520, 340)

        # --- Configuración inicial del fondo animado ---
        self.color_index = 0
        self.colores = [
            QColor("#E0FFFF"), QColor("#D8BFD8"),
            QColor("#FFFACD"), QColor("#F0E68C"),
            QColor("#E6E6FA"), QColor("#FFB6C1")
        ]

        # Temporizador para animar el fondo
        self.timer = QTimer()
        self.timer.timeout.connect(self.cambiar_color_fondo)
        self.timer.start(1500)

        # --- Título ---
        self.label_titulo = QLabel("🌟 Verificador de Palíndromos 🌟", self)
        self.label_titulo.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("color: #003366;")

        # --- Campo de entrada ---
        self.input_cadena = QLineEdit(self)
        self.input_cadena.setPlaceholderText("🔹 Escribe una frase aquí...")
        self.input_cadena.setFont(QFont("Consolas", 14))
        self.input_cadena.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 3px solid #4682B4;
                border-radius: 12px;
                background-color: white;
                color: #333;
            }
            QLineEdit:focus {
                border: 3px solid #1E90FF;
                background-color: #F0FFFF;
            }
        """)

        # --- Botón ---
        self.boton_verificar = QPushButton("🔍 Verificar", self)
        self.boton_verificar.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.boton_verificar.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """)
        self.boton_verificar.clicked.connect(self.verificar_palindromo)

        # --- Resultado visual ---
        self.resultado = QLabel("", self)
        self.resultado.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("margin-top: 20px; color: #333;")

        # --- Texto de comparación ---
        self.comparacion = QLabel("", self)
        self.comparacion.setFont(QFont("Consolas", 11))
        self.comparacion.setAlignment(Qt.AlignCenter)
        self.comparacion.setStyleSheet("color: #222; margin-top: 10px;")

        # --- Diseño general ---
        layout = QVBoxLayout()
        layout.addWidget(self.label_titulo)
        layout.addWidget(self.input_cadena)
        layout.addWidget(self.boton_verificar)
        layout.addWidget(self.resultado)
        layout.addWidget(self.comparacion)
        layout.setSpacing(10)
        self.setLayout(layout)

    def cambiar_color_fondo(self):
        """Cambia el color de fondo suavemente cada 1.5 segundos"""
        color = self.colores[self.color_index]
        gradiente = QLinearGradient(0, 0, 0, self.height())
        gradiente.setColorAt(0.0, color)
        gradiente.setColorAt(1.0, QColor("white"))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradiente))
        self.setPalette(palette)
        self.color_index = (self.color_index + 1) % len(self.colores)

    def verificar_palindromo(self):
        texto_original = self.input_cadena.text().strip()
        if not texto_original:
            QMessageBox.warning(self, "⚠️ Advertencia", "Por favor ingresa una frase antes de verificar.")
            return

        # Normalizamos la cadena
        cadena = ''.join(filter(str.isalnum, texto_original)).lower()
        cadena_invertida = cadena[::-1]

        # Resultado visual
        if cadena == cadena_invertida:
            self.resultado.setText(f"✅ '{texto_original}' ES un palíndromo 💚")
            self.resultado.setStyleSheet("color: green; font-weight: bold; background-color: #E0FFE0; border-radius: 10px; padding: 8px;")
        else:
            self.resultado.setText(f"❌ '{texto_original}' NO es un palíndromo 💔")
            self.resultado.setStyleSheet("color: red; font-weight: bold; background-color: #FFE0E0; border-radius: 10px; padding: 8px;")

        self.comparacion.setText(f"🪞 Original: {cadena}\n🔁 Invertida: {cadena_invertida}")

# --- Ejecución principal ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PalindromoVisual()
    ventana.show()
    sys.exit(app.exec_())
